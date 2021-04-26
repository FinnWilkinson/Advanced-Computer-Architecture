from Instruction import Instruction
from Branch_Prediction import *
import copy as copy

# Instructions:
# HALT = 0, ADD = 1, ADDI = 2, SUB = 3, SUBI = 4, MUL = 5, MULI = 6, DIV = 7, DIVI = 8, LD = 9,
# LDC = 10, STR = 11, STRC = 12, CMP = 13, JMP = 14, BR = 15, BEQ = 16, BLT = 17, LSL = 18, LSR = 19
# XOR = 20, AND = 21, MOD = 22

class Decode_Unit :

    def __init__(self) :
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.loadStoreInstructions = ["LD", "LDC", "STR", "STRC"]
        self.logicInstructions = ["HALT", "LSL", "LSR", "AND", "XOR", "CMP"]
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT"]

    def decode(self, IF_DE, RS, ARF, RAT, ROB, BIPB, BTB, PC, branchPredType, LSQ) :        
        # Get instruction from IF_DE
        nextInstruction = copy.copy(IF_DE.Instruction)

        if(((ROB.IssuePtr + 1) % 256) == ROB.CommitPtr) :
            return True, PC

        if(nextInstruction.opCode in self.loadStoreInstructions and ((LSQ.IssuePtr + 1) % 128) == LSQ.CommitPtr) :
            return True, PC

        # Get Reservation station ID
        resID = 0
        # Branch or Logic
        if(nextInstruction.opCode in self.branchInstructions or nextInstruction.opCode in self.logicInstructions) :
            if(len(RS[2].Instruction) < 8) :
                resID = 2
            else :
                # Full so stall this cycle (return true) and return
                return True, PC
        # Load or Store
        elif(nextInstruction.opCode in self.loadStoreInstructions) :
            if(len(RS[1].Instruction) < 8) :
               resID = 1
            else :
                # Full so stall this cycle (return true) and return
                return True, PC
        # Arithmetic
        else :
            if(len(RS[0].Instruction) < 16) :
               resID = 0
            else :
                # Full so stall this cycle (return true) and return
                return True, PC

        if(branchPredType != 0) :
            # Branch Prediction
            if(nextInstruction.opCode in self.branchInstructions) :
                if(nextInstruction.instructionNumber not in BIPB.InstructionNumber) :
                    # Branch not executed before so not in BTB
                    BIPB.BranchPC.append(copy.copy(IF_DE.InstructionPC))
                    BIPB.InstructionNumber.append(copy.copy(nextInstruction.instructionNumber))
                    # Not in BTB so will default to Fixed prediction (Taken / True)
                    BIPB.Prediction.append(True)
                    BIPB.InstructionType.append(copy.copy(nextInstruction.opCode))

                    # Add Branch to BTB
                    BTB.BranchPC.append(copy.copy(IF_DE.InstructionPC))
                    BTB.BranchType.append(copy.copy(nextInstruction.opCode))
                    if(nextInstruction.opCode == "BR" or nextInstruction.opCode == "JMP") :
                        BTB.LastResult.append(True)
                        BTB.Last2Result.append(3)
                    else :
                        BTB.LastResult.append(True)
                        BTB.Last2Result.append(2)

                    if(nextInstruction.opCode == "BR") :
                        BTB.TargetAddress.append(copy.copy(int(nextInstruction.operand1)))
                        BIPB.TargetAddress.append(copy.copy(int(nextInstruction.operand1)))
                        # Update PC to target address
                        PC = copy.copy(int(nextInstruction.operand1))
                    elif(nextInstruction.opCode == "BEQ" or nextInstruction.opCode == "BLT") :
                        BTB.TargetAddress.append(copy.copy(int(nextInstruction.operand3)))
                        BIPB.TargetAddress.append(copy.copy(int(nextInstruction.operand3)))
                        # Update PC to target address
                        PC = copy.copy(int(nextInstruction.operand3))
                    else :
                        # Need to update in Execute after register is read and address known
                        BTB.TargetAddress.append(0)
                        BIPB.TargetAddress.append(0)
                

        # If load or store, Assign place in LSQ
        if(nextInstruction.opCode in self.loadStoreInstructions) :
            # Assign place in LSQ
            LSQindex = copy.copy(LSQ.IssuePtr)
            LSQ.IssuePtr = copy.copy((LSQ.IssuePtr + 1) % 128)
            # Input values
            LSQ.InstructionNumber[LSQindex] = copy.copy(nextInstruction.instructionNumber)
            LSQ.Complete[LSQindex] = 0
            LSQ.Address[LSQindex] = -1
            if(nextInstruction.opCode == "LD" or nextInstruction.opCode == "LDC") :
                LSQ.InstructionType[LSQindex] = copy.copy("LOAD")
            else :
                LSQ.InstructionType[LSQindex] = copy.copy("STORE")
            



        # Assign place in ROB
        ROBindex = copy.copy(ROB.IssuePtr)
        ROB.IssuePtr = copy.copy((ROB.IssuePtr + 1) % 256)                                # mod 256 so tat index loops around
        # If read only, change ROB register value assigning
        if(nextInstruction.opCode in self.readOnlyINSTR) :
            ROB.Register[ROBindex] = "SKIP"                                     # SKIP as we dont need to write back value
            ROB.Complete[ROBindex] = 1                                          # Completed as nothing to write back or read from
        else :  
            ROB.Register[ROBindex] = copy.copy(nextInstruction.operand1)        # Input actual register to write to
            ROB.Complete[ROBindex] = 0
            ROB.InstructionNumber[ROBindex] = copy.copy(nextInstruction.instructionNumber)
            

        # Read available values via RAT address & assign
        d1 = 0
        v1 = 0
        v2 = 0
        s1 = 0
        s2 = 0
        # Get d1 (operand 1) value if read only and available
        if(nextInstruction.opCode in self.readOnlyINSTR) :
            if("r" in str(nextInstruction.operand1)) :
                if("ROB" in str(RAT.Address[int(nextInstruction.operand1[1:])])) :
                    # Register has been renamed
                    tempRobAddr = copy.copy(int(RAT.Address[int(nextInstruction.operand1[1:])][3:]))
                    if(ROB.Complete[tempRobAddr] == 1) :
                        # Value ready to be read
                        d1 = copy.copy(ROB.Value[tempRobAddr])
                    else :
                        # Value not ready
                        d1 = copy.copy(RAT.Address[int(nextInstruction.operand1[1:])])
                else :
                    # Most up to date value has been written back & no instructions ahead of it write to same register
                    d1 = copy.copy(ARF.Register[int(nextInstruction.operand1[1:])])
            elif(nextInstruction.operand1 != ''):
                # If operand 1 is a constant, get value
                d1 = copy.copy(int(nextInstruction.operand1))

        # Get s1 value (operand 2) if available
        if("r" in str(nextInstruction.operand2)) :
            if("ROB" in str(RAT.Address[int(nextInstruction.operand2[1:])])) :
                # Register has been renamed
                tempRobAddr = int(RAT.Address[int(nextInstruction.operand2[1:])][3:])
                if(ROB.Complete[tempRobAddr] == 1) :
                    # Value ready to be read
                    s1 = copy.copy(ROB.Value[tempRobAddr])
                    v1 = 0
                else :
                    # Value not ready
                    v1 = copy.copy(RAT.Address[int(nextInstruction.operand2[1:])])
            else :
                # Most up to date value has been written back & no instructions ahead of it write to same register
                s1 = copy.copy(ARF.Register[int(nextInstruction.operand2[1:])])
                v1 = 0
        else :
            # If operand 2 is a constant, get value
            s1 = int(nextInstruction.operand2)
            v1 = 0

        # Get s2 value (operand 3) if available
        if("r" in str(nextInstruction.operand3)) :
            if("ROB" in str(RAT.Address[int(nextInstruction.operand3[1:])])) :
                # Register has been renamed
                tempRobAddr = int(RAT.Address[int(nextInstruction.operand3[1:])][3:])
                if(ROB.Complete[tempRobAddr] == 1) :
                    # Value ready to be read
                    s2 = copy.copy(ROB.Value[tempRobAddr])
                    v2 = 0
                else :
                    # Value not ready
                    v2 = copy.copy(RAT.Address[int(nextInstruction.operand3[1:])])
            else :
                # Most up to date value has been written back & no instructions ahead of it write to same register
                s2 = copy.copy(ARF.Register[int(nextInstruction.operand3[1:])])
                v2 = 0
        else :
            # If operand 3 is a constant, get value
            s2 = int(nextInstruction.operand3)
            v2 = 0
        

        # Rename and update RAT
        if(nextInstruction.opCode not in self.readOnlyINSTR) :
            RAT.Address[int(nextInstruction.operand1[1:])] = copy.copy("ROB" + str(ROBindex))        # Update most recent physical address in RAT
            d1 = copy.copy("ROB" + str(ROBindex))

        # Add to correct RS
        RS[resID].Instruction.append(copy.copy(nextInstruction))
        RS[resID].Op.append(copy.copy(nextInstruction.opCode))
        RS[resID].D1.append(copy.copy(d1))
        RS[resID].V1.append(copy.copy(v1))
        RS[resID].V2.append(copy.copy(v2))
        RS[resID].S1.append(copy.copy(s1))
        RS[resID].S2.append(copy.copy(s2))
        if(resID == 2) :
            RS[resID].BranchPC.append(copy.copy(IF_DE.InstructionPC))

        # Set IF_DE to empty
        IF_DE.Empty = True

        return False, PC