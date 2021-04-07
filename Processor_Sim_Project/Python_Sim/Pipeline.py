from Instruction import Instruction
from Register_File import *
from Pipeline_Registers import *
from Fetch import Fetch_Unit
from Decode import Decode_Unit
from Execute import *
from Reg_To_Reg_Index import *

class Pipeline:

    def __init__(self) :
        
        self.IF_DE = IF_DE_Reg()                            # Instruction
        self.DE_IS = DE_IS_Reg()                            # Instruction, TargetAddress, Type = 0,1,2,3 (branch, load/store, arithmetic, logic) 
        self.IS_EX = IS_EX_Reg()                            # Instruction, TargetAddress, Type = 0,1,2,3 (branch, load/store, arithmetic, logic) 
        self.EX_WB = EX_WB_Reg()                            # Instruction

        self.fetchUnit = Fetch_Unit()
        self.decodeUnit = Decode_Unit()
        self.EU = [ARITH_Execution_Unit(), ARITH_Execution_Unit(), LDSTR_Execution_Unit(), BRLGC_Execution_Unit()] # 0,1 = ARITHMETIC, 2 = LOAD/STORE, 3 = BRANCH/LOGIC

        self.RS = [ReservationStation(), ReservationStation(), ReservationStation] # 0 = ARITHMETIC, 1 = LOAD/STORE, 2 = BRANCH/LOGIC

    
    def advance(self, PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, ARF, MEM, INSTR, error) :
        # Advance back to front to ensure pipeline can progress
        
        # WRITE BACK (WB) - ROB needed, register re-naming, PRF
        if(self.EX_WB.Empty is False) :
            self.EX_WB.Empty = True

        # EXECUTE (EX) - OoO, multiple cycle operations, all execute every cycle, forwarding output to IS
        for i in range(0,4) :
            if(self.IS_EX.Empty[i] is False) :
                error, PC, finished, branchExecutedCount, branchTakenCount = self.EU[i].executeInstruction(self.IS_EX, i, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount)
                if(error == 1) : #if branch traken, flush pipeline
                    flushCount = self.flush(self.IS_EX.Instruction[i].instructionNumber, flushCount, ARF)
                    error = 0   #reset error for Main to process correctly
                self.IS_EX.Empty[i] = True
                self.EX_WB.Instruction = self.IS_EX.Instruction[i]
                self.EX_WB.Empty = False
                instructionExecuteCount += 1
                break
            
        # ISSUE (IS) - reservation stations needed, dependancies
        if self.DE_IS.Empty is False:
            # Branch / logic (3rd EU)
            if(self.DE_IS.Type == 0 or self.DE_IS.Type == 3) :
                if(self.IS_EX.Empty[3] is True) :
                    self.IS_EX.Instruction[3] = self.DE_IS.Instruction
                    self.IS_EX.Type[3] = self.DE_IS.Type
                    self.IS_EX.TargetAddress[3] = self.DE_IS.TargetAddress
                    self.IS_EX.Empty[3] = False
                    self.DE_IS.Empty = True             
            # Load / Store (2nd EU)
            elif(self.DE_IS.Type == 1) :
                if(self.IS_EX.Empty[2] is True) :
                    self.IS_EX.Instruction[2] = self.DE_IS.Instruction
                    self.IS_EX.Type[2] = self.DE_IS.Type
                    self.IS_EX.Empty[2] = False
                    self.DE_IS.Empty = True   
            # Arithmetic (0th and 1st EU)
            elif(self.DE_IS.Type == 2) :
                if(self.IS_EX.Empty[0] is True) :
                    self.IS_EX.Instruction[0] = self.DE_IS.Instruction
                    self.IS_EX.Type[0] = self.DE_IS.Type
                    self.IS_EX.Empty[0] = False
                    self.DE_IS.Empty = True    
                elif(self.IS_EX.Empty[1] is True) :
                    self.IS_EX.Instruction[1] = self.DE_IS.Instruction
                    self.IS_EX.Type[1] = self.DE_IS.Type
                    self.IS_EX.Empty[1] = False
                    self.DE_IS.Empty = True   
            

        # DECODE (DE) - register re-naming, PRF
        if self.IF_DE.Empty is False and self.DE_IS.Empty is True:
            self.IF_DE, self.DE_IS = self.decodeUnit.decodeInstruction(self.IF_DE, self.DE_IS, ARF)
            self.IF_DE.Empty = True
            self.DE_IS.Empty = False
        # Record stall (only needed once in pipeline)
        elif instructionFetchCount > 1:
            stallCount += 1
        

        # INSTRUCTION FETCH (IF) - DONE
        if self.IF_DE.Empty is True:
            self.IF_DE = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount)
            self.IF_DE.Empty = False
            PC += 1
            instructionFetchCount += 1

        return PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, ARF, MEM, error


    def flush(self, instructionNumber, flushCount, ARF) :
        #remove all instrucions with instructionNumber > than this function's input
        if(self.IF_DE.Instruction.instructionNumber > instructionNumber) :
            self.IF_DE.Empty = True
        if(self.DE_IS.Instruction.instructionNumber > instructionNumber) :
            self.DE_IS.Empty = True
        flushCount += 1
        return flushCount