from Instruction import Instruction
from Register_File import *
from Pipeline_Registers import *
from Fetch import Fetch_Unit
from Decode import Decode_Unit
from Issue import Issue_Unit
from Execute import *
from Write_Back import Write_Back_Unit
from Reg_To_Reg_Index import *
import copy as copy

class Pipeline:

    def __init__(self) :
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT"]

        self.IF_DE = IF_DE_Reg()                                                            # Instruction, TargetAddress
        self.RS = [ReservationStation(), ReservationStation(), ReservationStation()]        # 0 = ARITHMETIC, 1 = LOAD/STORE, 2 = BRANCH/LOGIC. Max length of 16 for Arith, 8 for others
        self.IS_EX = [IS_EX_Reg(), IS_EX_Reg(), IS_EX_Reg(), IS_EX_Reg()]                   # TargetAddress, Op, D1, S1, S2 

        self.fetchUnit = Fetch_Unit()
        self.decodeUnit = Decode_Unit()
        self.issueUnit = Issue_Unit()
        self.EU = [ARITH_Execution_Unit(), ARITH_Execution_Unit(), LDSTR_Execution_Unit(), BRLGC_Execution_Unit()] # 0,1 = ARITHMETIC, 2 = LOAD/STORE, 3 = BRANCH/LOGIC
        self.writeBackUnit = Write_Back_Unit()


    def advance(self, PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, ARF, MEM, INSTR, ROB, RAT, error) :
        stallThisCycle = False
        
        # Advance back to front to ensure pipeline can progress
        
        # WRITE BACK (WB) - DONE
        self.writeBackUnit.writeBack(ROB, RAT, ARF)

        # EXECUTE (EX) - DONE
        for i in range(0,4) :
            if(self.IS_EX[i].Empty is False) :
                output = None
                #print("EX " + str(self.IS_EX[i].InstructionNumber) + "  " + str(self.IS_EX[i].Op) + "  " + str(self.IS_EX[i].D1) + "  " + str(self.IS_EX[i].S1) + "  " + str(self.IS_EX[i].S2))
                error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output = self.EU[i].executeInstruction(self.IS_EX, i, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount)
                # If branch taken (error = 1), flush pipeline
                if(error == 1) : 
                    flushCount, instructionFetchCount = self.flush(self.IS_EX[i].InstructionNumber, flushCount, ARF, instructionFetchCount, ROB, RAT)
                    error = 0   # Reset error for Main to process correctly
                # If multi-cycle instruction (error = 2), delay output
                if(error != 2) :  
                    if(self.IS_EX[i].Op not in self.readOnlyINSTR) :
                        tempROBaddr = int(self.IS_EX[i].D1[3:])
                        ROB.Value[tempROBaddr] = output
                        ROB.Complete[tempROBaddr] = 1
                    self.IS_EX[i].Empty = True 
                    instructionExecuteCount += 1
                else :
                    error = 0   # Reset error for Main to process correctly if multi-cycle


        #for j in range(0,3) :
        #    for i in range(0, len(self.RS[j].Instruction)) :
        #                print("RS " + str(self.RS[j].Instruction[i].instructionNumber) + "  " + str(self.RS[j].Op[i]) + "  " + str(self.RS[j].D1[i]) + "  " + str(self.RS[j].V1[i]) + "  " + str(self.RS[j].V2[i]))


        # ISSUE (IS) - DONE
        tempStallIndicator = self.issueUnit.issue(self.RS, self.IS_EX, ARF, ROB)  
        if tempStallIndicator == True and instructionFetchCount > 2 :
            stallThisCycle = copy.copy(stallThisCycle or True)


        # DECODE (DE) - DONE
        if self.IF_DE.Empty is False :
            stallThisCycle = copy.copy(stallThisCycle or self.decodeUnit.decode(self.IF_DE, self.RS, ARF, RAT, ROB))      
                    
        #print("IF " + str(self.IF_DE.Instruction.instructionNumber) + "  " + str(self.IF_DE.Instruction.opCode) + "  " + str(self.IF_DE.Instruction.operand1) + "  " + str(self.IF_DE.Instruction.operand2) + "  " + str(self.IF_DE.Instruction.operand3))

        # INSTRUCTION FETCH (IF) - DONE
        if self.IF_DE.Empty is True and PC < len(INSTR):
            PC, instructionFetchCount = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount)
        elif self.IF_DE.Empty is False :
            stallThisCycle = copy.copy(stallThisCycle or True)


        # Increase stall count if stall in pipeline
        if stallThisCycle == True :
            stallCount += 1

        return PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, ARF, MEM, ROB, RAT, error

    
    # All instrucions with instructionNumber > than this function's input are removed, ROB and RAT are updated accordingly
    def flush(self, instructionNumber, flushCount, ARF, instructionFetchCount, ROB, RAT) :        
        # Flush ID_DE
        if(self.IF_DE.Instruction.instructionNumber > instructionNumber) :
            instructionFetchCount -= 1
            self.IF_DE.Empty = True

        # Flush RSs ; Re-Adjust ROB and RAT
        for k in range(0,3) :
            for i in range(0, len(self.RS[k].Instruction)) :
                if(self.RS[k].Instruction[i].instructionNumber > instructionNumber) :
                    # If instruction would have written back to ROB
                    if("ROB" in str(self.RS[k].D1[i]) and self.RS[k].Op[i] not in self.readOnlyINSTR) :
                        # Get ROB index
                        index = int(self.RS[k].D1[i][3:])
                        # Set Complete in ROB
                        ROB.Complete[index] = 1
                        # Get register it would have written back to
                        ogReg = copy.copy(ROB.Register[index])

                        # Get new latest ROB address for this register
                        newROBaddr = ""
                        while True :
                            index = copy.copy( ((index - 1 + 128)%128) )    # reduce index by 1, if goes to negative loop around like ROB pointer does
                            if(ROB.Register[index] == ogReg) :
                                # Found replacement
                                newROBaddr = copy.copy("ROB" + str(index))
                                break
                            else :
                                if(ROB.CommitPtr == index) :
                                    # Oldest for this reg has already been written back
                                    newROBaddr = copy.copy(ogReg)
                                    break

                        # Update RAT
                        RAT.Address[int(ogReg[1:])] = copy.copy(newROBaddr)

                        # Set ROB register to SKIP so nothing committed
                        ROB.Register[int(self.RS[k].D1[i][3:])] = copy.copy("SKIP")

                    # Set invalid in RS 
                    self.RS[k].Instruction[i].Valid = False              
                    
    
        flushCount += 1
        return flushCount, instructionFetchCount

       