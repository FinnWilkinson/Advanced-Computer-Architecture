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


    # Execute next instruction for each EU in pipeline
    def execute(self, error, finished, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, branchPredType, flushOutput, pipelines, pipelineCount, PC, MEM, ARF, ROB, BTB, BIPB, LSQ) :
        # loop through the 4 execution units
        for i in range(0, 4) :
            if(self.IS_EX[i].Empty == False) :
                output = None

                # Execute instruction in IS_EX[i]
                output, error, finished, branchTakenCount, branchExecutedCount, correctBranchPreds, PC, MEM = self.EU[i].executeInstruction(self.IS_EX, i, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, branchPredType, correctBranchPreds, LSQ)
                
                #print("EX " + str(self.IS_EX[i].InstructionNumber) + "  " + str(self.IS_EX[i].Op) + "  " + str(self.IS_EX[i].D1) + "  " + str(self.IS_EX[i].S1) + "  " + str(self.IS_EX[i].S2))

                # If OpCode not recognised
                if(error == -1) :
                    break

                # If branch taken (no BP) / branch mis-prediction (error = 1), flush pipeline
                if(error == 1) : 
                    flushOutput = copy.copy(self.IS_EX[i].InstructionNumber)
                    # Re-set IS_EX[i]
                    self.IS_EX[i].Empty = True 
                    # Increment execute count
                    instructionExecuteCount += 1
                    break

                # Check for multi cycle instruction
                if(error == 2) :
                    # Do nothing, reset error 
                    error = 0
                    continue

                # Add result to ROB + forward to any waiting instructions in all RS
                if(self.IS_EX[i].Op not in self.readOnlyINSTR) :
                    tempROBaddr = ROB.InstructionNumber.index(self.IS_EX[i].InstructionNumber)
                    ROB.Value[tempROBaddr] = copy.copy(output)
                    ROB.Complete[tempROBaddr] = copy.copy(1)
                    self.forward(pipelines, pipelineCount, output, ("ROB" + str(tempROBaddr)))
                # Re-set IS_EX[i]
                self.IS_EX[i].Empty = True 
                # Increment execute count
                instructionExecuteCount += 1

        return error, finished, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, flushOutput, PC, MEM


    # Issue instructions to EUs
    def issue(self, pipelines, pipelineCount, branchPredType, stallThisCycle, instructionFetchCount, ARF, ROB, LSQ) :
        tempStallIndicatorIS = self.issueUnit.issue(self.RS, self.IS_EX, ARF, ROB, branchPredType, LSQ, pipelines, pipelineCount)  
        if tempStallIndicatorIS == True and instructionFetchCount > 3 :
            stallThisCycle = copy.copy(stallThisCycle or True)    

        #for i in range(0, 4) :
            #if(self.IS_EX[i].Empty == False) :
                #print("IS " + str(self.IS_EX[i].InstructionNumber) + "  " + str(self.IS_EX[i].Op) + "  " + str(self.IS_EX[i].D1) + "  " + str(self.IS_EX[i].S1) + "  " + str(self.IS_EX[i].S2))


        return stallThisCycle


    # De-Code next instruction in pipeline
    def decode(self, branchPredType, stallThisCycle, instructionFetchCount, PC, ARF, RAT, ROB, BTB, BIPB, LSQ) :
        needToFlush = False
        flushOutput = -1
        if(self.IF_DE.Empty == False):
            tempStallIndicatorDE, PC, needToFlush, flushOutput = self.decodeUnit.decode(self.IF_DE, self.RS, ARF, RAT, ROB, BIPB, BTB, PC, branchPredType, LSQ)  
            if tempStallIndicatorDE == True and instructionFetchCount > 2 :
                stallThisCycle = copy.copy(stallThisCycle or True)

        #for j in range(0,3) :
            #for i in range(0, len(self.RS[j].Instruction)) :
                #print("RS " + str(self.RS[j].Instruction[i].instructionNumber) + "  " + str(self.RS[j].Op[i]) + "  " + str(self.RS[j].D1[i]) + "  " + str(self.RS[j].V1[i]) + "  " + str(self.RS[j].V2[i]))    

        return stallThisCycle, PC, needToFlush, flushOutput


    # Fetch next instruction
    def fetch(self, instructionFetchCount, nextInstructionNumber, branchPredType, PC, INSTR, BTB, BIPB) :
        if(self.IF_DE.Empty is True and PC < len(INSTR)):
            PC, instructionFetchCount, nextInstructionNumber = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount, BTB, BIPB, branchPredType, nextInstructionNumber)

        #print("IF " + str(self.IF_DE.Instruction.instructionNumber) + "  " + str(self.IF_DE.Instruction.opCode) + "  " + str(self.IF_DE.Instruction.operand1) + "  " + str(self.IF_DE.Instruction.operand2) + "  " + str(self.IF_DE.Instruction.operand3))

        return instructionFetchCount, nextInstructionNumber, PC


    # Flush pipeline of any instructions after branch instruction number
    def flush(self, branchInstructionNumber, nextInstructionNumber) :
        # Flush IF_DE
        if(self.IF_DE.Instruction.instructionNumber > branchInstructionNumber) :
            nextInstructionNumber -= 1
            self.IF_DE.Empty = True

        # Flush Reservation Stations
        for k in range(0,3) :
            currentInx = 0
            length = len(self.RS[k].Instruction)
            while True :
                # If RS empty, go onto next one
                if(length == 0) :
                    break
                # If gone through whole RS, go onto next one
                if(currentInx == length) :
                    break
                # Check if we need to remove from RS 
                if(self.RS[k].Instruction[currentInx].instructionNumber > branchInstructionNumber) :
                    self.RS[k].Instruction.pop(currentInx)
                    self.RS[k].Op.pop(currentInx)
                    self.RS[k].D1.pop(currentInx)
                    self.RS[k].V1.pop(currentInx)
                    self.RS[k].V2.pop(currentInx)
                    self.RS[k].S1.pop(currentInx)
                    self.RS[k].S2.pop(currentInx)
                    # If removing branch/logic, need to pop an extra item
                    if(k == 2) :
                        self.RS[k].BranchPC.pop(currentInx)
                    length -= 1 
                else :
                    currentInx += 1  

        # Flush IS_EX
        for i in range(0, 4) :
            if(self.IS_EX[i].InstructionNumber > branchInstructionNumber) :
                self.IS_EX[i].Empty = True
                # Re-set execusion count if mid way through executing instruction
                self.EU[i].ExecutionCount = 0

        return nextInstructionNumber


    # Forward value to any waiting instructions in all RS
    def forward(self, pipelines, pipelineCount, value, ROBaddress) :
        for i in range(0, pipelineCount) :
            # Go through each Reservation Station
            for j in range(0, 3) :
                # Go through each instruction in RS
                for k in range(0, len(pipelines[i].RS[j].Instruction)) :
                    # Check D1
                    if(pipelines[i].RS[j].D1[k] == ROBaddress and pipelines[i].RS[j].Instruction[k].opCode in self.readOnlyINSTR) :
                        pipelines[i].RS[j].D1[k] = copy.copy(value)
                    # Check V1
                    if(pipelines[i].RS[j].V1[k] == ROBaddress) :
                        pipelines[i].RS[j].S1[k] = copy.copy(value)
                        pipelines[i].RS[j].V1[k] = copy.copy(0)
                    # Check V2
                    if(pipelines[i].RS[j].V2[k] == ROBaddress) :
                        pipelines[i].RS[j].S2[k] = copy.copy(value)
                        pipelines[i].RS[j].V2[k] = copy.copy(0)
              


    # def advance(self, PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount, finished, ARF, MEM, INSTR, ROB, RAT, BIPB, BTB, LSQ, branchPredType, error, pipelines, pipelineCount, nextInstructionNumber) :
    #     stallThisCycle = False
        
        # Advance back to front to ensure pipeline can progress

        # WRITE BACK (WB) - DONE
        # self.writeBackUnit.writeBack(ROB, RAT, ARF, BIPB)   # ROB write back
        # self.writeBackUnit.LSQCommit(LSQ, MEM, BIPB) # LSQ write back

        # EXECUTE (EX) - DONE
        # for i in range(0,4) :
        #     if(self.IS_EX[i].Empty is False) :
        #         output = None
        #         #print("EX " + str(self.IS_EX[i].InstructionNumber) + "  " + str(self.IS_EX[i].Op) + "  " + str(self.IS_EX[i].D1) + "  " + str(self.IS_EX[i].S1) + "  " + str(self.IS_EX[i].S2))
        #         error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output, correctBranchPreds = self.EU[i].executeInstruction(self.IS_EX, i, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, branchPredType, correctBranchPreds, LSQ)
        #         # If branch taken (error = 1), flush pipeline
        #         if(error == 1) : 
        #             for k in range(0, pipelineCount) :
        #                 nextInstructionNumber = pipelines[k].flush(self.IS_EX[i].InstructionNumber, ARF, nextInstructionNumber, ROB, RAT, BIPB, LSQ)
        #             flushCount += 1
        #             error = 0   # Reset error for Main to process correctly
        #         # If multi-cycle instruction (error = 2), delay output
        #         if(error != 2) :  
        #             if(self.IS_EX[i].Op not in self.readOnlyINSTR) :
        #                 tempROBaddr = int(self.IS_EX[i].D1[3:])
        #                 ROB.Value[tempROBaddr] = output
        #                 ROB.Complete[tempROBaddr] = 1
        #             self.IS_EX[i].Empty = True 
        #             instructionExecuteCount += 1
        #         else :
        #             error = 0   # Reset error for Main to process correctly if multi-cycle


        #for j in range(0,3) :
            #for i in range(0, len(self.RS[j].Instruction)) :
                #print("RS " + str(self.RS[j].Instruction[i].instructionNumber) + "  " + str(self.RS[j].Op[i]) + "  " + str(self.RS[j].D1[i]) + "  " + str(self.RS[j].V1[i]) + "  " + str(self.RS[j].V2[i]))


        # # ISSUE (IS) - DONE
        # tempStallIndicatorIS = self.issueUnit.issue(self.RS, self.IS_EX, ARF, ROB, branchPredType, LSQ)  
        # if tempStallIndicatorIS == True and instructionFetchCount > 3 :
        #     stallThisCycle = copy.copy(stallThisCycle or True)

        #print("DE " + str(self.IF_DE.Instruction.instructionNumber) + "  " + str(self.IF_DE.Instruction.opCode) + "  " + str(self.IF_DE.Instruction.operand1) + "  " + str(self.IF_DE.Instruction.operand2) + "  " + str(self.IF_DE.Instruction.operand3))

        # # DECODE (DE) - DONE
        # if self.IF_DE.Empty is False :
        #     tempStallIndicatorDE, PC = self.decodeUnit.decode(self.IF_DE, self.RS, ARF, RAT, ROB, BIPB, BTB, PC, branchPredType, LSQ)  
        #     if tempStallIndicatorDE == True and instructionFetchCount > 2 :
        #         stallThisCycle = copy.copy(stallThisCycle or True)

        #print("IF " + str(self.IF_DE.Instruction.instructionNumber) + "  " + str(self.IF_DE.Instruction.opCode) + "  " + str(self.IF_DE.Instruction.operand1) + "  " + str(self.IF_DE.Instruction.operand2) + "  " + str(self.IF_DE.Instruction.operand3))
  

        # INSTRUCTION FETCH (IF) - DONE
        # if self.IF_DE.Empty is True and PC < len(INSTR):
        #     PC, instructionFetchCount, nextInstructionNumber = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount, BTB, BIPB, branchPredType, nextInstructionNumber)

        
        # # Increase stall count if stall in pipeline
        # if stallThisCycle == True :
        #     stallCount += 1

        # return PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount, finished, ARF, MEM, ROB, RAT, BIPB, BTB, LSQ, error, pipelines, nextInstructionNumber



    # All instrucions with instructionNumber > than this function's input are removed, ROB and RAT are updated accordingly
    # def flush_old(self, instructionNumber, ARF, nextInstructionNumber, ROB, RAT, BIPB, LSQ) :        
        # # Flush IF_DE
        # if(self.IF_DE.Instruction.instructionNumber > instructionNumber) :
        #     nextInstructionNumber -= 1
        #     self.IF_DE.Empty = True

        # Flush RSs ; Re-Adjust ROB and RAT
        # for k in range(0,3) :
        #     currentInx = 0
        #     length = len(self.RS[k].Instruction)
        #     while True :
        #         if(currentInx == length) :
        #             break
        #         if(length > 0 and self.RS[k].Instruction[currentInx].instructionNumber > instructionNumber) :
        #             # Remove from RS 
        #             self.RS[k].Instruction.pop(currentInx)
        #             self.RS[k].Op.pop(currentInx)
        #             self.RS[k].D1.pop(currentInx)
        #             self.RS[k].V1.pop(currentInx)
        #             self.RS[k].V2.pop(currentInx)
        #             self.RS[k].S1.pop(currentInx)
        #             self.RS[k].S2.pop(currentInx)
        #             if(k == 2) :
        #                 self.RS[k].BranchPC.pop(currentInx)
        #             length -= 1 
        #         else :
        #             currentInx += 1              
                    
        # # Flush IS_EX
        # for i in range(0, 4) :
        #     if(self.IS_EX[i].InstructionNumber > instructionNumber) :
        #         self.IS_EX[i].Empty = True


        # # Flush ROB 
        # robIndex = copy.copy(ROB.CommitPtr)
        # while True :
        #     if(robIndex == ROB.IssuePtr) :
        #         break
        #     if(ROB.InstructionNumber[robIndex] > instructionNumber and ROB.Register[robIndex] != "SKIP") :
        #         # Find last value for our reg, update RAT
        #         reg = ROB.Register[robIndex]
        #         newRegAddr = ""
        #         indx = copy.copy(robIndex)

        #         while True :
        #             indx = copy.copy((indx - 1 + 128) % 128) # reduce index by 1, if goes to negative loop around like ROB pointer does
        #             if(indx == (ROB.CommitPtr - 1 + 128) % 128) :
        #                 newRegAddr = copy.copy(reg)
        #                 break
        #             if(ROB.Register[indx] == reg and ROB.InstructionNumber[indx] < instructionNumber) :
        #                 newRegAddr = copy.copy("ROB" + str(indx))
        #                 break
        #             else :
        #                 if(ROB.CommitPtr == indx) :
        #                     newRegAddr = copy.copy(reg)
        #                     break
                
        #         # Update RAT
        #         RAT.Address[int(reg[1:])] = copy.copy(newRegAddr)
        #         # Update ROB
        #         ROB.Register[robIndex] = copy.copy("SKIP")

        #     robIndex = copy.copy((robIndex + 1) % 128)
            

        # Flush BIPB (Branch in Pipeline Buffer)
        # currentIndex = 0
        # listLength = len(BIPB.BranchPC)
        # while currentIndex < listLength :
        #     if(BIPB.InstructionNumber[currentIndex] > instructionNumber) :
        #         BIPB.BranchPC.pop(currentIndex)
        #         BIPB.InstructionNumber.pop(currentIndex)
        #         BIPB.Prediction.pop(currentIndex)
        #         BIPB.TargetAddress.pop(currentIndex)
        #         listLength -= 1
        #     else :
        #         currentIndex += 1

        # Flush LSQ - Set Issue pointer back to before mispredicted instructions
        # ptr = copy.copy(LSQ.CommitPtr)
        # while True :
        #     if(ptr == LSQ.IssuePtr) :
        #         break
        #     if(LSQ.InstructionNumber[ptr] > instructionNumber) :
        #         LSQ.Complete[ptr] = 0
        #         LSQ.IssuePtr = copy.copy(ptr)
        #         break
        #     ptr = copy.copy((ptr + 1) % 128)
            
    
        
        # return nextInstructionNumber

       