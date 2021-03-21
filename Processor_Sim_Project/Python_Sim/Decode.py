from Instruction import Instruction
from Register_File import RegFile

# Instructions:
# HALT = 0, ADD = 1, ADDI = 2, SUB = 3, SUBI = 4, MUL = 5, MULI = 6, DIV = 7, DIVI = 8, LD = 9,
# LDC = 10, STR = 11, STRC = 12, CMP = 13, JMP = 14, BR = 15, BEQ = 16, BLT = 17, LSL = 18, LSR = 19

class Decode_Unit :

    def __init__(self) :
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.loadStoreInstructions = ["LD", "LDC", "STR", "STRC"]


    def decodeInstruction(self, IF_DE, DE_EX, RF) :
        # Get instruction Type = 0,1,2 (branch, load/store, arithmetic)
        # Calc. target address


        nextInstruction = IF_DE._instruction()
        if nextInstruction.opCode in self.branchInstructions :
            DE_EX._type(0)
        elif nextInstruction.opCode in self.loadStoreInstructions :
            DE_EX._type(1)
        else :
            DE_EX._type(2)

        if DE_EX._type() == 1 :
            targetAddress = 0 
            if nextInstruction.opCode == "LD" or nextInstruction.opCode == "STR" :
                targetAddress = RF.Get(nextInstruction.operand2) + RF.Get(nextInstruction.operand3)
            elif nextInstruction.opCode == "LDC" or nextInstruction.opCode == "STRC" :
                targetAddress = RF.Get(nextInstruction.operand2) + int(nextInstruction.operand3)
            
            DE_EX._targetAddress(targetAddress)

        DE_EX._instruction(IF_DE._instruction())

        return IF_DE, DE_EX
        