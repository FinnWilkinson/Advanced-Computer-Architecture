from Instruction import Instruction

class IF_DE_Reg :
    def __init__(self) :
        self.Empty = True
        self.Instruction = Instruction(0,0,0,0,0)
        self.TargetAddress = 0                      # Used for branch target address


class DE_IS_Reg :
    def __init__(self) :
        self.Empty = True
        self.Instruction = Instruction(0,0,0,0,0)
        self.TargetAddress = 0                      # Used for branch target address
        self.Type = -1                              # Type = 0,1,2,3 (branch, load, arithmetic, logic)


class ReservationStation :
    def __init__(self) :
        self.Instruction = list()
        self.Op = list()                # Operation to perform on operands
        self.S1 = list()                # Operand 1
        self.S2 = list()                # Operand 2
        self.S3 = list()                # Operand 3
        self.Q2 = list()                # Reservation station index that will produce s2. Value of 0 = s2 available
        self.Q3 = list()                # Reservation station index that will produce s2. Value of 0 = s3 available
        self.Busy = 0                   # Accompanying EU(s) occupied


class IS_EX_Reg :
    # Everything is *4 as 4 EUs
    def __init__(self) :
        self.Empty = [True] * 4
        self.Instruction = [Instruction(0,0,0,0,0)] * 4
        self.TargetAddress = [0] * 4                   # Used for branch target address
        self.Type = [-1] * 4                           # Type = 0,1,2,3 (branch, load, arithmetic, logic)


class EX_WB_Reg :
    def __init__(self) :
        self.Empty = True
        self.Instruction = Instruction(0,0,0,0,0)