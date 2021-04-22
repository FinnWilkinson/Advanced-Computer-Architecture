from Instruction import Instruction
from Branch_Prediction import *
import copy as copy

class Fetch_Unit :

    def __init__(self) :
        return

    def fetchNext(self, PC, INSTR, IF_DE, instructionFetchCount, BTB, BIPB, branchPredType) :
        nextInstruction = INSTR[PC]
        btbIndex = -1

        # Stops program crashes due to unknown opcode after end of program
        if nextInstruction.opCode == 0 :
            IF_DE.Empty = True
            return PC, instructionFetchCount

        nextInstruction.instructionNumber = copy.copy(instructionFetchCount)
        nextInstruction.Valid = True
        IF_DE.Instruction = copy.copy(nextInstruction)
        IF_DE.InstructionPC = copy.copy(PC)

        if(branchPredType != 0) :
            # Branch Prediction Check
            for i in range(0, len(BTB.BranchPC)) :
                if(BTB.BranchPC[i] == PC) :
                    btbIndex = i
                    break

            # Branch prediction target address
            if(btbIndex != -1) :
                # Add branch to Branch in Pipeline Buffer
                BIPB.BranchPC.append(copy.copy(PC))
                BIPB.InstructionNumber.append(copy.copy(nextInstruction.instructionNumber))
                BIPB.Prediction.append(copy.copy(getBranchPred(branchPredType, BTB, btbIndex)))
                if(getBranchPred(branchPredType, BTB, btbIndex) == True) :
                    PC = copy.copy(BTB.TargetAddress[btbIndex])
                else :
                    PC += 1
            else :
                PC += 1
        else :
            PC += 1



        IF_DE.Empty = False
        instructionFetchCount += 1
            
        return PC, instructionFetchCount