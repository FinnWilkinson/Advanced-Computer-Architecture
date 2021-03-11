from Instruction import Instruction
from Register_File import RegFile

# Instructions:
# HALT = 0, ADD = 1, ADDI = 2, SUB = 3, SUBI = 4, MUL = 5, MULI = 6, DIV = 7, DIVI = 8, LD = 9,
# LDC = 10, STR = 11, STRC = 12, CMP = 13, JMP = 14, BR = 15, BEQ = 16, BLT = 17

class Decode_Unit :

    def __init__(self) :
            return

    def decodeInstruction(self, RF, cycles, currentInstruction) :
        targetAddress = 0 
        #calculate target address for load or store
        if currentInstruction.opCode == "LD" :
            targetAddress = RF.Get(currentInstruction.operand2) + int(currentInstruction.operand3)
        elif currentInstruction.opCode == "LDC" :
            targetAddress = int(currentInstruction.operand2)
        elif currentInstruction.opCode == "STR" :
            targetAddress = RF.Get(currentInstruction.operand2) + int(currentInstruction.operand3)
        elif currentInstruction.opCode == "STRC" :
            targetAddress = int(currentInstruction.operand2)

        cycles += 1
        return targetAddress, cycles
        