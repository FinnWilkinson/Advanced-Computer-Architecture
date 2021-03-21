from Instruction import Instruction
from Register_File import RegFile
from IF_DE_Reg import IF_DE_Reg
from DE_EX_Reg import DE_EX_Reg
from Fetch import Fetch_Unit
from Decode import Decode_Unit
from Execute import Execution_Unit

class Pipeline:

    def __init__(self) :
        
        self.IF_DE = IF_DE_Reg()                            # Instruction
        self.DE_EX = DE_EX_Reg()                            # Instruction, TargetAddress, Type = 0,1,2 (branch, load/store, arithmetic) 

        self.fetchUnit = Fetch_Unit()
        self.decodeUnit = Decode_Unit()
        self.EU = Execution_Unit()
    
    def advance(self, PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, finished, RF, MEM, INSTR, error) :
        # Advance back to front to ensure pipeline can progress
        
        # EX
        if self.DE_EX._empty() is False :
            error, PC, finished, branchExecutedCount, branchTakenCount = self.EU.executeInstruction(self.DE_EX, RF, MEM, PC, finished, branchExecutedCount, branchTakenCount)
            if self.DE_EX._type() == 0 :
                self.fetchUnit._stalled(False)
            self.DE_EX._empty(True)
            instructionExecuteCount += 1

        # DE
        if self.IF_DE._empty() is False and self.DE_EX._empty() is True:
            self.IF_DE, self.DE_EX = self.decodeUnit.decodeInstruction(self.IF_DE, self.DE_EX, RF)
            self.IF_DE._empty(True)
            self.DE_EX._empty(False)

        # IF
        if self.IF_DE._empty() is True and self.fetchUnit._stalled() is False :
            self.IF_DE, stallCount = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount, stallCount)
            self.IF_DE._empty(False)
            PC += 1
            instructionFetchCount += 1

        return PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, finished, RF, MEM, error