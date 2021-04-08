from Instruction import Instruction
from Register_File import *
from Pipeline_Registers import *
from Fetch import Fetch_Unit
from Decode import Decode_Unit
from Issue import Issue_Unit
from Execute import *
from Write_Back import Write_Back_Unit
from Reg_To_Reg_Index import *

class Pipeline:

    def __init__(self) :
        
        self.IF_DE = IF_DE_Reg()                                                    # Instruction
        self.RS = [ReservationStation(), ReservationStation(), ReservationStation()]  # 0 = ARITHMETIC, 1 = LOAD/STORE, 2 = BRANCH/LOGIC. Max length of 16 for Arith, 8 for others
        self.IS_EX = IS_EX_Reg()                                                    # Instruction, TargetAddress 
        self.ROB = ReOrderBuffer()                                                  # Instruction, Value


        self.fetchUnit = Fetch_Unit()
        self.decodeUnit = Decode_Unit()
        self.issueUnit = Issue_Unit()
        self.EU = [ARITH_Execution_Unit(), ARITH_Execution_Unit(), LDSTR_Execution_Unit(), BRLGC_Execution_Unit()] # 0,1 = ARITHMETIC, 2 = LOAD/STORE, 3 = BRANCH/LOGIC
        self.writeBackUnit = Write_Back_Unit()


    def advance(self, PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, ARF, MEM, INSTR, error) :
        stallThisCycle = False
        # Advance back to front to ensure pipeline can progress
        
        # WRITE BACK (WB) - register re-naming, PRF
        ARF = self.writeBackUnit.writeBack(self.ROB, ARF)

        # EXECUTE (EX) - OoO, multiple cycle operations, all execute every cycle, forwarding output to IS
        for i in range(0,4) :
            if(self.IS_EX.Empty[i] is False) :
                output = None
                error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output = self.EU[i].executeInstruction(self.IS_EX, i, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount)
                if(error == 1) : # If branch traken, flush pipeline
                    flushCount = self.flush(self.IS_EX.Instruction[i].instructionNumber, flushCount, ARF, instructionFetchCount)
                    error = 0   # Reset error for Main to process correctly
                if(error != 2) :  # If multi-cycle instruction, delay output
                    self.IS_EX.Empty[i] = True
                    self.ROB.Instruction.append(self.IS_EX.Instruction[i])
                    self.ROB.Value.append(output)
                    instructionExecuteCount += 1
                else :
                    error = 0   # Reset error for Main to process correctly
                
            
        # ISSUE (IS) - Proper Dependancy and OoO scheduling
        tempStallIndicator = self.issueUnit.issueInstruction(self.RS, self.IS_EX, ARF, stallThisCycle)
        if tempStallIndicator == True and instructionFetchCount > 2 :
            stallThisCycle = True
         

        # DECODE (DE) - register re-naming, PRF,
        if self.IF_DE.Empty is False :
            stallThisCycle = self.decodeUnit.decodeInstruction(self.IF_DE, self.RS, ARF, stallThisCycle)         
                    

        # INSTRUCTION FETCH (IF) - DONE
        if self.IF_DE.Empty is True and PC < len(INSTR):
            PC, instructionFetchCount = self.fetchUnit.fetchNext(PC, INSTR, self.IF_DE, instructionFetchCount)


        # Increase stall count if stall in pipeline
        if stallThisCycle == True :
            stallCount += 1

        return PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, flushCount, finished, ARF, MEM, error


    def flush(self, instructionNumber, flushCount, ARF, instructionFetchCount) :
        # All instrucions with instructionNumber > than this function's input set to invalid so they are not executed or written back
        if(self.IF_DE.Instruction.instructionNumber > instructionNumber) :
            self.IF_DE.Instruction.Valid = False
        self.RS[0].flush(instructionNumber)
        self.RS[1].flush(instructionNumber)
        self.RS[2].flush(instructionNumber)
        for i in range(0,4) :
            if(self.IS_EX.Instruction[i].instructionNumber > instructionNumber) :
                self.IS_EX.Instruction[i].Valid = False
        flushCount += 1
        return flushCount