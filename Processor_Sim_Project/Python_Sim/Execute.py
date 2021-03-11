from Instruction import Instruction
from Register_File import RegFile

class Execution_Unit :

    def __init__(self) :
        return

    def executeInstruction(self, opcode, operand1, operand2, operand3, targetAddress, RF, MEM, PC, cycles, instructionExecuteCount, finished, branchCount) :
        error = 0
        # HALT
        if opcode == "HALT":                                                     
            finished = True
        # ADD
        elif opcode == "ADD": 
            RF.Set(operand1, RF.Get(operand2) + RF.Get(operand3))
        # ADDI
        elif opcode == "ADDI": 
            RF.Set(operand1, RF.Get(operand2) + int(operand3))
        # SUB
        elif opcode == "SUB": 
            RF.Set(operand1, RF.Get(operand2) - RF.Get(operand3))
        # SUBI
        elif opcode == "SUBI": 
            RF.Set(operand1, RF.Get(operand2) - int(operand3))
        # MUL
        elif opcode == "MUL": 
            RF.Set(operand1, RF.Get(operand2) * RF.Get(operand3))
        # MULI
        elif opcode == "MULI": 
            RF.Set(operand1, RF.Get(operand2) * int(operand3))
        # DIV
        elif opcode == "DIV": 
            RF.Set(operand1, int(RF.Get(operand2) / RF.Get(operand3)))
        # DIVI
        elif opcode == "DIVI": 
            RF.Set(operand1, int(RF.Get(operand2) / int(operand3)))
        # LD
        elif opcode == "LD": 
            RF.Set(operand1, MEM[targetAddress])
        # LDC
        elif opcode == "LDC": 
            RF.Set(operand1, MEM[targetAddress])
        # STR
        elif opcode == "STR": 
            MEM[targetAddress] = RF.Get(operand1)
        # STRC
        elif opcode == "STRC":
            MEM[targetAddress] = RF.Get(operand1)
        # CMP
        elif opcode == "CMP": 
            if(RF.Get(operand2) > RF.Get(operand3)) :
                RF.Set(operand1, 1)
            elif(RF.Get(operand2) == RF.Get(operand3)) :
                RF.Set(operand1, 0)
            elif(RF.Get(operand2) < RF.Get(operand3)) :
                RF.Set(operand1, -1)
        # JMP
        elif opcode == "JMP": 
            branchCount += 1
            PC = RF.Get(operand1)
        # BR
        elif opcode == "BR": 
            branchCount += 1
            PC = int(operand1)
        # BEQ
        elif opcode == "BEQ": 
            if(RF.Get(operand1) == RF.Get(operand2)) :
                PC = int(operand3)
                branchCount += 1
        # BLT
        elif opcode == "BLT": 
            if(RF.Get(operand1) < RF.Get(operand2)) :
                PC = int(operand3)
                branchCount += 1
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(opcode))
            error = -1

        cycles += 1
        instructionExecuteCount += 1
        return error, PC, cycles, instructionExecuteCount, finished, branchCount