from Instruction import Instruction
from Register_File import *
from Reg_To_Reg_Index import *

# ARITHMETIC EXECUTION UNIT
class ARITH_Execution_Unit :
    def __init__(self) :
        self.ExecutionCount = 0
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount) :
        output = None
        error = 0

        # ADD
        if IS_EX[EUindex].Op == "ADD": 
            output = IS_EX[EUindex].S1 + IS_EX[EUindex].S2
        # ADDI
        elif IS_EX[EUindex].Op == "ADDI": 
            output = IS_EX[EUindex].S1 + IS_EX[EUindex].S2
        # SUB
        elif IS_EX[EUindex].Op == "SUB": 
            output = IS_EX[EUindex].S1 - IS_EX[EUindex].S2
        # SUBI
        elif IS_EX[EUindex].Op == "SUBI": 
            output = IS_EX[EUindex].S1 - IS_EX[EUindex].S2
        # MUL
        elif IS_EX[EUindex].Op == "MUL": 
            # Introduce 3 cycle latency for Multiplication
            if(self.ExecutionCount == 2) :
                output = IS_EX[EUindex].S1 * IS_EX[EUindex].S2
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # MULI
        elif IS_EX[EUindex].Op == "MULI": 
            # Introduce 3 cycle latency for Multiplication
            if(self.ExecutionCount == 2) :
                output = IS_EX[EUindex].S1 * IS_EX[EUindex].S2
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # DIV
        elif IS_EX[EUindex].Op == "DIV": 
            # Introduce 16 cycle latency for Division
            if(self.ExecutionCount == 15) :
                output = IS_EX[EUindex].S1 / IS_EX[EUindex].S2
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # DIVI
        elif IS_EX[EUindex].Op == "DIVI": 
            # Introduce 16 cycle latency for Division
            if(self.ExecutionCount == 15) :
                output = IS_EX[EUindex].S1 / IS_EX[EUindex].S2
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
            error = -1
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output


# LOAD / STORE EXECUTION UNIT
class LDSTR_Execution_Unit :
    def __init__(self) :
        self.ExecutionCount = 0
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount) :
        output = None
        error = 0

        # Introduce 2 cycle latency for Load and Stores (Replicating L1 cache latency)
        if(self.ExecutionCount == 1) :
            # LD
            if IS_EX[EUindex].Op == "LD": 
                output = MEM[IS_EX[EUindex].S1 + IS_EX[EUindex].S2]
            # LDC
            elif IS_EX[EUindex].Op == "LDC": 
                output = MEM[IS_EX[EUindex].S1 + IS_EX[EUindex].S2]
            # STR
            elif IS_EX[EUindex].Op == "STR": 
                MEM[IS_EX[EUindex].S1 + IS_EX[EUindex].S2] = IS_EX[EUindex].D1
            # STRC
            elif IS_EX[EUindex].Op == "STRC":
                MEM[IS_EX[EUindex].S1 + IS_EX[EUindex].S2] = IS_EX[EUindex].D1
            # Opcode not recognised
            else: 
                print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
                error = -1
            self.ExecutionCount = 0     # Re-set execution count
        else :
            self.ExecutionCount += 1
            error = 2   # Cycle delay occured
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output


# BRANCH / LOGIC EXECUTION UNIT
class BRLGC_Execution_Unit :
    def __init__(self) :
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount) :
        output = None
        error = 0
        targetAddress = IS_EX[EUindex].TargetAddress

        # HALT
        if IS_EX[EUindex].Op == "HALT":                                                     
            finished = True
        # CMP
        elif IS_EX[EUindex].Op == "CMP": 
            if(IS_EX[EUindex].S1 > IS_EX[EUindex].S2) :
                output = 1
            elif(IS_EX[EUindex].S1 == IS_EX[EUindex].S2) :
                output = 0
            elif(IS_EX[EUindex].S1 < IS_EX[EUindex].S2) :
                output = -1
        # JMP
        elif IS_EX[EUindex].Op == "JMP": 
            branchExecutedCount += 1
            branchTakenCount += 1
            PC = IS_EX[EUindex].D1
            error = 1   # Flush pipeline
        # BR
        elif IS_EX[EUindex].Op == "BR": 
            branchExecutedCount += 1
            branchTakenCount += 1
            PC = IS_EX[EUindex].D1
            error = 1   # Flush pipeline
        # BEQ
        elif IS_EX[EUindex].Op == "BEQ": 
            branchExecutedCount += 1
            if(IS_EX[EUindex].D1 == IS_EX[EUindex].S1) :
                PC = IS_EX[EUindex].S2
                branchTakenCount += 1
                error = 1   # Flush pipeline
        # BLT
        elif IS_EX[EUindex].Op == "BLT": 
            branchExecutedCount += 1
            if(IS_EX[EUindex].D1 < IS_EX[EUindex].S1) :
                PC = IS_EX[EUindex].S2
                branchTakenCount += 1
                error = 1   # Flush pipeline
        #LSL
        elif IS_EX[EUindex].Op == "LSL":
            output = IS_EX[EUindex].S1 << IS_EX[EUindex].S2
        #LSR
        elif IS_EX[EUindex].Op == "LSR":
            output = IS_EX[EUindex].S1 >> IS_EX[EUindex].S2
        #XOR
        elif IS_EX[EUindex].Op == "XOR" :
            output = IS_EX[EUindex].S1 ^ IS_EX[EUindex].S2
        #AND
        elif IS_EX[EUindex].Op == "AND" :
            output = IS_EX[EUindex].S1 & IS_EX[EUindex].S2
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
            error = -1
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output