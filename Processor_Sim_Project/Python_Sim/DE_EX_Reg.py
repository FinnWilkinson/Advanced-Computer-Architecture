from Instruction import Instruction

class DE_EX_Reg :

    def __init__(self) :
        self.empty = True
        self.Instruction = Instruction(0,0,0,0,0)
        self.TargetAddress = 0
        self.Type = -1                              # Type = 0,1,2 (branch, load, arithmetic)

    def _empty(self, input=None) :
        if input is not None :
            self.empty = input
        else :
            return self.empty

    def _instruction(self, input=None) :
        if input is not None :
            self.Instruction = input
        else :
            return self.Instruction

    def _targetAddress(self, input=None) :
        if input is not None :
            self.TargetAddress = input
        else :
            return self.TargetAddress

    def _type(self, input=None) :
        if input is not None :
            self.Type = input
        else :
            return self.Type