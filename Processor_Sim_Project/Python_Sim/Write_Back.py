from Instruction import Instruction
from Register_File import *
from Reg_To_Reg_Index import *
import copy as copy

class Write_Back_Unit :
    def __init__(self) :
        self.nextInstruction = 0
        self.noWriteBack = ["STR", "STRC", "JMP", "BR", "BLT", "BEQ"]
        return

    def writeBack(self, ROB, ARF) :
        if(len(ROB.Instruction) > 0) :
            for i in range(0, len(ROB.Instruction)) :
                if(ROB.Instruction[i].instructionNumber == self.nextInstruction) :                    
                    if(ROB.Instruction[i].Valid != False) :
                        if(ROB.Value[i] != None) :
                            ARF.Register[regToRegIndex(ROB.Instruction[i].operand1)] = copy.copy(ROB.Value[i])
                    if("r" in str(ROB.Instruction[i].operand1)) :
                        ARF.regInUse[regToRegIndex(ROB.Instruction[i].operand1)] = 0
                    ROB.Instruction.pop(i)
                    ROB.Value.pop(i)
                    self.nextInstruction += 1
                    break

        return ARF