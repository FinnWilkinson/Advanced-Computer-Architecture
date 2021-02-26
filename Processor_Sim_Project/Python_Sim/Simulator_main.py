from Instruction import Instruction
from Print import *
from Load_Assembly import *
from Fetch import *
from Decode import *
from Execute import *

# Global values
finished = False
cycles = 0
instructionFetchCount = 0
instructionExecuteCount = 0
PC = 0

RF = [0] * 32           # Register file. RF[0] or r0 is always = 0
MEM = [0] * 1024        # Data memory
INSTR = [Instruction(0,0,0,0,0)] * 512    # Instruction memory

if __name__=="__main__" :
    # Ensure file name was provided
    if len(sys.argv) < 2:
        printUsageInfo()
        sys.exit(0)
    
    # Load the instructions into memory
    loadProgram(sys.argv[1], INSTR)

    # Initialise values
    error = 0
    nextInstruction = None
    targetAddress = 0

    # Effective Clock
    while not finished :
        # Print initial system information
        printSysInfo(RF, MEM, INSTR, PC, cycles, instructionFetchCount, instructionExecuteCount)

        nextInstruction, instructionFetchCount, cycles, PC = fetchNext(INSTR, instructionFetchCount, cycles, PC)
        targetAddress, cycles = decodeInstruction(RF, cycles, nextInstruction)
        error, PC, cycles, instructionExecuteCount, finished = executeInstruction(nextInstruction.opCode, nextInstruction.operand1, nextInstruction.operand2, nextInstruction.operand3, targetAddress, RF, MEM, PC, cycles, instructionExecuteCount, finished)
        if error != 0 :
            sys.exit(1)
    
    # Print final system information
    printSysInfo(RF, MEM, INSTR, PC, cycles, instructionFetchCount, instructionExecuteCount)