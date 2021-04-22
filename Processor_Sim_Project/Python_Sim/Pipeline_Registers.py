from Instruction import Instruction

class IF_DE_Reg :
    def __init__(self) :
        self.Empty = True
        self.Instruction = Instruction(0,0,0,0,0)
        self.InstructionPC = 0


class ReservationStation :
    def __init__(self) :
        self.Instruction = list()
        self.BranchPC = list()
        self.Op = list()                # Operation used on s1, s2
        self.D1 = list()                # Destination ROB address OR if read only instruction, value at address operand1
        self.V1 = list()                # 0 if value in S1 is correct, otherwise ROB address
        self.V2 = list()                # 0 if value in S2 is correct, otherwise ROB address
        self.S1 = list()                # Operand 2
        self.S2 = list()                # Operand 3


class IS_EX_Reg :
    def __init__(self) :
        self.Empty = True
        self.InstructionNumber = 0  # Instruction sequence number of instruction
        self.BranchPC = 0           # PC of branch (if applicable)
        self.Op = ""                # Operation used on s1, s2
        self.D1 = ""                # Destination address
        self.S1 = 0                 # Operand 1
        self.S2 = 0                 # Operand 2


class ReOrderBuffer :
    def __init__(self) :
        self.Register = [" "] * 128
        self.InstructionNumber = [0] * 128
        self.Value = [0] * 128
        self.Complete = [0] * 128   # 0 = not completed, 1 = completed
        self.CommitPtr = 0          # Points to index to write back to ARF next
        self.IssuePtr = 0           # Points to index to assign instruction to next


class RegAddrTable :
    def __init__(self) :
        # Index of address = corresponding register in ARF i.e. index 3 = r3 address
        # Initialised to point to ARF locations 
        self.Address = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15", "r16", "r17", "r18", "r19", "r20", "r21", "r22", "r23", "r24", "r25", "r26", "r27", "r28", "r29", "r30", "r31"]