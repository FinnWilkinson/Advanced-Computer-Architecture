from Instruction import Instruction
from Register_File import *
from Reg_To_Reg_Index import *
import copy as copy

class Write_Back_Unit :
    def __init__(self) :
        self.nextInstruction = 0
        self.noWriteBack = ["STR", "STRC", "JMP", "BR", "BLT", "BEQ"]
        return

    def writeBack(self, ROB, RAT, ARF) :
        # If read only instruction in place, move to next item in ROB
        if(ROB.Register[ROB.CommitPtr] == "SKIP") :
            ROB.CommitPtr = copy.copy((ROB.CommitPtr + 1) % 128)
            return

        if(ROB.Complete[ROB.CommitPtr] == 1) :
            ARF.Register[int(ROB.Register[ROB.CommitPtr][1:])] = copy.copy(ROB.Value[ROB.CommitPtr])
            self.cleanUp(ROB, RAT, ROB.Register[ROB.CommitPtr]) 
            ROB.CommitPtr = copy.copy((ROB.CommitPtr + 1) % 128)

        return 

    # If last in ROB to write to register, Set RAT address to be "rx"
    def cleanUp(self, ROB, RAT, reg) :
        # Look between CommitPtr and IssuePtr for any other use of reg, if none then reset RAT address
        index = copy.copy(ROB.CommitPtr)
        regCount = 0
        while True :
            if(ROB.Register[index] == reg) :
                regCount += 1
            if(index == ROB.IssuePtr) :
                break
            index = copy.copy((index + 1) % 128)

        if(regCount == 1) :
            RAT.Address[int(reg[1:])] = reg