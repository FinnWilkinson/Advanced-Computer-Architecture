from Instruction import Instruction
from Branch_Prediction import *
import copy as copy

class Fetch_Unit :

    def __init__(self) :
        return

    def fetchNext(self, PC, INSTR, IF_DE, instructionFetchCount, BTB, BIPB, branchPredType, nextInstructionNumber) :
        nextInstruction = INSTR[PC]
        btbIndex = -1

        # Stops program crashes due to unknown opcode after end of program
        if nextInstruction.opCode == 0 :
            #IF_DE.Empty = True
            return PC, instructionFetchCount, nextInstructionNumber

        nextInstruction.instructionNumber = copy.copy(nextInstructionNumber)
        nextInstruction.Valid = True
        IF_DE.Instruction = copy.copy(nextInstruction)
        IF_DE.InstructionPC = copy.copy(PC)

        if(branchPredType != 0) :
            # Branch Prediction Check
            for i in range(0, len(BTB.BranchPC)) :
                if(BTB.BranchPC[i] == PC) :
                    btbIndex = i
                    break

            # If seen branch PC before, predict and load into BIPB
            if(btbIndex != -1) :
                # Add branch to Branch in Pipeline Buffer
                BIPB.BranchPC.append(copy.copy(PC))
                BIPB.InstructionNumber.append(copy.copy(nextInstruction.instructionNumber))
                BIPB.Prediction.append(copy.copy(getBranchPred(branchPredType, BTB, btbIndex)))
                BIPB.TargetAddress.append(copy.copy(BTB.TargetAddress[btbIndex]))
                BIPB.InstructionType.append(" ")
                # If predicted taken, update PC
                if(getBranchPred(branchPredType, BTB, btbIndex) == True) :
                    PC = copy.copy(BTB.TargetAddress[btbIndex])
                # Otherwise, increment PC
                else :
                    PC += 1
            else :
                PC += 1
        else :
            PC += 1



        IF_DE.Empty = False
        instructionFetchCount += 1
        nextInstructionNumber += 1
            
        return PC, instructionFetchCount, nextInstructionNumber