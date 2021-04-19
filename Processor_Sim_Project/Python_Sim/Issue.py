from Instruction import Instruction
from Reg_To_Reg_Index import *
import copy as copy

class Issue_Unit :
    def __init__(self) :
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT"]
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.nextInstruction = 0
        return


    def issue(self, RS, IS_EX, ARF, ROB) :
        stallThisCycle = False
        instructionsIssued = 0

        # Only issue instructions that have all operands Valid
        # In each RS, issue oldest (lowest INSTR number) instruction that has all values + no True dependancies with instructions ahead of it in queue
        # List will be sorted by default from oldest to youngest

        # Arithmetic RS
        if(len(RS[0].Instruction) > 0) :
            # Check EU ready to recieve next instruction
            if(IS_EX[0].Empty == True or IS_EX[1].Empty == True) :
                for i in range(0, len(RS[0].Instruction)) :
                    # Try get all values, if cant then go to next instruction in queue

                    # Check Valid, if not remove
                    if(RS[0].Instruction[i].Valid == False) :
                        RS[0].Instruction.pop(i)
                        RS[0].TargetAddress.pop(i)
                        RS[0].Op.pop(i)
                        RS[0].D1.pop(i)
                        RS[0].V1.pop(i)
                        RS[0].V2.pop(i)
                        RS[0].S1.pop(i)
                        RS[0].S2.pop(i)
                        break

                    # Get value of operand2 if needed
                    if(RS[0].V1[i] != 0) :
                        tempROBaddr = int(RS[0].V1[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[0].S1[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # Get value of operand3 if needed
                    if(RS[0].V2[i] != 0) :
                        tempROBaddr = int(RS[0].V2[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[0].S2[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # If no branch that preceeds it, Issue          !! EDIT OUT WITH BRANCH PREDICTION !!
                    preceedingBranch = False
                    for j in range(0, len(RS[2].Instruction)) :
                        if(RS[2].Instruction[j].instructionNumber < RS[0].Instruction[i].instructionNumber) :
                            if(RS[2].Op[j] in self.branchInstructions) :
                                preceedingBranch = True
                                break
                        else :
                            break
                    if(preceedingBranch == True) :
                        break

                    # Issue to EU
                    if(IS_EX[0].Empty == True) :
                        IS_EX[0].TargetAddress = copy.copy(RS[0].TargetAddress[i])
                        IS_EX[0].InstructionNumber = copy.copy(RS[0].Instruction[i].instructionNumber)
                        IS_EX[0].Op = copy.copy(RS[0].Op[i])
                        IS_EX[0].D1 = copy.copy(RS[0].D1[i])
                        IS_EX[0].S1 = copy.copy(RS[0].S1[i])
                        IS_EX[0].S2 = copy.copy(RS[0].S2[i])
                        IS_EX[0].Empty = False
                    else :
                        IS_EX[1].TargetAddress = copy.copy(RS[0].TargetAddress[i])
                        IS_EX[1].InstructionNumber = copy.copy(RS[0].Instruction[i].instructionNumber)
                        IS_EX[1].Op = copy.copy(RS[0].Op[i])
                        IS_EX[1].D1 = copy.copy(RS[0].D1[i])
                        IS_EX[1].S1 = copy.copy(RS[0].S1[i])
                        IS_EX[1].S2 = copy.copy(RS[0].S2[i])
                        IS_EX[1].Empty = False
                    
                    # Remove from RS
                    RS[0].Instruction.pop(i)
                    RS[0].TargetAddress.pop(i)
                    RS[0].Op.pop(i)
                    RS[0].D1.pop(i)
                    RS[0].V1.pop(i)
                    RS[0].V2.pop(i)
                    RS[0].S1.pop(i)
                    RS[0].S2.pop(i)

                    instructionsIssued += 1
                    break
            else :
                # If no EU free, stall
                stallThisCycle = True                   
        else :
            # If reservation station full, stall
            stallThisCycle = True

############################################################################################

        # Load / Store RS
        if(len(RS[1].Instruction) > 0) :
            # Check EU ready to recieve next instruction
            if(IS_EX[2].Empty == True) :
                for i in range(0, len(RS[1].Instruction)) :
                    # Try get all values, if cant then go to next instruction in queue

                    # Check Valid, if not remove
                    if(RS[1].Instruction[i].Valid == False) :
                        RS[1].Instruction.pop(i)
                        RS[1].TargetAddress.pop(i)
                        RS[1].Op.pop(i)
                        RS[1].D1.pop(i)
                        RS[1].V1.pop(i)
                        RS[1].V2.pop(i)
                        RS[1].S1.pop(i)
                        RS[1].S2.pop(i)
                        break

                    # Check if read-only instruction, and get value of operand1 if needed
                    if(RS[1].Op[i] in self.readOnlyINSTR) :
                        if("ROB" in str(RS[1].D1[i])) :
                            tempROBaddr = int(RS[1].D1[i][3:])
                            if(ROB.Complete[tempROBaddr] == 1) :
                                # Value ready to be read
                                RS[1].D1[i] = copy.copy(ROB.Value[tempROBaddr])
                            else :
                                # Value not ready, continue to next in list
                                continue

                    # Get value of operand2 if needed
                    if(RS[1].V1[i] != 0) :
                        tempROBaddr = int(RS[1].V1[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[1].S1[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # Get value of operand3 if needed
                    if(RS[1].V2[i] != 0) :
                        tempROBaddr = int(RS[1].V2[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[1].S2[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # If no branch that preceeds it, Issue          !! EDIT OUT WITH BRANCH PREDICTION !!
                    preceedingBranch = False
                    for j in range(0, len(RS[2].Instruction)) :
                        if(RS[2].Instruction[j].instructionNumber < RS[1].Instruction[i].instructionNumber) :
                            if(RS[2].Op[j] in self.branchInstructions) :
                                preceedingBranch = True
                                break
                        else :
                            break
                    if(preceedingBranch == True) :
                        break

                    # Issue to EU
                    IS_EX[2].TargetAddress = copy.copy(RS[1].TargetAddress[i])
                    IS_EX[2].InstructionNumber = copy.copy(RS[1].Instruction[i].instructionNumber)
                    IS_EX[2].Op = copy.copy(RS[1].Op[i])
                    IS_EX[2].D1 = copy.copy(RS[1].D1[i])
                    IS_EX[2].S1 = copy.copy(RS[1].S1[i])
                    IS_EX[2].S2 = copy.copy(RS[1].S2[i])
                    IS_EX[2].Empty = False
                    
                    # Remove from RS
                    RS[1].Instruction.pop(i)
                    RS[1].TargetAddress.pop(i)
                    RS[1].Op.pop(i)
                    RS[1].D1.pop(i)
                    RS[1].V1.pop(i)
                    RS[1].V2.pop(i)
                    RS[1].S1.pop(i)
                    RS[1].S2.pop(i)

                    instructionsIssued += 1
                    break
            else :
                # If no EU free, stall
                stallThisCycle = True                   
        else :
            # If reservation station full, stall
            stallThisCycle = True

##########################################################################################

        # Branch / Logic
        if(len(RS[2].Instruction) > 0) :
            # Check EU ready to recieve next instruction
            if(IS_EX[3].Empty == True) :
                for i in range(0, len(RS[2].Instruction)) :
                    # Check Valid, if not remove
                    if(RS[2].Instruction[i].Valid == False) :
                        RS[2].Instruction.pop(i)
                        RS[2].TargetAddress.pop(i)
                        RS[2].Op.pop(i)
                        RS[2].D1.pop(i)
                        RS[2].V1.pop(i)
                        RS[2].V2.pop(i)
                        RS[2].S1.pop(i)
                        RS[2].S2.pop(i)
                        break

                    # Check for HALT
                    if(RS[2].Op[i] == "HALT") :
                        if(len(RS[0].Op) != 0 or len(RS[1].Op) != 0) :
                            continue
                        if(IS_EX[0].Empty == False or IS_EX[1].Empty == False or IS_EX[2].Empty == False or IS_EX[3].Empty == False) :
                            continue

                    # Try get all values, if cant then go to next instruction in queue

                    # Check if read-only instruction, and get value of operand1 if needed
                    if(RS[2].Op[i] in self.readOnlyINSTR) :
                        if("ROB" in str(RS[2].D1[i])) :
                            tempROBaddr = int(RS[2].D1[i][3:])
                            if(ROB.Complete[tempROBaddr] == 1) :
                                # Value ready to be read
                                RS[2].D1[i] = copy.copy(ROB.Value[tempROBaddr])
                            else :
                                # Value not ready, continue to next in list
                                continue

                    # Get value of operand2 if needed
                    if(RS[2].V1[i] != 0) :
                        tempROBaddr = int(RS[2].V1[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[2].S1[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # Get value of operand3 if needed
                    if(RS[2].V2[i] != 0) :
                        tempROBaddr = int(RS[2].V2[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[2].S2[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # If no branch that preceeds it, Issue          !! EDIT OUT WITH BRANCH PREDICTION !!
                    preceedingBranch = False
                    for j in range(0, len(RS[2].Instruction)) :
                        if(RS[2].Instruction[j].instructionNumber < RS[2].Instruction[i].instructionNumber) :
                            if(RS[2].Op[j] in self.branchInstructions) :
                                preceedingBranch = True
                                break
                        else :
                            break
                    if(preceedingBranch == True) :
                        break

                    # IF branch, make sure all done before it
                    oldestINSTR = True
                    for t in range(0,1) :
                        for h in range(0, len(RS[t].Instruction)) :
                            if(RS[t].Instruction[h].instructionNumber < RS[2].Instruction[i].instructionNumber) :
                                oldestINSTR = False
                    if(oldestINSTR == False) :
                        continue
                    

                    # Issue to EU
                    IS_EX[3].TargetAddress = copy.copy(RS[2].TargetAddress[i])
                    IS_EX[3].InstructionNumber = copy.copy(RS[2].Instruction[i].instructionNumber)
                    IS_EX[3].Op = copy.copy(RS[2].Op[i])
                    IS_EX[3].D1 = copy.copy(RS[2].D1[i])
                    IS_EX[3].S1 = copy.copy(RS[2].S1[i])
                    IS_EX[3].S2 = copy.copy(RS[2].S2[i])
                    IS_EX[3].Empty = False
                    
                    # Remove from RS
                    RS[2].Instruction.pop(i)
                    RS[2].TargetAddress.pop(i)
                    RS[2].Op.pop(i)
                    RS[2].D1.pop(i)
                    RS[2].V1.pop(i)
                    RS[2].V2.pop(i)
                    RS[2].S1.pop(i)
                    RS[2].S2.pop(i)

                    instructionsIssued += 1
                    break
            else :
                # If no EU free, stall
                stallThisCycle = True                   
        else :
            # If reservation station full, stall
            stallThisCycle = True
        
##########################################################################################

        if(instructionsIssued != 3) :
            stallThisCycle = True

        return stallThisCycle
