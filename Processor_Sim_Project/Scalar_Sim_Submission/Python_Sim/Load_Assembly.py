import sys
from Instruction import Instruction

# Line length constant for reading assembly lines from text file
LINE_LEN = 256

# Instructions:
# HALT = 0, ADD = 1, ADDI = 2, SUB = 3, SUBI = 4, MUL = 5, MULI = 6, DIV = 7, DIVI = 8, LD = 9,
# LDC = 10, STR = 11, STRC = 12, CMP = 13, JMP = 14, BR = 15, BEQ = 16, BLT = 17


# Registers. int corresponding value ==> rx = int(x)    i.e. r13 = 13
# r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, 
# r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31

# Load specified assembly program
# Igrnores any lines beginning with '//' in the input program
def loadProgram(filename, INSTR) :
    instructionCount = 0
    # Open file
    programFile = open(filename, 'r')
    if(programFile == None) :
        print("ERROR - File '%s' not found.\n", filename)
        sys.exit(1)

    while True :
        line = programFile.readline()
        # Stop the loop at end of file
        if not line :
            break

        words = line.split(' ')
        # Remove comments
        if '//' in words[0] :
            continue
        # Remove commas and line endings
        for i in range(1, len(words)) :
            words[i] = words[i][:-1]

        newOpcode = words[0]
        newOperands = ['0'] * 3
        for i in range(1, len(words)) :
            newOperands[i-1] = words[i]

        INSTR[instructionCount] = Instruction(opcodeSTRtoENUM(newOpcode), operandSTRtoENUM(newOperands[0]), operandSTRtoENUM(newOperands[1]), operandSTRtoENUM(newOperands[2]), 0)
        instructionCount += 1

    programFile.close()
        

# Convert between instruction string read from file and enum version
def opcodeSTRtoENUM(opcode) :
    if(opcode == "HALT") :
        return 0
    elif(opcode == "ADD") :
        return 1
    elif(opcode == "ADDI") :
        return 2
    elif(opcode == "SUB") :
        return 3
    elif(opcode == "SUBI") :
        return 4
    elif(opcode == "MUL") :
        return 5
    elif(opcode == "MULI") :
        return 6
    elif(opcode == "DIV") :
        return 7
    elif(opcode == "DIVI") :
        return 8
    elif(opcode == "LD") :
        return 9
    elif(opcode == "LDC") :
        return 10
    elif(opcode == "STR") :
        return 11
    elif(opcode == "STRC") :
        return 12
    elif(opcode == "CMP") :
        return 13
    elif(opcode == "JMP") :
        return 14
    elif(opcode == "BR") :
        return 15
    elif(opcode == "BEQ") :
        return 16
    elif(opcode == "BLT") :
        return 17
    return -1

# Converts operand into associated register enum index, or the directly to an int if an immediate operand
def operandSTRtoENUM(operand) :
    if(operand == "r0") :
        return 0
    elif(operand == "r1") :
        return 1
    elif(operand == "r2") :
        return 2
    elif(operand == "r3") :
        return 3
    elif(operand == "r4") :
        return 4
    elif(operand == "r5") :
        return 5
    elif(operand == "r6") :
        return 6
    elif(operand == "r7") :
        return 7
    elif(operand == "r8") :
        return 8
    elif(operand == "r9") :
        return 9
    elif(operand == "r10") :
        return 10
    elif(operand == "r11") :
        return 11
    elif(operand == "r12") :
        return 12
    elif(operand == "r13") :
        return 13
    elif(operand == "r14") :
        return 14
    elif(operand == "r15") :
        return 15
    elif(operand == "r16") :
        return 16
    elif(operand == "r17") :
        return 17
    elif(operand == "r18") :
        return 18
    elif(operand == "r19") :
        return 19
    elif(operand == "r20") :
        return 20
    elif(operand == "r21") :
        return 21
    elif(operand == "r22") :
        return 22
    elif(operand == "r23") :
        return 23
    elif(operand == "r24") :
        return 24
    elif(operand == "r25") :
        return 25
    elif(operand == "r26") :
        return 26
    elif(operand == "r27") :
        return 27
    elif(operand == "r28") :
        return 28
    elif(operand == "r29") :
        return 29
    elif(operand == "r30") :
        return 30
    elif(operand == "r31") :
        return 31

    # Defualt being convert the string to int
    return int(operand)