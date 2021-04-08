from Instruction import Instruction
from Reg_To_Reg_Index import *
import copy as copy

class Issue_Unit :
    def __init__(self) :
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT"]
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.nextInstruction = 0
        return

    def issueInstruction(self, RS, IS_EX, ARF, stallThisCycle) :
        # When instruction issued, validation bit in ARF for that register set to NOT valid
        # Only issue instructions that have all operands Valid
        proceed = [True] * 3    # 0 = ARITHMETIC, 1 = LOAD / STORE, 2 = BRANCH / LOGIC
        #FIFO system
        for i in range(0,3) :
            if(len(RS[i].Instruction) > 0) :
                # ARITHMETIC
                if i == 0 :
                    if IS_EX.Empty[0] == True :
                        # Check if all fields are available to read from or write to
                        if("r" in str(RS[i].Instruction[0].operand1)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand1)] != 0) :
                                proceed[0] = False
                        if("r" in str(RS[i].Instruction[0].operand2)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand2)] != 0) :
                                proceed[0] = False
                        if("r" in str(RS[i].Instruction[0].operand3)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand3)] != 0) :
                                proceed[0] = False
                    elif IS_EX.Empty[1] == True :
                        # Check if all fields are available to read from or write to
                        if("r" in str(RS[i].Instruction[0].operand1)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand1)] != 0) :
                                proceed[0] = False
                        if("r" in str(RS[i].Instruction[0].operand2)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand2)] != 0) :
                                proceed[0] = False
                        if("r" in str(RS[i].Instruction[0].operand3)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand3)] != 0) :
                                proceed[0] = False
                    else :
                        proceed[0] = False
                
                # LOAD/STORE
                elif i == 1 :
                    if IS_EX.Empty[2] == True :
                        # Check if all fields are available to read from or write to
                        if("r" in str(RS[i].Instruction[0].operand1)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand1)] != 0) :
                                proceed[1] = False
                        if("r" in str(RS[i].Instruction[0].operand2)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand2)] != 0) :
                                proceed[1] = False
                        if("r" in str(RS[i].Instruction[0].operand3)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand3)] != 0) :
                                proceed[1] = False
                    else :
                        proceed[1] = False
                
                # BRANCH/LOGIC
                else :
                    if IS_EX.Empty[3] == True :
                        # Check if all fields are available to read from or write to
                        if("r" in str(RS[i].Instruction[0].operand1)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand1)] != 0) :
                                proceed[2] = False
                        if("r" in str(RS[i].Instruction[0].operand2)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand2)] != 0) :
                                proceed[2] = False
                        if("r" in str(RS[i].Instruction[0].operand3)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand3)] != 0) :
                                proceed[2] = False
                    else :
                        proceed[2] = False
            else :
                proceed[i] = False



        # Ensure  we execute in order
        if proceed[0] == True:
            if RS[0].Instruction[0].instructionNumber != self.nextInstruction :
                proceed[0] = False
        
        if proceed[1] == True:
            if RS[1].Instruction[0].instructionNumber != self.nextInstruction :
                proceed[1] = False
        
        if proceed[2] == True:
            if RS[2].Instruction[0].instructionNumber != self.nextInstruction :
                proceed[2] = False

       


        issueCount = 0
        if proceed[0] == True:
            # If opcode does operation that writes to ARF then set that register to invalid
            if(RS[0].Instruction[0].opCode not in self.readOnlyINSTR) :
                ARF.regInUse[regToRegIndex(RS[0].Instruction[0].operand1)] = 1
            # Issue to appropriate EU
            if IS_EX.Empty[0] == True :
                IS_EX.Instruction[0] = copy.copy(RS[0].Instruction[0])
                IS_EX.TargetAddress[0] = copy.copy(RS[0].TargetAddress[0])
                IS_EX.Empty[0] = False
            else :
                IS_EX.Instruction[1] = copy.copy(RS[0].Instruction[0])
                IS_EX.TargetAddress[1] = copy.copy(RS[0].TargetAddress[0])
                IS_EX.Empty[1] = False
            # Pop from RS queue
            RS[0].Instruction.pop(0)
            RS[0].TargetAddress.pop(0)
            issueCount += 1

        if proceed[1] == True:
            # If opcode does operation that writes to ARF then set that register to invalid
            if(RS[1].Instruction[0].opCode not in self.readOnlyINSTR) :
                ARF.regInUse[regToRegIndex(RS[1].Instruction[0].operand1)] = 1
            # Issue to appropriate EU
            IS_EX.Instruction[2] = copy.copy(RS[1].Instruction[0])
            IS_EX.TargetAddress[2] = copy.copy(RS[1].TargetAddress[0])
            IS_EX.Empty[2] = False
            # Pop from RS queue
            RS[1].Instruction.pop(0)
            RS[1].TargetAddress.pop(0)
            issueCount += 1

        if proceed[2] == True:
            # If opcode does operation that writes to ARF then set that register to invalid
            if(RS[2].Instruction[0].opCode not in self.readOnlyINSTR) :
                ARF.regInUse[regToRegIndex(RS[2].Instruction[0].operand1)] = 1
            # Issue to appropriate EU
            IS_EX.Instruction[3] = copy.copy(RS[2].Instruction[0])
            IS_EX.TargetAddress[3] = copy.copy(RS[2].TargetAddress[0])
            IS_EX.Empty[3] = False
            # Pop from RS queue
            RS[2].Instruction.pop(0)
            RS[2].TargetAddress.pop(0)
            issueCount += 1
        
        if(issueCount == 0) :
            stallThisCycle = True
        else :
            self.nextInstruction += issueCount

        return stallThisCycle