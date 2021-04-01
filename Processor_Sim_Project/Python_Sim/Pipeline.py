from Instruction import Instruction
from Register_File import RegFile
from Pipeline_Registers import *
from Fetch import Fetch_Unit
from Decode import Decode_Unit
from Execute import Execution_Unit
from Reg_To_Reg_Index import *

class Pipeline:

    def __init__(self) :
        
        self.IF_DE = IF_DE_Reg()                            # Instruction
        self.DE_IS = DE_IS_Reg()                            # Instruction, TargetAddress, Type = 0,1,2,3 (branch, load/store, arithmetic, logic) 
        self.IS_EX = IS_EX_Reg()                            # Instruction, TargetAddress, Type = 0,1,2,3 (branch, load/store, arithmetic, logic) 
        self.EX_WB = EX_WB_Reg()                            # Instruction

        self.fetchUnit = Fetch_Unit()
        self.decodeUnit = Decode_Unit()
        self.EU = [Execution_Unit(0), Execution_Unit(0), Execution_Unit(1), Execution_Unit(2)] # 0,1 = ARITHMETIC, 2 = LOAD/STORE, 3 = BRANCH/LOGIC
    
    def advance(self, PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, RF, MEM, INSTR, error) :
        # Advance back to front to ensure pipeline can progress
        
        # WRITE BACK (WB)
        if(self.EX_WB._empty() is False) :
            # Set reg to not in use, Actual write back occurs in execute
            # 0 = NOT in use,   1 = in use
            if("r" in self.EX_WB._instruction().operand1) :
                RF._inUse(regToRegIndex(self.EX_WB._instruction().operand1), 0)
            if("r" in self.EX_WB._instruction().operand2) :
                RF._inUse(regToRegIndex(self.EX_WB._instruction().operand2), 0)
            if("r" in self.EX_WB._instruction().operand3) :
                RF._inUse(regToRegIndex(self.EX_WB._instruction().operand3), 0)
            self.EX_WB._empty(True)

        # EXECUTE (EX)
        for i in range(0,4) :
            if(self.IS_EX._empty(i) is False) :
                error, PC, finished, branchExecutedCount, branchTakenCount = self.EU[i].executeInstruction(self.IS_EX, i, RF, MEM, PC, finished, branchExecutedCount, branchTakenCount)
                if(error == 1) : #if branch traken, flush pipeline
                    flushCount = self.flush(self.IS_EX._instruction(i).instructionNumber, flushCount, RF)
                    error = 0   #reset error for Main to process correctly
                self.IS_EX._empty(i, True)
                self.EX_WB._instruction(self.IS_EX._instruction(i))
                self.EX_WB._empty(False)
                instructionExecuteCount += 1
                break
            
        # ISSUE (IS)
        if self.DE_IS._empty() is False:
            # Branch / logic (3rd EU)
            if(self.DE_IS._type() == 0 or self.DE_IS._type() == 3) :
                if(self.IS_EX._empty(3) is True) :
                    self.IS_EX._instruction(3, self.DE_IS._instruction())
                    self.IS_EX._type(3, self.DE_IS._type())
                    self.IS_EX._empty(3, False)           
            # Load / Store (2nd EU)
            elif(self.DE_IS._type() == 1) :
                if(self.IS_EX._empty(2) is True) :
                    self.IS_EX._instruction(2, self.DE_IS._instruction())
                    self.IS_EX._type(2, self.DE_IS._type())
                    self.IS_EX._targetAddress(2, self.DE_IS._targetAddress())
                    self.IS_EX._empty(2, False) 
            # Arithmetic (0th and 1st EU)
            elif(self.DE_IS._type() == 2) :
                if(self.IS_EX._empty(0) is True) :
                    self.IS_EX._instruction(0, self.DE_IS._instruction())
                    self.IS_EX._type(0, self.DE_IS._type())
                    self.IS_EX._empty(0, False) 
                elif(self.IS_EX._empty(1) is True) :
                    self.IS_EX._instruction(1, self.DE_IS._instruction())
                    self.IS_EX._type(1, self.DE_IS._type())
                    self.IS_EX._empty(1, False)
            self.DE_IS._empty(True)  

        # DECODE (DE)
        if self.IF_DE._empty() is False and self.DE_IS._empty() is True:
            self.IF_DE, self.DE_IS = self.decodeUnit.decodeInstruction(self.IF_DE, self.DE_IS, RF)
            if(self.decodeUnit._state() == 1) :
                stallCount += 1
            else :
                self.IF_DE._empty(True)
                self.DE_IS._empty(False)
        # Record stall (only needed once in pipeline)
        elif instructionFetchCount > 1:
            stallCount += 1
        

        # INSTRUCTION FETCH (IF)
        if self.IF_DE._empty() is True:
            self.IF_DE = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount)
            self.IF_DE._empty(False)
            PC += 1
            instructionFetchCount += 1

        return PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, RF, MEM, error

    def flush(self, instructionNumber, flushCount, RF) :
        #remove all instrucions with instructionNumber > than this function's input
        if(self.IF_DE._instruction().instructionNumber > instructionNumber) :
            self.IF_DE._empty(True)
        if(self.DE_IS._instruction().instructionNumber > instructionNumber) :
            self.DE_IS._empty(True)
            if("r" in str(self.DE_IS._instruction().operand1)) :
                RF._inUse(regToRegIndex(self.DE_IS._instruction().operand1), 0)
            if("r" in str(self.DE_IS._instruction().operand2)) :
                RF._inUse(regToRegIndex(self.DE_IS._instruction().operand2), 0)
            if("r" in str(self.DE_IS._instruction().operand3)) :
                RF._inUse(regToRegIndex(self.DE_IS._instruction().operand3), 0)
        flushCount += 1
        return flushCount