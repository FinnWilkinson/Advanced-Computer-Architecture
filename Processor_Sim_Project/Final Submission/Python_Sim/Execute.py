from Instruction import Instruction
from Register_File import *
import copy as copy

# ARITHMETIC EXECUTION UNIT
class ARITH_Execution_Unit :
    def __init__(self) :
        self.ExecutionCount = 0
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, branchPredType, correctBranchPreds, LSQ) :
        output = None
        error = 0

        # ADD
        if IS_EX[EUindex].Op == "ADD": 
            output = IS_EX[EUindex].S1 + IS_EX[EUindex].S2
        # ADDI
        elif IS_EX[EUindex].Op == "ADDI": 
            output = IS_EX[EUindex].S1 + IS_EX[EUindex].S2
        # SUB
        elif IS_EX[EUindex].Op == "SUB": 
            output = IS_EX[EUindex].S1 - IS_EX[EUindex].S2
        # SUBI
        elif IS_EX[EUindex].Op == "SUBI": 
            output = IS_EX[EUindex].S1 - IS_EX[EUindex].S2
        # MUL
        elif IS_EX[EUindex].Op == "MUL": 
            # Introduce 3 cycle latency for Multiplication
            if(self.ExecutionCount == 1) :
                output = IS_EX[EUindex].S1 * IS_EX[EUindex].S2
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # MULI
        elif IS_EX[EUindex].Op == "MULI": 
            # Introduce 3 cycle latency for Multiplication
            if(self.ExecutionCount == 1) :
                output = IS_EX[EUindex].S1 * IS_EX[EUindex].S2
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # DIV
        elif IS_EX[EUindex].Op == "DIV": 
            # Introduce 16 cycle latency for Division
            if(self.ExecutionCount == 15) :
                output = int(IS_EX[EUindex].S1 / IS_EX[EUindex].S2)
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # DIVI
        elif IS_EX[EUindex].Op == "DIVI": 
            # Introduce 16 cycle latency for Division
            if(self.ExecutionCount == 15) :
                output = int(IS_EX[EUindex].S1 / IS_EX[EUindex].S2)
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # MOD
        elif IS_EX[EUindex].Op == "MOD":
            output = IS_EX[EUindex].S1 % IS_EX[EUindex].S2
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
            error = -1
        return output, error, finished, branchTakenCount, branchExecutedCount, correctBranchPreds, PC, MEM


# LOAD / STORE EXECUTION UNIT
class LDSTR_Execution_Unit :
    def __init__(self) :
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, branchPredType, correctBranchPreds, LSQ) :
        output = None
        error = 0
        memAddress = copy.copy(IS_EX[EUindex].S1 + IS_EX[EUindex].S2)
        # LD or LDC
        if IS_EX[EUindex].Op == "LD" or IS_EX[EUindex].Op == "LDC" : 
            output = copy.copy(MEM[memAddress])
            LSQindex = LSQ.InstructionNumber.index(IS_EX[EUindex].InstructionNumber)
            LSQ.Value[LSQindex] = copy.copy(output)
            LSQ.Complete[LSQindex] = 1
        # STR or STRC
        elif IS_EX[EUindex].Op == "STR" or IS_EX[EUindex].Op == "STRC" : 
            LSQindex = LSQ.InstructionNumber.index(IS_EX[EUindex].InstructionNumber)
            LSQ.Value[LSQindex] = copy.copy(IS_EX[EUindex].D1)
            LSQ.Complete[LSQindex] = 1
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
            error = -1
        return output, error, finished, branchTakenCount, branchExecutedCount, correctBranchPreds, PC, MEM


# BRANCH / LOGIC EXECUTION UNIT
class BRLGC_Execution_Unit :
    def __init__(self) :
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, branchPredType, correctBranchPreds, LSQ) :
        output = None
        error = 0

        # HALT
        if IS_EX[EUindex].Op == "HALT":                                                     
            finished = True
        # CMP
        elif IS_EX[EUindex].Op == "CMP": 
            if(IS_EX[EUindex].S1 > IS_EX[EUindex].S2) :
                output = 1
            elif(IS_EX[EUindex].S1 == IS_EX[EUindex].S2) :
                output = 0
            elif(IS_EX[EUindex].S1 < IS_EX[EUindex].S2) :
                output = -1
        # JMP
        elif IS_EX[EUindex].Op == "JMP": 
            branchExecutedCount += 1
            branchTakenCount += 1
            if(branchPredType != 0) :
                for i in range(0, len(BIPB.BranchPC)) :
                    if(BIPB.InstructionNumber[i] == IS_EX[EUindex].InstructionNumber) :
                        if(IS_EX[EUindex].D1 == BIPB.TargetAddress[i]) :
                            # Successful Prediction
                            correctBranchPreds += 1
                        else :
                            # Unsuccessful Prediction
                            btbIndex = BTB.BranchPC.index(IS_EX[EUindex].BranchPC)
                            BTB.TargetAddress[btbIndex] = copy.copy(IS_EX[EUindex].D1)
                            PC = copy.copy(IS_EX[EUindex].D1)
                            error = 1   # Flush pipeline
                        BIPB.remove(IS_EX[EUindex].InstructionNumber)
                        break
            else :
                PC = copy.copy(IS_EX[EUindex].D1)
                error = 1   # Flush pipeline

        # BR
        elif IS_EX[EUindex].Op == "BR": 
            branchExecutedCount += 1
            branchTakenCount += 1
            if(branchPredType == 0) :
                PC = copy.copy(IS_EX[EUindex].D1)
                error = 1   # Flush pipeline
            else :
                # Correct prediction always
                correctBranchPreds += 1
                BIPB.remove(IS_EX[EUindex].InstructionNumber)

        # BEQ
        elif IS_EX[EUindex].Op == "BEQ": 
            branchExecutedCount += 1
            # No branch predictor
            if(branchPredType == 0) :
                if(IS_EX[EUindex].D1 == IS_EX[EUindex].S1) :
                    PC = copy.copy(IS_EX[EUindex].S2)
                    branchTakenCount += 1
                    error = 1   # Flush pipeline
            else :
                taken = False
                if(IS_EX[EUindex].D1 == IS_EX[EUindex].S1) :
                    branchTakenCount += 1
                    taken = True
                # Get BTB index
                btbIndex = copy.copy(BTB.BranchPC.index(IS_EX[EUindex].BranchPC))
                # Do branch
                for i in range(0, len(BIPB.BranchPC)) :
                    if(BIPB.BranchPC[i] == IS_EX[EUindex].BranchPC) :
                        if(BIPB.Prediction[i] == taken) :
                            # Successful Prediction
                            correctBranchPreds += 1
                        else :
                            # Unsuccessful Prediction
                            if(taken == True) :
                                PC = copy.copy(IS_EX[EUindex].S2)
                            else :
                                PC = copy.copy(BTB.BranchPC[btbIndex]+1)
                            error = 1   # Flush pipeline
                        BIPB.remove(IS_EX[EUindex].InstructionNumber)
                        BTB.updateResult(btbIndex, taken)
                        break
                
        # BLT
        elif IS_EX[EUindex].Op == "BLT": 
            branchExecutedCount += 1
            # No branch predictor
            if(branchPredType == 0) :
                if(IS_EX[EUindex].D1 < IS_EX[EUindex].S1) :
                    PC = copy.copy(IS_EX[EUindex].S2)
                    branchTakenCount += 1
                    error = 1   # Flush pipeline
            else :
                taken = False
                if(IS_EX[EUindex].D1 < IS_EX[EUindex].S1) :
                    branchTakenCount += 1
                    taken = True
                # Get BTB index
                btbIndex = BTB.BranchPC.index(IS_EX[EUindex].BranchPC)
                # Do branch
                for i in range(0, len(BIPB.BranchPC)) :
                    if(BIPB.BranchPC[i] == IS_EX[EUindex].BranchPC) :
                        if(BIPB.Prediction[i] == taken) :
                            # Successful Prediction
                            correctBranchPreds += 1
                        else :
                            # Unsuccessful Prediction
                            if(taken == True) :
                                PC = copy.copy(IS_EX[EUindex].S2)
                            else :
                                PC = copy.copy(BTB.BranchPC[btbIndex]+1)
                            error = 1   # Flush pipeline
                        BIPB.remove(IS_EX[EUindex].InstructionNumber)
                        BTB.updateResult(btbIndex, taken)
                        break

        # LSL
        elif IS_EX[EUindex].Op == "LSL":
            output = IS_EX[EUindex].S1 << IS_EX[EUindex].S2
        # LSR
        elif IS_EX[EUindex].Op == "LSR":
            output = IS_EX[EUindex].S1 >> IS_EX[EUindex].S2
        # XOR
        elif IS_EX[EUindex].Op == "XOR" :
            output = IS_EX[EUindex].S1 ^ IS_EX[EUindex].S2
        # AND
        elif IS_EX[EUindex].Op == "AND" :
            output = IS_EX[EUindex].S1 & IS_EX[EUindex].S2
        # PAUSE
        elif IS_EX[EUindex].Op == "PAUSE" :
            output = 1
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
            error = -1
        return output, error, finished, branchTakenCount, branchExecutedCount, correctBranchPreds, PC, MEM