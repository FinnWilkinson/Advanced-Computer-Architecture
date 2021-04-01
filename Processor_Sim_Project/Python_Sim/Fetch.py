from Instruction import Instruction

class Fetch_Unit :

    def __init__(self) :
        return

    def fetchNext(self, PC, INSTR, IF_DE, instructionCount) :
        nextInstruction = INSTR[PC]
        nextInstruction.instructionNumber = instructionCount
        IF_DE._instruction(nextInstruction)
            
        return IF_DE