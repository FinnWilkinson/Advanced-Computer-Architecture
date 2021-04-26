from Instruction import Instruction
from Register_File import *
import copy as copy

class Write_Back_Unit :
    def __init__(self) :
        self.nextInstruction = 0
        self.noWriteBack = ["STR", "STRC", "JMP", "BR", "BLT", "BEQ"]
        return

    def writeBack(self, ROB, RAT, ARF, BIPB) :
        # If caught up to issue ptr, do nothing
        if(ROB.IssuePtr == ROB.CommitPtr) :
            return

        # If branch in BIPB that is less than next to commit, wait for it to execute
        for i in range(0, len(BIPB.BranchPC)) :
            if(ROB.InstructionNumber[ROB.CommitPtr] == BIPB.InstructionNumber[i]) :
                return

        # If read only instruction in place, move to next item in ROB
        if(ROB.Register[ROB.CommitPtr] == "SKIP") :
            ROB.CommitPtr = copy.copy((ROB.CommitPtr + 1) % 256)
            return

        if(ROB.Complete[ROB.CommitPtr] == 1) :
            ARF.Register[int(ROB.Register[ROB.CommitPtr][1:])] = copy.copy(ROB.Value[ROB.CommitPtr])
            self.cleanUp(ROB, RAT, ROB.Register[ROB.CommitPtr]) 
            ROB.Register[ROB.CommitPtr] = "SKIP"
            ROB.CommitPtr = copy.copy((ROB.CommitPtr + 1) % 256)

        return 

    # If last in ROB to write to register, Set RAT address to be "rx"
    def cleanUp(self, ROB, RAT, reg) :
        # Look between CommitPtr and IssuePtr for any other use of reg, if none then reset RAT address
        index = copy.copy(ROB.CommitPtr)
        regCount = 0
        while True :
            if(index == ROB.IssuePtr) :
                break
            if(ROB.Register[index] == reg) :
                regCount += 1
            index = copy.copy((index + 1) % 256)

        if(regCount == 1) :
            RAT.Address[int(reg[1:])] = reg

    
    # commit items in LSQ in order
    def LSQCommit(self, LSQ, MEM, BIPB) :
        # If caught up to issue ptr, do nothing
        if(LSQ.IssuePtr == LSQ.CommitPtr) :
            return

        # If branch in BIPB that is less than next to commit, wait for it to execute
        for i in range(0, len(BIPB.BranchPC)) :
            if(LSQ.InstructionNumber[LSQ.CommitPtr] > BIPB.InstructionNumber[i]) :
                return

        if(LSQ.Complete[LSQ.CommitPtr] == 1) :
            if(LSQ.InstructionType[LSQ.CommitPtr] == "STORE") :
                MEM[LSQ.Address[LSQ.CommitPtr]] = copy.copy(LSQ.Value[LSQ.CommitPtr])
            LSQ.InstructionType[LSQ.CommitPtr] = " "
            LSQ.InstructionNumber[LSQ.CommitPtr] = 0
            LSQ.Address[LSQ.CommitPtr] = 0
            LSQ.Value[LSQ.CommitPtr] = 0
            LSQ.Complete[LSQ.CommitPtr] = 0
            LSQ.CommitPtr = copy.copy((LSQ.CommitPtr + 1) % 128)

        return