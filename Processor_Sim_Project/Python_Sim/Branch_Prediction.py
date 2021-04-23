import copy as copy

def getBranchPred(branchPredType, BTB, btbIndex) :
        if(branchPredType == 1) :
            # Fixed - Always predict branch is taken
            return True
        elif(branchPredType == 2) :
            # Static - Branch taken if backward, not taken if forwards
            return True
        elif(branchPredType == 3) :
            # Dynamic 1-bit - look at previous time this branch was executed
            return True
        elif(branchPredType == 4) :
            # Dynamic 2-bit - look at previous 2 times this branch was executed
            return True

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
        self.TargetAddress = []
        self.LastResult = []

    def updateResult(self, index, result) :
        listTemp = copy.copy(list(self.LastResult[index]))
        temp = copy.copy(listTemp[0])
        listTemp[1] = copy.copy(temp)
        listTemp[0] = copy.copy(result)
        self.LastResult[index] = copy.copy(tuple(listTemp))
