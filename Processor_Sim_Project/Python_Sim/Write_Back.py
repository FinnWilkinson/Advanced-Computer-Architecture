from Instruction import Instruction
from Register_File import *
import copy as copy

class Write_Back_Unit :
    def __init__(self) :
        self.nextInstruction = 0
        self.noWriteBack = ["STR", "STRC", "JMP", "BR", "BLT", "BEQ"]
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT"]
        return

    def writeBack(self, pipelines, pipelineCount, ROB, RAT, ARF, BIPB, ROBsize) :
        toPrint = False
        # If caught up to issue ptr, do nothing
        if(ROB.CommitPtr == ROB.IssuePtr) :
            return toPrint

        # If branch in BIPB that is less than next to commit, wait for it to execute
        for i in range(0, len(BIPB.BranchPC)) :
            if(ROB.InstructionNumber[ROB.CommitPtr] > BIPB.InstructionNumber[i]) :
                return toPrint

        # If read only instruction in place, move to next item in ROB
        if(ROB.Register[ROB.CommitPtr] == "SKIP") :
            # Re-set ROB record
            ROB.Register[ROB.CommitPtr] = copy.copy(" ")
            ROB.InstructionNumber[ROB.CommitPtr] = copy.copy(0)
            ROB.Value[ROB.CommitPtr] = copy.copy(0)
            ROB.Complete[ROB.CommitPtr] = copy.copy(0)
            # Increment Commit Ptr
            ROB.CommitPtr = copy.copy((ROB.CommitPtr + 1) % ROBsize)
            return toPrint

        if(ROB.Register[ROB.CommitPtr] == "PAUSE") :
            toPrint = True
            # Re-set ROB record
            ROB.Register[ROB.CommitPtr] = copy.copy(" ")
            ROB.InstructionNumber[ROB.CommitPtr] = copy.copy(0)
            ROB.Value[ROB.CommitPtr] = copy.copy(0)
            ROB.Complete[ROB.CommitPtr] = copy.copy(0)
            # Increment Commit Ptr
            ROB.CommitPtr = copy.copy((ROB.CommitPtr + 1) % ROBsize)
            return toPrint

        if(ROB.Complete[ROB.CommitPtr] == 1) :
            # Save Value to ARF
            ARF.Register[int(ROB.Register[ROB.CommitPtr][1:])] = copy.copy(ROB.Value[ROB.CommitPtr])
            # Forward value to all reservation stations
            self.forwardVal(pipelines, pipelineCount, ROB)
            # Update RAT if needed
            self.cleanUp(ROB, RAT, ROB.Register[ROB.CommitPtr], ROBsize)
            # Re-set ROB record
            ROB.Register[ROB.CommitPtr] = copy.copy(" ")
            ROB.InstructionNumber[ROB.CommitPtr] = copy.copy(0)
            ROB.Value[ROB.CommitPtr] = copy.copy(0)
            ROB.Complete[ROB.CommitPtr] = copy.copy(0) 
            # Increment Commit Ptr
            ROB.CommitPtr = copy.copy((ROB.CommitPtr + 1) % ROBsize)

        return toPrint


    # Forward value to any waiting instructions in all RS
    def forwardVal(self, pipelines, pipelineCount, ROB) :
        for i in range(0, pipelineCount) :
            # Go through each Reservation Station
            for j in range(0, 3) :
                # Go through each instruction in RS
                for k in range(0, len(pipelines[i].RS[j].Instruction)) :
                    # Check D1
                    if(pipelines[i].RS[j].D1[k] == ("ROB" + str(ROB.CommitPtr)) and pipelines[i].RS[j].Instruction[k].opCode in self.readOnlyINSTR) :
                        pipelines[i].RS[j].D1[k] = copy.copy(ROB.Value[ROB.CommitPtr])
                    # Check V1
                    if(pipelines[i].RS[j].V1[k] == ("ROB" + str(ROB.CommitPtr))) :
                        pipelines[i].RS[j].S1[k] = copy.copy(ROB.Value[ROB.CommitPtr])
                        pipelines[i].RS[j].V1[k] = copy.copy(0)
                    # Check V2
                    if(pipelines[i].RS[j].V2[k] == ("ROB" + str(ROB.CommitPtr))) :
                        pipelines[i].RS[j].S2[k] = copy.copy(ROB.Value[ROB.CommitPtr])
                        pipelines[i].RS[j].V2[k] = copy.copy(0)


    # If last in ROB to write to register, Set RAT address to be "rx"
    def cleanUp(self, ROB, RAT, reg, ROBsize) :
        # Look between CommitPtr and IssuePtr for any other use of reg, if none then reset RAT address
        index = copy.copy(ROB.CommitPtr)
        regCount = 0
        while True :
            if(index == ROB.IssuePtr) :
                break
            if(ROB.Register[index] == reg) :
                regCount += 1
            index = copy.copy((index + 1) % ROBsize)

        # If last of instruction to that register
        if(regCount == 1) :
            # update RAT
            RAT.Address[int(reg[1:])] = copy.copy(reg)
            

    # commit items in LSQ in order
    def LSQCommit(self, LSQ, MEM, BIPB) :
        # If caught up to issue ptr, do nothing
        if(LSQ.CommitPtr == LSQ.IssuePtr) :
            return

        # If branch in BIPB that is less than next to commit, wait for it to execute
        for i in range(0, len(BIPB.BranchPC)) :
            if(LSQ.InstructionNumber[LSQ.CommitPtr] > BIPB.InstructionNumber[i]) :
                return

        # If item completed, write to memory
        if(LSQ.Complete[LSQ.CommitPtr] == 1) :
            # Only write value to memory if it's a store
            if(LSQ.InstructionType[LSQ.CommitPtr] == "STORE") :
                MEM[LSQ.Address[LSQ.CommitPtr]] = copy.copy(LSQ.Value[LSQ.CommitPtr])
            # Re-set LSQ record
            LSQ.InstructionType[LSQ.CommitPtr] = copy.copy(" ")
            LSQ.InstructionNumber[LSQ.CommitPtr] = copy.copy(0)
            LSQ.Address[LSQ.CommitPtr] = copy.copy(-1)
            LSQ.Value[LSQ.CommitPtr] = copy.copy(0)
            LSQ.Complete[LSQ.CommitPtr] = copy.copy(0)
            # Increment commit ptr
            LSQ.CommitPtr = copy.copy((LSQ.CommitPtr + 1) % 128)