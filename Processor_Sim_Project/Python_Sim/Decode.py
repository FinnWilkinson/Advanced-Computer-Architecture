from Instruction import Instruction
from Register_File import RegFile
from Reg_To_Reg_Index import *

# Instructions:
# HALT = 0, ADD = 1, ADDI = 2, SUB = 3, SUBI = 4, MUL = 5, MULI = 6, DIV = 7, DIVI = 8, LD = 9,
# LDC = 10, STR = 11, STRC = 12, CMP = 13, JMP = 14, BR = 15, BEQ = 16, BLT = 17, LSL = 18, LSR = 19
# XOR = 20, AND = 21

class Decode_Unit :

    def __init__(self) :
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.loadStoreInstructions = ["LD", "LDC", "STR", "STRC"]
        self.logicInstructions = ["HALT", "LSL", "LSR", "AND", "XOR"]
        self.state = 0       # 0 = fine, 1 = stalled due to dependancy

    def _state(self, input=None) :
        if input is not None :
            self.state = input
        else :
            return self.state

    def decodeInstruction(self, IF_DE, DE_IS, RF) :
        # Get instruction Type = 0,1,2,3 (branch, load/store, arithmetic, logic)
        # Calc. target address

        nextInstruction = IF_DE._instruction()

        #see if there is any dependancies
        canProceed = 0
        if("r" in str(nextInstruction.operand1)) :
            canProceed += RF._inUse(regToRegIndex(nextInstruction.operand1))
        if("r" in str(nextInstruction.operand2)) :
            canProceed += RF._inUse(regToRegIndex(nextInstruction.operand2))
        if("r" in str(nextInstruction.operand3)) :
            canProceed += RF._inUse(regToRegIndex(nextInstruction.operand3))

        if(canProceed != 0) :
            self.state = 1
            return IF_DE, DE_IS
        else :
            self.state = 0

        # If no dependancies, continue
        if(self.state == 0) :
            if nextInstruction.opCode in self.branchInstructions :
                DE_IS._type(0)
            elif nextInstruction.opCode in self.loadStoreInstructions :
                DE_IS._type(1)
            elif nextInstruction.opCode in self.logicInstructions :
                DE_IS._type(3)
            else :
                DE_IS._type(2)

            if DE_IS._type() == 1 :
                targetAddress = 0 
                if nextInstruction.opCode == "LD" or nextInstruction.opCode == "STR" :
                    targetAddress = RF.Get(nextInstruction.operand2) + RF.Get(nextInstruction.operand3)
                elif nextInstruction.opCode == "LDC" or nextInstruction.opCode == "STRC" :
                    targetAddress = RF.Get(nextInstruction.operand2) + int(nextInstruction.operand3)
                
                DE_IS._targetAddress(targetAddress)

            DE_IS._instruction(nextInstruction)

            # Set reg to in use, Actual write back occurs in execute
            # 0 = NOT in use,   1 = in use
            if("r" in str(nextInstruction.operand1)) :
                RF._inUse(regToRegIndex(nextInstruction.operand1), 1)
            if("r" in str(nextInstruction.operand2)) :
                RF._inUse(regToRegIndex(nextInstruction.operand2), 1)
            if("r" in str(nextInstruction.operand3)) :
                RF._inUse(regToRegIndex(nextInstruction.operand3), 1)
        

        return IF_DE, DE_IS
        