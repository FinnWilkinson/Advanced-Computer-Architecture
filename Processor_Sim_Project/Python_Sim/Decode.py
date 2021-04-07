from Instruction import Instruction
from Register_File import *
from Reg_To_Reg_Index import *

# Instructions:
# HALT = 0, ADD = 1, ADDI = 2, SUB = 3, SUBI = 4, MUL = 5, MULI = 6, DIV = 7, DIVI = 8, LD = 9,
# LDC = 10, STR = 11, STRC = 12, CMP = 13, JMP = 14, BR = 15, BEQ = 16, BLT = 17, LSL = 18, LSR = 19
# XOR = 20, AND = 21

class Decode_Unit :

    def __init__(self) :
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.loadStoreInstructions = ["LD", "LDC", "STR", "STRC"]
        self.logicInstructions = ["HALT", "LSL", "LSR", "AND", "XOR"]

    def decodeInstruction(self, IF_DE, DE_IS, ARF) :
        # Get instruction Type = 0,1,2,3 (branch, load/store, arithmetic, logic)
        # Calc. target address

        nextInstruction = IF_DE.Instruction

        if nextInstruction.opCode in self.branchInstructions :
            DE_IS.Type = 0
        elif nextInstruction.opCode in self.loadStoreInstructions :
            DE_IS.Type = 1
        elif nextInstruction.opCode in self.logicInstructions :
            DE_IS.Type = 3
        else :
            DE_IS.Type = 2

        DE_IS.Instruction = nextInstruction
        DE_IS.TargetAddress = (IF_DE.TargetAddress)
    
        return IF_DE, DE_IS
        


    