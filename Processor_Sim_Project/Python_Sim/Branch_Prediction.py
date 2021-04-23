import copy as copy

def getBranchPred(branchPredType, BTB, btbIndex) :
        # For BR and JMP, always taken an unconditional
        if(BTB.BranchType[btbIndex] == "BR" or BTB.BranchType[btbIndex] == "JMP") :
            return True

        # Fixed - Always predict branch is taken
        if(branchPredType == 1) :
            return True
        # Static - always taken if branching backwards
        elif(branchPredType == 2) :
            if(BTB.TargetAddress[btbIndex] < BTB.BranchPC[btbIndex]) :
                return True
            else :
                return False
        # Dynamic 1-bit - look at previous time this branch was executed
        elif(branchPredType == 3) :
            return BTB.LastResult[btbIndex]
        # Dynamic 2-bit - look at previous 2 times this branch was executed
        elif(branchPredType == 4) :
            # Dynamic 2-bit - look at previous 2 times this branch was executed
            if(BTB.Last2Result[btbIndex] == 3 or BTB.Last2Result[btbIndex] == 2) :
                return True
            else :
                return False
        # Default = Fixed
        return True

class BranchPipelineBuffer :
    def __init__(self) :
        self.BranchPC = []
        self.InstructionNumber = []
        self.Prediction = []       

    def remove(self, BranchInstructionNumber) :
        for i in range(0, len(self.BranchPC)) :
            if(self.InstructionNumber[i] == BranchInstructionNumber) :
                self.BranchPC.pop(i)
                self.InstructionNumber.pop(i)
                self.Prediction.pop(i)
                break


class BranchTargetBuffer :
    def __init__(self) :
        self.BranchPC = []
        self.BranchType = []
        self.TargetAddress = []
        self.LastResult = []        # Either True or False (taken, not taken)
        self.Last2Result = []       # 3 = Taken-Strong, 2 = Taken-Weak, 1 = Not-Taken-Weak, 0 = Not-Taken-Strong 

    def updateResult(self, index, result) :
        self.LastResult[index] = copy.copy(result)

        if(result == True) :
            if(self.Last2Result[index] < 3) :
                self.Last2Result[index] += 1
        else :
            if(self.Last2Result[index] > 0) :
                self.Last2Result[index] -= 1
