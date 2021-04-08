from Instruction import Instruction
from Register_File import *
from Reg_To_Reg_Index import *

# ARITHMETIC EXECUTION UNIT
class ARITH_Execution_Unit :
    def __init__(self) :
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount) :
        output = None
        error = 0
        currentInstruction = IS_EX.Instruction[EUindex]
        # Invalid due to branch mispredict
        if currentInstruction.Valid == False :
            return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output
        # ADD
        if currentInstruction.opCode == "ADD": 
            output = ARF.Register[regToRegIndex(currentInstruction.operand2)] + ARF.Register[regToRegIndex(currentInstruction.operand3)]
        # ADDI
        elif currentInstruction.opCode == "ADDI": 
            output = ARF.Register[regToRegIndex(currentInstruction.operand2)] + int(currentInstruction.operand3)
        # SUB
        elif currentInstruction.opCode == "SUB": 
            output = ARF.Register[regToRegIndex(currentInstruction.operand2)] - ARF.Register[regToRegIndex(currentInstruction.operand3)]
        # SUBI
        elif currentInstruction.opCode == "SUBI": 
            output = ARF.Register[regToRegIndex(currentInstruction.operand2)] - int(currentInstruction.operand3)
        # MUL
        elif currentInstruction.opCode == "MUL": 
            output = ARF.Register[regToRegIndex(currentInstruction.operand2)] * ARF.Register[regToRegIndex(currentInstruction.operand3)]
        # MULI
        elif currentInstruction.opCode == "MULI": 
            output = ARF.Register[regToRegIndex(currentInstruction.operand2)] * int(currentInstruction.operand3)
        # DIV
        elif currentInstruction.opCode == "DIV": 
            output = ARF.Register[regToRegIndex(currentInstruction.operand2)] / ARF.Register[regToRegIndex(currentInstruction.operand3)]
        # DIVI
        elif currentInstruction.opCode == "DIVI": 
            output = ARF.Register[regToRegIndex(currentInstruction.operand2)] / int(currentInstruction.operand3)
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
            error = -1
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output


# LOAD / STORE EXECUTION UNIT
class LDSTR_Execution_Unit :
    def __init__(self) :
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount) :
        output = None
        error = 0
        currentInstruction = IS_EX.Instruction[EUindex]
        # Invalid due to branch mispredict
        if currentInstruction.Valid == False :
            return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output
        # LD
        if currentInstruction.opCode == "LD": 
            output = MEM[ARF.Register[regToRegIndex(currentInstruction.operand2)] + ARF.Register[regToRegIndex(currentInstruction.operand3)]]
        # LDC
        elif currentInstruction.opCode == "LDC": 
            output = MEM[ARF.Register[regToRegIndex(currentInstruction.operand2)] + int(currentInstruction.operand3)]
        # STR
        elif currentInstruction.opCode == "STR": 
            MEM[ARF.Register[regToRegIndex(currentInstruction.operand2)] + ARF.Register[regToRegIndex(currentInstruction.operand3)]] = ARF.Register[regToRegIndex(currentInstruction.operand1)]
        # STRC
        elif currentInstruction.opCode == "STRC":
            MEM[ARF.Register[regToRegIndex(currentInstruction.operand2)] + int(currentInstruction.operand3)] = ARF.Register[regToRegIndex(currentInstruction.operand1)]
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
            error = -1
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
        if currentInstruction.opCode == "HALT":                                                     
            finished = True
        # CMP
        elif currentInstruction.opCode == "CMP": 
            if(ARF.Register[regToRegIndex(currentInstruction.operand2)] > ARF.Register[regToRegIndex(currentInstruction.operand3)]) :
                output = 1
            elif(ARF.Register[regToRegIndex(currentInstruction.operand2)] == ARF.Register[regToRegIndex(currentInstruction.operand3)]) :
                output = 0
            elif(ARF.Register[regToRegIndex(currentInstruction.operand2)] < ARF.Register[regToRegIndex(currentInstruction.operand3)]) :
                output = -1
        # JMP
        elif currentInstruction.opCode == "JMP": 
            branchExecutedCount += 1
            branchTakenCount += 1
            PC = ARF.Register[regToRegIndex(currentInstruction.operand1)]
            error = 1   # Flush pipeline
        # BR
        elif currentInstruction.opCode == "BR": 
            branchExecutedCount += 1
            branchTakenCount += 1
            PC = int(currentInstruction.operand1)
            error = 1   # Flush pipeline
        # BEQ
        elif currentInstruction.opCode == "BEQ": 
            branchExecutedCount += 1
            if(ARF.Register[regToRegIndex(currentInstruction.operand1)] == ARF.Register[regToRegIndex(currentInstruction.operand2)]) :
                PC = int(currentInstruction.operand3)
                branchTakenCount += 1
                error = 1   # Flush pipeline
        # BLT
        elif currentInstruction.opCode == "BLT": 
            branchExecutedCount += 1
            if(ARF.Register[regToRegIndex(currentInstruction.operand1)] < ARF.Register[regToRegIndex(currentInstruction.operand2)]) :
                PC = int(currentInstruction.operand3)
                branchTakenCount += 1
                error = 1   # Flush pipeline
        #LSL
        elif currentInstruction.opCode == "LSL":
            output = int(ARF.Register[regToRegIndex(currentInstruction.operand2)]) << int(ARF.Register[regToRegIndex(currentInstruction.operand3)])
        #LSR
        elif currentInstruction.opCode == "LSR":
            output = int(ARF.Register[regToRegIndex(currentInstruction.operand2)]) >> int(ARF.Register[regToRegIndex(currentInstruction.operand3)])
        #XOR
        elif currentInstruction.opCode == "XOR" :
            output = int(ARF.Register[regToRegIndex(currentInstruction.operand2)]) ^ int(ARF.Register[regToRegIndex(currentInstruction.operand3)])
        #AND
        elif currentInstruction.opCode == "AND" :
            output = int(ARF.Register[regToRegIndex(currentInstruction.operand2)]) & int(ARF.Register[regToRegIndex(currentInstruction.operand3)])
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
            error = -1
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output