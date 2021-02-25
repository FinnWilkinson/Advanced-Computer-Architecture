from Instruction import Instruction

def fetchNext(INSTR, instructionCount, cycles, PC) :
    nextInstruction = INSTR[PC]
    nextInstruction.instructionNumber = instructionCount

    instructionCount += 1
    cycles += 1
    PC += 1

    return nextInstruction, instructionCount, cycles, PC
