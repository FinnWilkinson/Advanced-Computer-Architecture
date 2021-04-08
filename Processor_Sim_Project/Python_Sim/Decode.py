from Instruction import Instruction
from Reg_To_Reg_Index import *
import copy as copy

# Instructions:
# HALT = 0, ADD = 1, ADDI = 2, SUB = 3, SUBI = 4, MUL = 5, MULI = 6, DIV = 7, DIVI = 8, LD = 9,
# LDC = 10, STR = 11, STRC = 12, CMP = 13, JMP = 14, BR = 15, BEQ = 16, BLT = 17, LSL = 18, LSR = 19
# XOR = 20, AND = 21

class Decode_Unit :

    def __init__(self) :
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.loadStoreInstructions = ["LD", "LDC", "STR", "STRC"]
        self.logicInstructions = ["HALT", "LSL", "LSR", "AND", "XOR"]

    def decodeInstruction(self, IF_DE, RS, ARF, stallThisCycle) :
        # Add to BRACH/LOGIC RS
        if IF_DE.Instruction.opCode in self.branchInstructions or IF_DE.Instruction.opCode in self.logicInstructions :
            if(len(RS[2].Instruction) < 8) :
                RS[2].Instruction.append(copy.copy(IF_DE.Instruction))
                RS[2].TargetAddress.append(0)
                IF_DE.Empty = True
            else :
                stallThisCycle = True
        # Add to LOAD/STORE RS
        elif IF_DE.Instruction.opCode in self.loadStoreInstructions :
            if(len(RS[1].Instruction) < 8) :
                RS[1].Instruction.append(copy.copy(IF_DE.Instruction))
                RS[1].TargetAddress.append(0)
                IF_DE.Empty = True
            else :
                stallThisCycle = True
        # Add to ARITHMETIC RS
        else :
            if(len(RS[0].Instruction) < 16) :
                RS[0].Instruction.append(copy.copy(IF_DE.Instruction))
                RS[0].TargetAddress.append(0)
                IF_DE.Empty = True
            else :
                stallThisCycle = True
        
        
    
        return stallThisCycle
        