from Instruction import Instruction
from Register_File import RegFile

class Execution_Unit :
    # inputType = 0,1,2 (arithmetic, load/store, branch/logic) 
    def __init__(self, inputType) :
        self.type = inputType
        return

    def executeInstruction(self, IS_EX, EUindex, RF, MEM, PC, finished, branchExecutedCount, branchTakenCount) :
        error = 0
        currentInstruction = IS_EX._instruction(EUindex)
        targetAddress = IS_EX._targetAddress(EUindex)
        # ARITHMETIC EXECUTION UNIT
        if(self.type == 0):
            # ADD
            if currentInstruction.opCode == "ADD": 
                RF.Set(currentInstruction.operand1, RF.Get(currentInstruction.operand2) + RF.Get(currentInstruction.operand3))
            # ADDI
            elif currentInstruction.opCode == "ADDI": 
                RF.Set(currentInstruction.operand1, RF.Get(currentInstruction.operand2) + int(currentInstruction.operand3))
            # SUB
            elif currentInstruction.opCode == "SUB": 
                RF.Set(currentInstruction.operand1, RF.Get(currentInstruction.operand2) - RF.Get(currentInstruction.operand3))
            # SUBI
            elif currentInstruction.opCode == "SUBI": 
                RF.Set(currentInstruction.operand1, RF.Get(currentInstruction.operand2) - int(currentInstruction.operand3))
            # MUL
            elif currentInstruction.opCode == "MUL": 
                RF.Set(currentInstruction.operand1, RF.Get(currentInstruction.operand2) * RF.Get(currentInstruction.operand3))
            # MULI
            elif currentInstruction.opCode == "MULI": 
                RF.Set(currentInstruction.operand1, RF.Get(currentInstruction.operand2) * int(currentInstruction.operand3))
            # DIV
            elif currentInstruction.opCode == "DIV": 
                RF.Set(currentInstruction.operand1, int(RF.Get(currentInstruction.operand2) / RF.Get(currentInstruction.operand3)))
            # DIVI
            elif currentInstruction.opCode == "DIVI": 
                RF.Set(currentInstruction.operand1, int(RF.Get(currentInstruction.operand2) / int(currentInstruction.operand3)))
            # Opcode not recognised
            else: 
                print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
                error = -1
        # LOAD / STORE EXECUTION UNIT
        elif(self.type == 1) :
            # LD
            if currentInstruction.opCode == "LD": 
                RF.Set(currentInstruction.operand1, MEM[targetAddress])
            # LDC
            elif currentInstruction.opCode == "LDC": 
                RF.Set(currentInstruction.operand1, MEM[targetAddress])
            # STR
            elif currentInstruction.opCode == "STR": 
                MEM[targetAddress] = RF.Get(currentInstruction.operand1)
            # STRC
            elif currentInstruction.opCode == "STRC":
                MEM[targetAddress] = RF.Get(currentInstruction.operand1)
            # Opcode not recognised
            else: 
                print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
                error = -1
        # BRANCH / LOGIC EXECUTION UNIT
        elif(self.type == 2) :
            # HALT
            if currentInstruction.opCode == "HALT":                                                     
                finished = True
            # CMP
            elif currentInstruction.opCode == "CMP": 
                if(RF.Get(currentInstruction.operand2) > RF.Get(currentInstruction.operand3)) :
                    RF.Set(currentInstruction.operand1, 1)
                elif(RF.Get(currentInstruction.operand2) == RF.Get(currentInstruction.operand3)) :
                    RF.Set(currentInstruction.operand1, 0)
                elif(RF.Get(currentInstruction.operand2) < RF.Get(currentInstruction.operand3)) :
                    RF.Set(currentInstruction.operand1, -1)
            # JMP
            elif currentInstruction.opCode == "JMP": 
                branchExecutedCount += 1
                branchTakenCount += 1
                PC = RF.Get(currentInstruction.operand1)
            # BR
            elif currentInstruction.opCode == "BR": 
                branchExecutedCount += 1
                branchTakenCount += 1
                PC = int(currentInstruction.operand1)
                error = 1 #flush pipeline
            # BEQ
            elif currentInstruction.opCode == "BEQ": 
                branchExecutedCount += 1
                if(RF.Get(currentInstruction.operand1) == RF.Get(currentInstruction.operand2)) :
                    PC = int(currentInstruction.operand3)
                    branchTakenCount += 1
                    error = 1 #flush pipeline
            # BLT
            elif currentInstruction.opCode == "BLT": 
                branchExecutedCount += 1
                if(RF.Get(currentInstruction.operand1) < RF.Get(currentInstruction.operand2)) :
                    PC = int(currentInstruction.operand3)
                    branchTakenCount += 1
                    error = 1 #flush pipeline
            #LSL
            elif currentInstruction.opCode == "LSL":
                RF.Set(currentInstruction.operand1, int(RF.Get(currentInstruction.operand2)) << int(RF.Get(currentInstruction.operand3)))
            #LSR
            elif currentInstruction.opCode == "LSR":
                RF.Set(currentInstruction.operand1, int(RF.Get(currentInstruction.operand2)) >> int(RF.Get(currentInstruction.operand3)))
            #XOR
            elif currentInstruction.opCode == "XOR" :
                RF.Set(currentInstruction.operand1, int(RF.Get(currentInstruction.operand2)) ^ int(RF.Get(currentInstruction.operand3)))
            #AND
            elif currentInstruction.opCode == "AND" :
                RF.Set(currentInstruction.operand1, int(RF.Get(currentInstruction.operand2)) & int(RF.Get(currentInstruction.operand3)))
            # Opcode not recognised
            else: 
                print("ERROR - Opcode '{}' not recognised. Exiting..." .format(currentInstruction.opCode))
                error = -1
        return error, PC, finished, branchExecutedCount, branchTakenCount