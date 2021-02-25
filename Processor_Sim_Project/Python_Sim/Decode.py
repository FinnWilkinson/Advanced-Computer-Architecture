from Instruction import Instruction

# Instructions:
# HALT = 0, ADD = 1, ADDI = 2, SUB = 3, SUBI = 4, MUL = 5, MULI = 6, DIV = 7, DIVI = 8, LD = 9,
# LDC = 10, STR = 11, STRC = 12, CMP = 13, JMP = 14, BR = 15, BEQ = 16, BLT = 17

def decodeInstruction(RF, cycles, currentInstruction) :
    targetAddress = 0 
    #calculate target address for load or store
    if currentInstruction.opCode == 9 :
        targetAddress = RF[currentInstruction.operand2] + currentInstruction.operand3
    elif currentInstruction.opCode == 10 :
        targetAddress = currentInstruction.operand2
    elif currentInstruction.opCode == 11 :
        targetAddress = RF[currentInstruction.operand2] + currentInstruction.operand3
    elif currentInstruction.opCode == 12 :
        targetAddress = currentInstruction.operand2

    cycles += 1
    return targetAddress
    