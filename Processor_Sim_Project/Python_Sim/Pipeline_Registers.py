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


class DE_IS_Reg :
    def __init__(self) :
        self.empty = True
        self.Instruction = Instruction(0,0,0,0,0)
        self.TargetAddress = 0
        self.Type = -1                              # Type = 0,1,2,3 (branch, load, arithmetic, logic)

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


class IS_EX_Reg :
    # Everything is *4 as 4 EUs
    def __init__(self) :
        self.empty = [True] * 4
        self.Instruction = [Instruction(0,0,0,0,0)] * 4
        self.TargetAddress = [0] * 4
        self.Type = [-1] * 4                           # Type = 0,1,2,3 (branch, load, arithmetic, logic)

    def _empty(self, index, input=None) :
        if input is not None :
            self.empty[index] = input
        else :
            return self.empty[index]

    def _instruction(self, index, input=None) :
        if input is not None :
            self.Instruction[index] = input
        else :
            return self.Instruction[index]

    def _targetAddress(self, index, input=None) :
        if input is not None :
            self.TargetAddress[index] = input
        else :
            return self.TargetAddress[index]

    def _type(self, index, input=None) :
        if input is not None :
            self.Type[index] = input
        else :
            return self.Type[index]


class EX_WB_Reg :
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

# class DE_EX_Reg :

#     def __init__(self) :
#         self.empty = True
#         self.Instruction = Instruction(0,0,0,0,0)
#         self.TargetAddress = 0
#         self.Type = -1                              # Type = 0,1,2,3 (branch, load, arithmetic, logic)

#     def _empty(self, input=None) :
#         if input is not None :
#             self.empty = input
#         else :
#             return self.empty

#     def _instruction(self, input=None) :
#         if input is not None :
#             self.Instruction = input
#         else :
#             return self.Instruction

#     def _targetAddress(self, input=None) :
#         if input is not None :
#             self.TargetAddress = input
#         else :
#             return self.TargetAddress

#     def _type(self, input=None) :
#         if input is not None :
#             self.Type = input
#         else :
#             return self.Type