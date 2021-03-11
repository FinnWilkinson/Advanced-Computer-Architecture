from Instruction import Instruction

class Fetch_Unit :

    def __init__(self) :
        return

    def fetchNext(self, INSTR, instructionCount, cycles, PC) :
        nextInstruction = INSTR[PC]
        nextInstruction.instructionNumber = instructionCount

        instructionCount += 1
        cycles += 1
        PC += 1

        return nextInstruction, instructionCount, cycles, PC
