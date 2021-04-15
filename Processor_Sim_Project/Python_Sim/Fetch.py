from Instruction import Instruction
import copy as copy

class Fetch_Unit :

    def __init__(self) :
        return

    def fetchNext(self, PC, INSTR, IF_DE, instructionFetchCount) :
        nextInstruction = INSTR[PC]

        # Stops program crashes due to unknown opcode after end of program
        if nextInstruction.opCode == 0 :
            IF_DE.Empty = True
            return PC, instructionFetchCount

        nextInstruction.instructionNumber = instructionFetchCount
        nextInstruction.Valid = True
        IF_DE.Instruction = copy.copy(nextInstruction)

        # Branch prediction target address
        IF_DE.TargetAddress = 0

        IF_DE.Empty = False
        PC += 1
        instructionFetchCount += 1
            
        return PC, instructionFetchCount