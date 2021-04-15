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
            ROB.CommitPtr = copy.copy((ROB.CommitPtr + 1) % 128)
            

        return 