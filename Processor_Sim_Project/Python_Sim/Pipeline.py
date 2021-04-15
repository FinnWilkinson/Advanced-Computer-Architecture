from Instruction import Instruction
from Register_File import *
from Pipeline_Registers import *
from Fetch import Fetch_Unit
from Decode import Decode_Unit
from Issue import Issue_Unit
from Execute import *
from Write_Back import Write_Back_Unit
from Reg_To_Reg_Index import *

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
                error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output = self.EU[i].executeInstruction(self.IS_EX, i, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount)
                # If branch taken (error = 1), flush pipeline
                if(error == 1) : 
                    flushCount = self.flush(self.IS_EX[i].InstructionNumber, flushCount, ARF, instructionFetchCount)
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


        # ISSUE (IS) - DONE
        tempStallIndicator = self.issueUnit.issue(self.RS, self.IS_EX, ARF, ROB)  
        if tempStallIndicator == True and instructionFetchCount > 2 :
            stallThisCycle = True
             

        # DECODE (DE) - DONE
        if self.IF_DE.Empty is False :
            stallThisCycle = self.decodeUnit.decode(self.IF_DE, self.RS, ARF, RAT, ROB)      
                    

        # INSTRUCTION FETCH (IF) - DONE
        if self.IF_DE.Empty is True and PC < len(INSTR):
            PC, instructionFetchCount = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount)
        elif self.IF_DE.Empty is False :
            stallThisCycle = True


        # Increase stall count if stall in pipeline
        if stallThisCycle == True :
            stallCount += 1

        return PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, ARF, MEM, ROB, RAT, error


    def flush(self, instructionNumber, flushCount, ARF, instructionFetchCount) :
        # All instrucions with instructionNumber > than this function's input set to invalid so they are not executed or written back
        if(self.IF_DE.Instruction.instructionNumber > instructionNumber) :
            self.IF_DE.Empty = True
        self.RS[0].flush(instructionNumber)
        self.RS[1].flush(instructionNumber)
        self.RS[2].flush(instructionNumber)
 
        flushCount += 1
        return flushCount