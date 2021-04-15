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
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT"]

    def decodeInstruction(self, IF_DE, RS, ARF) :
        stallThisCycle = False
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
        

    def decodeNext(self, IF_DE, RS, ARF) :
        stallThisCycle = False

        # Add to BRACH/LOGIC RS
        if IF_DE.Instruction.opCode in self.branchInstructions or IF_DE.Instruction.opCode in self.logicInstructions :
            # Check corresponding RS is not full
            if(len(RS[2].Instruction) < 8) :
                RS[2].Instruction.append(copy.copy(IF_DE.Instruction))
                RS[2].TargetAddress.append(0)
                RS[2].Op.append(copy.copy(IF_DE.Instruction.opCode))
                # Operand 1
                if(IF_DE.Instruction.opCode in self.readOnlyINSTR) :
                    if("r" in str(IF_DE.Instruction.operand1)) :
                        RS[2].D1.append(None)
                    else :
                        RS[2].D1.append(copy.copy(IF_DE.Instruction.operand1))
                else :
                    RS[2].D1.append(copy.copy(IF_DE.Instruction.operand1))
                # Operand 2
                if("r" in str(IF_DE.Instruction.operand2)) :
                    RS[2].V1.append(1)
                    RS[2].S1.append(0)
                else :
                    RS[2].V1.append(0)
                    RS[2].S1.append(copy.copy(IF_DE.Instruction.operand2))
                # Operand 3
                if("r" in str(IF_DE.Instruction.operand3)) :
                    RS[2].V2.append(1)
                    RS[2].S2.append(0)
                else :
                    RS[2].V2.append(0)
                    RS[2].S2.append(copy.copy(IF_DE.Instruction.operand3))
                IF_DE.Empty = True
            else :
                stallThisCycle = True       # If corresponding RS full, log stall
        # Add to LOAD/STORE RS
        elif IF_DE.Instruction.opCode in self.loadStoreInstructions :
            # Check corresponding RS is not full
            if(len(RS[1].Instruction) < 8) :
                RS[1].Instruction.append(copy.copy(IF_DE.Instruction))
                RS[1].TargetAddress.append(0)
                RS[1].Op.append(copy.copy(IF_DE.Instruction.opCode))
                # Operand 1
                if(IF_DE.Instruction.opCode in self.readOnlyINSTR) :
                    if("r" in str(IF_DE.Instruction.operand1)) :
                        RS[1].D1.append(None)
                    else :
                        RS[1].D1.append(copy.copy(IF_DE.Instruction.operand1))
                else :
                    RS[1].D1.append(copy.copy(IF_DE.Instruction.operand1))
                # Operand 2
                if("r" in str(IF_DE.Instruction.operand2)) :
                    RS[1].V1.append(1)
                    RS[1].S1.append(0)
                else :
                    RS[1].V1.append(0)
                    RS[1].S1.append(copy.copy(IF_DE.Instruction.operand2))
                # Operand 3
                if("r" in str(IF_DE.Instruction.operand3)) :
                    RS[1].V2.append(1)
                    RS[1].S2.append(0)
                else :
                    RS[1].V2.append(0)
                    RS[1].S2.append(copy.copy(IF_DE.Instruction.operand3))
                IF_DE.Empty = True
            else :
                stallThisCycle = True       # If corresponding RS full, log stall
        # Add to ARITHMETIC RS
        else :
            # Check corresponding RS is not full
            if(len(RS[0].Instruction) < 16) :
                RS[0].Instruction.append(copy.copy(IF_DE.Instruction))
                RS[0].TargetAddress.append(0)
                RS[0].Op.append(copy.copy(IF_DE.Instruction.opCode))
                RS[0].D1.append(copy.copy(IF_DE.Instruction.operand1))
                if("r" in str(IF_DE.Instruction.operand2)) :
                    RS[0].V1.append(1)
                    RS[0].S1.append(0)
                else :
                    RS[0].V1.append(0)
                    RS[0].S1.append(copy.copy(IF_DE.Instruction.operand2))
                if("r" in str(IF_DE.Instruction.operand3)) :
                    RS[0].V2.append(1)
                    RS[0].S2.append(0)
                else :
                    RS[0].V2.append(0)
                    RS[0].S2.append(copy.copy(IF_DE.Instruction.operand3))
                IF_DE.Empty = True
            else :
                stallThisCycle = True       # If corresponding RS full, log stall

        return stallThisCycle