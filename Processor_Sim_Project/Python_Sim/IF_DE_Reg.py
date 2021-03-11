from Instruction import Instruction

class IF_DE_Reg :

    def __init__(self) :
        self.empty = True
        self.Instruction = Instruction(0,0,0,0,0)

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