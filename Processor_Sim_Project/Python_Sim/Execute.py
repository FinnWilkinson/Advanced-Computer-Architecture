from Instruction import Instruction
from Register_File import RegFile

class Execution_Unit :

    def __init__(self) :
        return

    def executeInstruction(self, DE_EX, RF, MEM, PC, finished, branchExecutedCount, branchTakenCount) :
        error = 0
        # HALT
        if DE_EX._instruction().opCode == "HALT":                                                     
            finished = True
        # ADD
        elif DE_EX._instruction().opCode == "ADD": 
            RF.Set(DE_EX._instruction().operand1, RF.Get(DE_EX._instruction().operand2) + RF.Get(DE_EX._instruction().operand3))
        # ADDI
        elif DE_EX._instruction().opCode == "ADDI": 
            RF.Set(DE_EX._instruction().operand1, RF.Get(DE_EX._instruction().operand2) + int(DE_EX._instruction().operand3))
        # SUB
        elif DE_EX._instruction().opCode == "SUB": 
            RF.Set(DE_EX._instruction().operand1, RF.Get(DE_EX._instruction().operand2) - RF.Get(DE_EX._instruction().operand3))
        # SUBI
        elif DE_EX._instruction().opCode == "SUBI": 
            RF.Set(DE_EX._instruction().operand1, RF.Get(DE_EX._instruction().operand2) - int(DE_EX._instruction().operand3))
        # MUL
        elif DE_EX._instruction().opCode == "MUL": 
            RF.Set(DE_EX._instruction().operand1, RF.Get(DE_EX._instruction().operand2) * RF.Get(DE_EX._instruction().operand3))
        # MULI
        elif DE_EX._instruction().opCode == "MULI": 
            RF.Set(DE_EX._instruction().operand1, RF.Get(DE_EX._instruction().operand2) * int(DE_EX._instruction().operand3))
        # DIV
        elif DE_EX._instruction().opCode == "DIV": 
            RF.Set(DE_EX._instruction().operand1, int(RF.Get(DE_EX._instruction().operand2) / RF.Get(DE_EX._instruction().operand3)))
        # DIVI
        elif DE_EX._instruction().opCode == "DIVI": 
            RF.Set(DE_EX._instruction().operand1, int(RF.Get(DE_EX._instruction().operand2) / int(DE_EX._instruction().operand3)))
        # LD
        elif DE_EX._instruction().opCode == "LD": 
            RF.Set(DE_EX._instruction().operand1, MEM[DE_EX._targetAddress()])
        # LDC
        elif DE_EX._instruction().opCode == "LDC": 
            RF.Set(DE_EX._instruction().operand1, MEM[DE_EX._targetAddress()])
        # STR
        elif DE_EX._instruction().opCode == "STR": 
            MEM[DE_EX._targetAddress()] = RF.Get(DE_EX._instruction().operand1)
        # STRC
        elif DE_EX._instruction().opCode == "STRC":
            MEM[DE_EX._targetAddress()] = RF.Get(DE_EX._instruction().operand1)
        # CMP
        elif DE_EX._instruction().opCode == "CMP": 
            if(RF.Get(DE_EX._instruction().operand2) > RF.Get(DE_EX._instruction().operand3)) :
                RF.Set(DE_EX._instruction().operand1, 1)
            elif(RF.Get(DE_EX._instruction().operand2) == RF.Get(DE_EX._instruction().operand3)) :
                RF.Set(DE_EX._instruction().operand1, 0)
            elif(RF.Get(DE_EX._instruction().operand2) < RF.Get(DE_EX._instruction().operand3)) :
                RF.Set(DE_EX._instruction().operand1, -1)
        # JMP
        elif DE_EX._instruction().opCode == "JMP": 
            branchExecutedCount += 1
            branchTakenCount += 1
            PC = RF.Get(DE_EX._instruction().operand1)
        # BR
        elif DE_EX._instruction().opCode == "BR": 
            branchExecutedCount += 1
            branchTakenCount += 1
            PC = int(DE_EX._instruction().operand1)
        # BEQ
        elif DE_EX._instruction().opCode == "BEQ": 
            branchExecutedCount += 1
            if(RF.Get(DE_EX._instruction().operand1) == RF.Get(DE_EX._instruction().operand2)) :
                PC = int(DE_EX._instruction().operand3)
                branchTakenCount += 1
        # BLT
        elif DE_EX._instruction().opCode == "BLT": 
            branchExecutedCount += 1
            if(RF.Get(DE_EX._instruction().operand1) < RF.Get(DE_EX._instruction().operand2)) :
                PC = int(DE_EX._instruction().operand3)
                branchTakenCount += 1
        #LSL
        elif DE_EX._instruction().opCode == "LSL":
            RF.Set(DE_EX._instruction().operand1, int(RF.Get(DE_EX._instruction().operand2) << int(RF.Get(RF.Get(DE_EX._instruction().operand3)))))
        #LSR
        elif DE_EX._instruction().opCode == "LSR":
            RF.Set(DE_EX._instruction().operand1, int(RF.Get(DE_EX._instruction().operand2) >> int(RF.Get(RF.Get(DE_EX._instruction().operand3)))))
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(DE_EX._instruction().opCode))
            error = -1

        return error, PC, finished, branchExecutedCount, branchTakenCount