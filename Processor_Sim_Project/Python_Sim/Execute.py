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
        currentInstruction = IS_EX.Instruction[EUindex]
        # Invalid due to branch mispredict
        if currentInstruction.Valid == False :
            return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output

        # ADD
        if IS_EX.Op[EUindex] == "ADD": 
            output = IS_EX.S1[EUindex] + IS_EX.S2[EUindex]
        # ADDI
        elif IS_EX.Op[EUindex] == "ADDI": 
            output = IS_EX.S1[EUindex] + IS_EX.S2[EUindex]
        # SUB
        elif IS_EX.Op[EUindex] == "SUB": 
            output = IS_EX.S1[EUindex] - IS_EX.S2[EUindex]
        # SUBI
        elif IS_EX.Op[EUindex] == "SUBI": 
            output = IS_EX.S1[EUindex] - IS_EX.S2[EUindex]
        # MUL
        elif IS_EX.Op[EUindex] == "MUL": 
            # Introduce 3 cycle latency for Multiplication
            if(self.ExecutionCount == 2) :
                output = IS_EX.S1[EUindex] * IS_EX.S2[EUindex]
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # MULI
        elif IS_EX.Op[EUindex] == "MULI": 
            # Introduce 3 cycle latency for Multiplication
            if(self.ExecutionCount == 2) :
                output = IS_EX.S1[EUindex] * IS_EX.S2[EUindex]
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # DIV
        elif IS_EX.Op[EUindex] == "DIV": 
            # Introduce 16 cycle latency for Division
            if(self.ExecutionCount == 15) :
                output = IS_EX.S1[EUindex] / IS_EX.S2[EUindex]
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # DIVI
        elif IS_EX.Op[EUindex] == "DIVI": 
            # Introduce 16 cycle latency for Division
            if(self.ExecutionCount == 15) :
                output = IS_EX.S1[EUindex] / IS_EX.S2[EUindex]
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # # ADD
        # if currentInstruction.opCode == "ADD": 
        #     output = ARF.Register[regToRegIndex(currentInstruction.operand2)] + ARF.Register[regToRegIndex(currentInstruction.operand3)]
        # # ADDI
        # elif currentInstruction.opCode == "ADDI": 
        #     output = ARF.Register[regToRegIndex(currentInstruction.operand2)] + int(currentInstruction.operand3)
        # # SUB
        # elif currentInstruction.opCode == "SUB": 
        #     output = ARF.Register[regToRegIndex(currentInstruction.operand2)] - ARF.Register[regToRegIndex(currentInstruction.operand3)]
        # # SUBI
        # elif currentInstruction.opCode == "SUBI": 
        #     output = ARF.Register[regToRegIndex(currentInstruction.operand2)] - int(currentInstruction.operand3)
        # # MUL
        # elif currentInstruction.opCode == "MUL": 
        #     # Introduce 3 cycle latency for Multiplication
        #     if(self.ExecutionCount == 2) :
        #         output = ARF.Register[regToRegIndex(currentInstruction.operand2)] * ARF.Register[regToRegIndex(currentInstruction.operand3)]
        #         self.ExecutionCount = 0     # Re-set execution count
        #     else :
        #         error = 2       # Cycle delay occured
        #         self.ExecutionCount += 1
        # # MULI
        # elif currentInstruction.opCode == "MULI": 
        #     # Introduce 3 cycle latency for Multiplication
        #     if(self.ExecutionCount == 2) :
        #         output = ARF.Register[regToRegIndex(currentInstruction.operand2)] * int(currentInstruction.operand3)
        #         self.ExecutionCount = 0     # Re-set execution count
        #     else :
        #         error = 2       # Cycle delay occured
        #         self.ExecutionCount += 1
        # # DIV
        # elif currentInstruction.opCode == "DIV": 
        #     # Introduce 16 cycle latency for Division
        #     if(self.ExecutionCount == 15) :
        #         output = ARF.Register[regToRegIndex(currentInstruction.operand2)] / ARF.Register[regToRegIndex(currentInstruction.operand3)]
        #         self.ExecutionCount = 0     # Re-set execution count
        #     else :
        #         error = 2       # Cycle delay occured
        #         self.ExecutionCount += 1
        # # DIVI
        # elif currentInstruction.opCode == "DIVI": 
        #     # Introduce 16 cycle latency for Division
        #     if(self.ExecutionCount == 15) :
        #         output = ARF.Register[regToRegIndex(currentInstruction.operand2)] / int(currentInstruction.operand3)
        #         self.ExecutionCount = 0     # Re-set execution count
        #     else :
        #         error = 2       # Cycle delay occured
        #         self.ExecutionCount += 1
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
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
        currentInstruction = IS_EX.Instruction[EUindex]
        # Invalid due to branch mispredict
        if currentInstruction.Valid == False :
            return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output
        
        # Introduce 2 cycle latency for Load and Stores (Replicating L1 cache latency)
        if(self.ExecutionCount == 1) :
            # LD
            if IS_EX.Op[EUindex] == "LD": 
                output = MEM[IS_EX.S1[EUindex] + IS_EX.S2[EUindex]]
            # LDC
            elif IS_EX.Op[EUindex] == "LDC": 
                output = MEM[IS_EX.S1[EUindex] + IS_EX.S2[EUindex]]
            # STR
            elif IS_EX.Op[EUindex] == "STR": 
                MEM[IS_EX.S1[EUindex] + IS_EX.S2[EUindex]] = IS_EX.D1[EUindex]
            # STRC
            elif IS_EX.Op[EUindex] == "STRC":
                MEM[IS_EX.S1[EUindex] + IS_EX.S2[EUindex]] = IS_EX.D1[EUindex]

            # # LD
            # if currentInstruction.opCode == "LD": 
            #     output = MEM[ARF.Register[regToRegIndex(currentInstruction.operand2)] + ARF.Register[regToRegIndex(currentInstruction.operand3)]]
            # # LDC
            # elif currentInstruction.opCode == "LDC": 
            #     output = MEM[ARF.Register[regToRegIndex(currentInstruction.operand2)] + int(currentInstruction.operand3)]
            # # STR
            # elif currentInstruction.opCode == "STR": 
            #     MEM[ARF.Register[regToRegIndex(currentInstruction.operand2)] + ARF.Register[regToRegIndex(currentInstruction.operand3)]] = ARF.Register[regToRegIndex(currentInstruction.operand1)]
            # # STRC
            # elif currentInstruction.opCode == "STRC":
            #     MEM[ARF.Register[regToRegIndex(currentInstruction.operand2)] + int(currentInstruction.operand3)] = ARF.Register[regToRegIndex(currentInstruction.operand1)]
            # Opcode not recognised
            else: 
                print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
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
        currentInstruction = IS_EX.Instruction[EUindex]
        targetAddress = IS_EX.TargetAddress[EUindex]
        # Invalid due to branch mispredict
        if currentInstruction.Valid == False :
            return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output

        # HALT
        if IS_EX.Op[EUindex] == "HALT":                                                     
            finished = True
        # CMP
        elif IS_EX.Op[EUindex] == "CMP": 
            if(IS_EX.S1[EUindex] > IS_EX.S2[EUindex]) :
                output = 1
            elif(IS_EX.S1[EUindex] == IS_EX.S2[EUindex]) :
                output = 0
            elif(IS_EX.S1[EUindex] < IS_EX.S2[EUindex]) :
                output = -1
        # JMP
        elif IS_EX.Op[EUindex] == "JMP": 
            branchExecutedCount += 1
            branchTakenCount += 1
            PC = IS_EX.D1[EUindex]
            error = 1   # Flush pipeline
        # BR
        elif IS_EX.Op[EUindex] == "BR": 
            branchExecutedCount += 1
            branchTakenCount += 1
            PC = IS_EX.D1[EUindex]
            error = 1   # Flush pipeline
        # BEQ
        elif IS_EX.Op[EUindex] == "BEQ": 
            branchExecutedCount += 1
            if(IS_EX.D1[EUindex] == IS_EX.S1[EUindex]) :
                PC = IS_EX.S2[EUindex]
                branchTakenCount += 1
                error = 1   # Flush pipeline
        # BLT
        elif IS_EX.Op[EUindex] == "BLT": 
            branchExecutedCount += 1
            if(IS_EX.D1[EUindex] < IS_EX.S1[EUindex]) :
                PC = IS_EX.S2[EUindex]
                branchTakenCount += 1
                error = 1   # Flush pipeline
        #LSL
        elif IS_EX.Op[EUindex] == "LSL":
            output = IS_EX.S1[EUindex] << IS_EX.S2[EUindex]
        #LSR
        elif IS_EX.Op[EUindex] == "LSR":
            output = IS_EX.S1[EUindex] >> IS_EX.S2[EUindex]
        #XOR
        elif IS_EX.Op[EUindex] == "XOR" :
            output = IS_EX.S1[EUindex] ^ IS_EX.S2[EUindex]
        #AND
        elif IS_EX.Op[EUindex] == "AND" :
            output = IS_EX.S1[EUindex] & IS_EX.S2[EUindex]

        # # HALT
        # if currentInstruction.opCode == "HALT":                                                     
        #     finished = True
        # # CMP
        # elif currentInstruction.opCode == "CMP": 
        #     if(ARF.Register[regToRegIndex(currentInstruction.operand2)] > ARF.Register[regToRegIndex(currentInstruction.operand3)]) :
        #         output = 1
        #     elif(ARF.Register[regToRegIndex(currentInstruction.operand2)] == ARF.Register[regToRegIndex(currentInstruction.operand3)]) :
        #         output = 0
        #     elif(ARF.Register[regToRegIndex(currentInstruction.operand2)] < ARF.Register[regToRegIndex(currentInstruction.operand3)]) :
        #         output = -1
        # # JMP
        # elif currentInstruction.opCode == "JMP": 
        #     branchExecutedCount += 1
        #     branchTakenCount += 1
        #     PC = ARF.Register[regToRegIndex(currentInstruction.operand1)]
        #     error = 1   # Flush pipeline
        # # BR
        # elif currentInstruction.opCode == "BR": 
        #     branchExecutedCount += 1
        #     branchTakenCount += 1
        #     PC = int(currentInstruction.operand1)
        #     error = 1   # Flush pipeline
        # # BEQ
        # elif currentInstruction.opCode == "BEQ": 
        #     branchExecutedCount += 1
        #     if(ARF.Register[regToRegIndex(currentInstruction.operand1)] == ARF.Register[regToRegIndex(currentInstruction.operand2)]) :
        #         PC = int(currentInstruction.operand3)
        #         branchTakenCount += 1
        #         error = 1   # Flush pipeline
        # # BLT
        # elif currentInstruction.opCode == "BLT": 
        #     branchExecutedCount += 1
        #     if(ARF.Register[regToRegIndex(currentInstruction.operand1)] < ARF.Register[regToRegIndex(currentInstruction.operand2)]) :
        #         PC = int(currentInstruction.operand3)
        #         branchTakenCount += 1
        #         error = 1   # Flush pipeline
        # #LSL
        # elif currentInstruction.opCode == "LSL":
        #     output = int(ARF.Register[regToRegIndex(currentInstruction.operand2)]) << int(ARF.Register[regToRegIndex(currentInstruction.operand3)])
        # #LSR
        # elif currentInstruction.opCode == "LSR":
        #     output = int(ARF.Register[regToRegIndex(currentInstruction.operand2)]) >> int(ARF.Register[regToRegIndex(currentInstruction.operand3)])
        # #XOR
        # elif currentInstruction.opCode == "XOR" :
        #     output = int(ARF.Register[regToRegIndex(currentInstruction.operand2)]) ^ int(ARF.Register[regToRegIndex(currentInstruction.operand3)])
        # #AND
        # elif currentInstruction.opCode == "AND" :
        #     output = int(ARF.Register[regToRegIndex(currentInstruction.operand2)]) & int(ARF.Register[regToRegIndex(currentInstruction.operand3)])
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
            error = -1
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output