from Instruction import Instruction
from Register_File import RegFile
from Fetch import Fetch_Unit
from Decode import Decode_Unit
from Execute import Execution_Unit

class Pipeline:

    def __init__(self) :
        self.IF_DE = None
        self.DE_EX = None

        self.fetchUnit = Fetch_Unit()
        self.decodeUnit = Decode_Unit()
        self.executionUnit = Execution_Unit()
    
    def advance(self) :
        # Advance back to front to ensure pipeline can progress
        return