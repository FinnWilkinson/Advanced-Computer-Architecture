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
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT", "PAUSE"]

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
    def issue(self, pipelines, pipelineCount, branchPredType, stallThisCycle, instructionFetchCount, ARF, ROB, LSQ, ROBsize) :
        tempStallIndicatorIS = self.issueUnit.issue(self.RS, self.IS_EX, ARF, ROB, branchPredType, LSQ, pipelines, pipelineCount, ROBsize) 
        rsLength = len(self.RS[0].Op) + len(self.RS[1].Op) + len(self.RS[2].Op) 
        if tempStallIndicatorIS == True and instructionFetchCount > 3 and rsLength != 0:
            stallThisCycle = copy.copy(stallThisCycle or True)    

        #for i in range(0, 4) :
            #if(self.IS_EX[i].Empty == False) :
                #print("IS " + str(self.IS_EX[i].InstructionNumber) + "  " + str(self.IS_EX[i].Op) + "  " + str(self.IS_EX[i].D1) + "  " + str(self.IS_EX[i].S1) + "  " + str(self.IS_EX[i].S2))


        return stallThisCycle


    # De-Code next instruction in pipeline
    def decode(self, branchPredType, stallThisCycle, instructionFetchCount, PC, ARF, RAT, ROB, BTB, BIPB, LSQ,ROBsize) :
        needToFlush = False
        flushOutput = -1
        if(self.IF_DE.Empty == False):
            tempStallIndicatorDE, PC, needToFlush, flushOutput = self.decodeUnit.decode(self.IF_DE, self.RS, ARF, RAT, ROB, BIPB, BTB, PC, branchPredType, LSQ, ROBsize)  
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
              