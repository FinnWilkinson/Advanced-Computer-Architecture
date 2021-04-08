from Instruction import Instruction

class IF_DE_Reg :
    def __init__(self) :
        self.Empty = True
        self.Instruction = Instruction(0,0,0,0,0)
        self.TargetAddress = 0                      # Used for branch target address


class ReservationStation :
    def __init__(self) :
        self.Instruction = list()
        self.TargetAddress = list()     # Used for branch target address
        self.Q1 = list()                # Reservation station index that will produce s1. Value of 0 = s1 available
        self.Q2 = list()                # Reservation station index that will produce s2. Value of 0 = s2 available
        self.Q3 = list()                # Reservation station index that will produce s2. Value of 0 = s3 available
        self.Busy = 0                   # Accompanying EU(s) occupied, 0 = Free, 1 = Busy
    
    def flush(self, instructionNumber) :
        for j in range(0, len(self.Instruction)) :
            if self.Instruction[j].instructionNumber > instructionNumber :
                self.Instruction[j].Valid = False

class IS_EX_Reg :
    # Everything is *4 as 4 EUs
    def __init__(self) :
        self.Empty = [True] * 4
        self.Instruction = [Instruction(0,0,0,0,0)] * 4
        self.TargetAddress = [0] * 4                   # Used for branch target address

class ReOrderBuffer :
    def __init__(self) :
        self.Instruction = list()
        self.Value = list()
