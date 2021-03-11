from Instruction import Instruction

class Fetch_Unit :

    def __init__(self) :
        self.stalled = False
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        return

    def fetchNext(self, PC, INSTR, IF_DE, instructionCount, stallCount) :
        nextInstruction = INSTR[PC]
        nextInstruction.instructionNumber = instructionCount
        IF_DE._instruction(nextInstruction)

        # If branch, stall until its executed so know next instruction needed
        if nextInstruction.opCode in self.branchInstructions :
            self.stalled = True 
            stallCount += 1
            
        return IF_DE, stallCount

    def _stalled(self, input=None) :
        if input is not None :
            self.stalled = input
        else :
            return self.stalled