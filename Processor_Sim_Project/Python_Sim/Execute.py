from Instruction import Instruction
from Register_File import *
import copy as copy

# ARITHMETIC EXECUTION UNIT
class ARITH_Execution_Unit :
    def __init__(self) :
        self.ExecutionCount = 0
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, MWB, branchPredType, correctBranchPreds) :
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
            if(self.ExecutionCount == 2) :
                output = IS_EX[EUindex].S1 * IS_EX[EUindex].S2
                self.ExecutionCount = 0     # Re-set execution count
            else :
                error = 2       # Cycle delay occured
                self.ExecutionCount += 1
        # MULI
        elif IS_EX[EUindex].Op == "MULI": 
            # Introduce 3 cycle latency for Multiplication
            if(self.ExecutionCount == 2) :
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
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
            error = -1
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output, correctBranchPreds


# LOAD / STORE EXECUTION UNIT
class LDSTR_Execution_Unit :
    def __init__(self) :
        self.ExecutionCount = 0
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, MWB, branchPredType, correctBranchPreds) :
        output = None
        error = 0

        # Introduce 2 cycle latency for Load and Stores (Replicating L1 cache latency)
        if(self.ExecutionCount == 1) :
            memAddress = copy.copy(IS_EX[EUindex].S1 + IS_EX[EUindex].S2)
            # No branch prediction
            if(branchPredType == 0) :
                # LD or LDC
                if IS_EX[EUindex].Op == "LD" or IS_EX[EUindex].Op == "LDC" : 
                    output = copy.copy(MEM[memAddress])
                # STR or STRC
                elif IS_EX[EUindex].Op == "STR" or IS_EX[EUindex].Op == "STRC" : 
                    MEM[memAddress] = copy.copy(IS_EX[EUindex].D1)
                # Opcode not recognised
                else: 
                    print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
                    error = -1
            # Branch prediction version
            else :
                writeToMem = True
                branchIN = 0
                # Check if we need to check Memory writeback buffer
                for i in range(0, len(BIPB.InstructionNumber)) :
                    if(IS_EX[EUindex].InstructionNumber < BIPB.InstructionNumber[i]) :
                        if(i > 0) :
                            writeToMem = False
                            branchIN = copy.copy(BIPB.InstructionNumber[i-1])
                        break

                # LD or LDC
                if IS_EX[EUindex].Op == "LD" or IS_EX[EUindex].Op == "LDC" : 
                    if(writeToMem == True) :
                        output = copy.copy(MEM[memAddress])
                    else :
                        lowerIndex = -1
                        higherIndex = -1
                        # Get index of store instruction after this LD (if it exists)
                        for i in range(0, len(MWB.InstructionNumber)) :
                            if(IS_EX[EUindex].InstructionNumber < MWB.InstructionNumber[i] and MWB.MemoryAddress[i] == memAddress) :
                                higherIndex = copy.copy(i)
                                break
                            if(IS_EX[EUindex].InstructionNumber > MWB.InstructionNumber[i] and MWB.MemoryAddress[i] == memAddress) :
                                lowerIndex = copy.copy(i)

                        # Read from memory
                        if(higherIndex == 0 or lowerIndex == -1) :
                            output = copy.copy(MEM[memAddress])
                        else :
                            output = copy.copy(MWB.Value[lowerIndex])
                # STR or STRC
                elif IS_EX[EUindex].Op == "STR" or IS_EX[EUindex].Op == "STRC" : 
                    if(writeToMem == True) :
                        MEM[memAddress] = copy.copy(IS_EX[EUindex].D1)
                    else :
                        MWB.MemoryAddress.append(copy.copy(memAddress))
                        MWB.Value.append(copy.copy(IS_EX[EUindex].D1))
                        MWB.InstructionNumber.append(copy.copy(IS_EX[EUindex].InstructionNumber))
                        MWB.BranchInstructionNumber.append(copy.copy(branchIN))
                # Opcode not recognised
                else: 
                    print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
                    error = -1

            self.ExecutionCount = 0     # Re-set execution count

        else :
            self.ExecutionCount += 1
            error = 2   # Cycle delay occured
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output, correctBranchPreds


# BRANCH / LOGIC EXECUTION UNIT
class BRLGC_Execution_Unit :
    def __init__(self) :
        return

    def executeInstruction(self, IS_EX, EUindex, ARF, MEM, PC, finished, branchExecutedCount, branchTakenCount, BIPB, BTB, MWB, branchPredType, correctBranchPreds) :
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
                for i in range(0, len(BTB.BranchPC)) :
                    if(BTB.BranchPC[i] == IS_EX[EUindex].BranchPC) :
                        if(IS_EX[EUindex].D1 == BTB.TargetAddress[i]) :
                            # Successful Prediction
                            correctBranchPreds += 1
                            MEM = MWB.commit(IS_EX[EUindex].InstructionNumber, MEM)
                        else :
                            # Unsuccessful Prediction
                            BTB.TargetAddress[i] = copy.copy(IS_EX[EUindex].D1)
                            MWB.remove(IS_EX[EUindex].InstructionNumber)
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
                PC = IS_EX[EUindex].D1
                error = 1   # Flush pipeline
            else :
                # Correct prediction always
                correctBranchPreds += 1
                MEM = MWB.commit(IS_EX[EUindex].InstructionNumber, MEM)
                BIPB.remove(IS_EX[EUindex].InstructionNumber)

        # BEQ
        elif IS_EX[EUindex].Op == "BEQ": 
            branchExecutedCount += 1
            if(branchPredType == 0) :
                if(IS_EX[EUindex].D1 == IS_EX[EUindex].S1) :
                    PC = IS_EX[EUindex].S2
                    branchTakenCount += 1
                    error = 1   # Flush pipeline
            else :
                taken = False
                if(IS_EX[EUindex].D1 == IS_EX[EUindex].S1) :
                    branchTakenCount += 1
                    taken = True
                # Get BTB index
                btbIndex = 0
                for k in range(0, len(BTB.BranchPC)) :
                    if(BTB.BranchPC[k] == IS_EX[EUindex].BranchPC) :
                        btbIndex = k
                        break
                # Do branch
                for i in range(0, len(BIPB.BranchPC)) :
                    if(BIPB.BranchPC[i] == IS_EX[EUindex].BranchPC) :
                        if(BIPB.Prediction[i] == taken) :
                            # Successful Prediction
                            correctBranchPreds += 1
                            MEM = MWB.commit(IS_EX[EUindex].InstructionNumber, MEM)
                        else :
                            # Unsuccessful Prediction
                            MWB.remove(IS_EX[EUindex].InstructionNumber)
                            PC = copy.copy(BTB.BranchPC[btbIndex] + 1)
                            error = 1   # Flush pipeline
                        BIPB.remove(IS_EX[EUindex].InstructionNumber)
                        BTB.updateResult(btbIndex, taken)
                        break
                
        # BLT
        elif IS_EX[EUindex].Op == "BLT": 
            branchExecutedCount += 1
            if(branchPredType == 0) :
                if(IS_EX[EUindex].D1 < IS_EX[EUindex].S1) :
                    PC = IS_EX[EUindex].S2
                    branchTakenCount += 1
                    error = 1   # Flush pipeline
            else :
                taken = False
                if(IS_EX[EUindex].D1 < IS_EX[EUindex].S1) :
                    branchTakenCount += 1
                    taken = True
                # Get BTB index
                btbIndex = 0
                for k in range(0, len(BTB.BranchPC)) :
                    if(BTB.BranchPC[k] == IS_EX[EUindex].BranchPC) :
                        btbIndex = k
                        break
                # Do branch
                for i in range(0, len(BIPB.BranchPC)) :
                    if(BIPB.BranchPC[i] == IS_EX[EUindex].BranchPC) :
                        if(BIPB.Prediction[i] == taken) :
                            # Successful Prediction
                            correctBranchPreds += 1
                            MEM = MWB.commit(IS_EX[EUindex].InstructionNumber, MEM)
                        else :
                            # Unsuccessful Prediction
                            MWB.remove(IS_EX[EUindex].InstructionNumber)
                            PC = copy.copy(BTB.BranchPC[btbIndex] + 1)
                            error = 1   # Flush pipeline
                        BIPB.remove(IS_EX[EUindex].InstructionNumber)
                        BTB.updateResult(btbIndex, taken)
                        break

        #LSL
        elif IS_EX[EUindex].Op == "LSL":
            output = IS_EX[EUindex].S1 << IS_EX[EUindex].S2
        #LSR
        elif IS_EX[EUindex].Op == "LSR":
            output = IS_EX[EUindex].S1 >> IS_EX[EUindex].S2
        #XOR
        elif IS_EX[EUindex].Op == "XOR" :
            output = IS_EX[EUindex].S1 ^ IS_EX[EUindex].S2
        #AND
        elif IS_EX[EUindex].Op == "AND" :
            output = IS_EX[EUindex].S1 & IS_EX[EUindex].S2
        # Opcode not recognised
        else: 
            print("ERROR - Opcode '{}' not recognised. Exiting..." .format(IS_EX[EUindex].Op))
            error = -1
        return error, PC, finished, branchExecutedCount, branchTakenCount, MEM, output, correctBranchPreds