from Instruction import Instruction
from Register_File import *
from Pipeline_Registers import *
from Fetch import Fetch_Unit
from Decode import Decode_Unit
from Issue import Issue_Unit
from Execute import *
from Write_Back import Write_Back_Unit
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


    def advance(self, PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount, finished, ARF, MEM, INSTR, ROB, RAT, BIPB, BTB, LSQ, branchPredType, error, pipelines, pipelineCount, nextInstructionNumber) :
        stallThisCycle = False
        
        # Advance back to front to ensure pipeline can progress

        # WRITE BACK (WB) - DONE
        self.writeBackUnit.writeBack(ROB, RAT, ARF, BIPB)   # ROB write back
        self.writeBackUnit.LSQCommit(LSQ, MEM, BIPB) # LSQ write back

        # EXECUTE (EX) - DONE
        for i in range(0,4) :
            if(self.IS_EX[i].Empty is False) :
                output = None
                #print("EX " + str(self.IS_EX[i].InstructionNumber) + "  " + str(self.IS_EX[i].Op) + "  " + str(self.IS_EX[i].D1) + "  " + str(self.IS_EX[i].S1) + "  " + str(self.IS_EX[i].S2))
                error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output, correctBranchPreds = self.EU[i].executeInstruction(self.IS_EX, i, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, branchPredType, correctBranchPreds, LSQ)
                # If branch taken (error = 1), flush pipeline
                if(error == 1) : 
                    for k in range(0, pipelineCount) :
                        nextInstructionNumber = pipelines[k].flush(self.IS_EX[i].InstructionNumber, ARF, nextInstructionNumber, ROB, RAT, BIPB, LSQ)
                    flushCount += 1
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
            #for i in range(0, len(self.RS[j].Instruction)) :
                #print("RS " + str(self.RS[j].Instruction[i].instructionNumber) + "  " + str(self.RS[j].Op[i]) + "  " + str(self.RS[j].D1[i]) + "  " + str(self.RS[j].V1[i]) + "  " + str(self.RS[j].V2[i]))


        # ISSUE (IS) - DONE
        tempStallIndicatorIS = self.issueUnit.issue(self.RS, self.IS_EX, ARF, ROB, branchPredType, LSQ)  
        if tempStallIndicatorIS == True and instructionFetchCount > 3 :
            stallThisCycle = copy.copy(stallThisCycle or True)

        #print("DE " + str(self.IF_DE.Instruction.instructionNumber) + "  " + str(self.IF_DE.Instruction.opCode) + "  " + str(self.IF_DE.Instruction.operand1) + "  " + str(self.IF_DE.Instruction.operand2) + "  " + str(self.IF_DE.Instruction.operand3))

        # DECODE (DE) - DONE
        if self.IF_DE.Empty is False :
            tempStallIndicatorDE, PC = self.decodeUnit.decode(self.IF_DE, self.RS, ARF, RAT, ROB, BIPB, BTB, PC, branchPredType, LSQ)  
            if tempStallIndicatorDE == True and instructionFetchCount > 2 :
                stallThisCycle = copy.copy(stallThisCycle or True)

        #print("IF " + str(self.IF_DE.Instruction.instructionNumber) + "  " + str(self.IF_DE.Instruction.opCode) + "  " + str(self.IF_DE.Instruction.operand1) + "  " + str(self.IF_DE.Instruction.operand2) + "  " + str(self.IF_DE.Instruction.operand3))
  

        # INSTRUCTION FETCH (IF) - DONE
        if self.IF_DE.Empty is True and PC < len(INSTR):
            PC, instructionFetchCount, nextInstructionNumber = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount, BTB, BIPB, branchPredType, nextInstructionNumber)

        
        # Increase stall count if stall in pipeline
        if stallThisCycle == True :
            stallCount += 1

        return PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount, finished, ARF, MEM, ROB, RAT, BIPB, BTB, LSQ, error, pipelines, nextInstructionNumber


    
    # All instrucions with instructionNumber > than this function's input are removed, ROB and RAT are updated accordingly
    def flush(self, instructionNumber, ARF, nextInstructionNumber, ROB, RAT, BIPB, LSQ) :        
        # Flush IF_DE
        if(self.IF_DE.Instruction.instructionNumber > instructionNumber) :
            nextInstructionNumber -= 1
            self.IF_DE.Empty = True

        # Flush RSs ; Re-Adjust ROB and RAT
        for k in range(0,3) :
            currentInx = 0
            length = len(self.RS[k].Instruction)
            while True :
                if(currentInx == length) :
                    break
                if(length > 0 and self.RS[k].Instruction[currentInx].instructionNumber > instructionNumber) :
                    # Remove from RS 
                    self.RS[k].Instruction.pop(currentInx)
                    self.RS[k].Op.pop(currentInx)
                    self.RS[k].D1.pop(currentInx)
                    self.RS[k].V1.pop(currentInx)
                    self.RS[k].V2.pop(currentInx)
                    self.RS[k].S1.pop(currentInx)
                    self.RS[k].S2.pop(currentInx)
                    if(k == 2) :
                        self.RS[k].BranchPC.pop(currentInx)
                    length -= 1 
                else :
                    currentInx += 1              
                    
        # Flush IS_EX
        for i in range(0, 4) :
            if(self.IS_EX[i].InstructionNumber > instructionNumber) :
                self.IS_EX[i].Empty = True


        # Flush ROB 
        robIndex = copy.copy(ROB.CommitPtr)
        while True :
            if(robIndex == ROB.IssuePtr) :
                break
            if(ROB.InstructionNumber[robIndex] > instructionNumber and ROB.Register[robIndex] != "SKIP") :
                # Find last value for our reg, update RAT
                reg = ROB.Register[robIndex]
                newRegAddr = ""
                indx = copy.copy(robIndex)

                while True :
                    indx = copy.copy((indx - 1 + 128) % 128) # reduce index by 1, if goes to negative loop around like ROB pointer does
                    if(indx == (ROB.CommitPtr - 1 + 128) % 128) :
                        newRegAddr = copy.copy(reg)
                        break
                    if(ROB.Register[indx] == reg and ROB.InstructionNumber[indx] < instructionNumber) :
                        newRegAddr = copy.copy("ROB" + str(indx))
                        break
                    else :
                        if(ROB.CommitPtr == indx) :
                            newRegAddr = copy.copy(reg)
                            break
                
                # Update RAT
                RAT.Address[int(reg[1:])] = copy.copy(newRegAddr)
                # Update ROB
                ROB.Register[robIndex] = copy.copy("SKIP")

            robIndex = copy.copy((robIndex + 1) % 128)
            

        # Flush BIPB (Branch in Pipeline Buffer)
        currentIndex = 0
        listLength = len(BIPB.BranchPC)
        while currentIndex < listLength :
            if(BIPB.InstructionNumber[currentIndex] > instructionNumber) :
                BIPB.BranchPC.pop(currentIndex)
                BIPB.InstructionNumber.pop(currentIndex)
                BIPB.Prediction.pop(currentIndex)
                BIPB.TargetAddress.pop(currentIndex)
                listLength -= 1
            else :
                currentIndex += 1

        # Flush LSQ - Set Issue pointer back to before mispredicted instructions
        ptr = copy.copy(LSQ.CommitPtr)
        while True :
            if(ptr == LSQ.IssuePtr) :
                break
            if(LSQ.InstructionNumber[ptr] > instructionNumber) :
                LSQ.Complete[ptr] = 0
                LSQ.IssuePtr = copy.copy(ptr)
                break
            ptr = copy.copy((ptr + 1) % 128)
            
    
        
        return nextInstructionNumber

       