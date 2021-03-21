from Instruction import Instruction
from Register_File import RegFile
from Pipeline import Pipeline
from Print import *
from Load_Assembly import *
#from Fetch import *
#from Decode import *
#from Execute import *

# Global values
finished = False
cycles = 0
instructionFetchCount = 0
instructionExecuteCount = 0
PC = 0
branchExecutedCount = 0
branchTakenCount = 0
correctBranchPreds = 0
stallCount = 0
instructionsExeThisCycle = 0
averageILP = 0.0

RF = RegFile()                            # Register file. RF[0] or r0 is always = 0
MEM = [0] * 1024                          # Data memory
INSTR = [Instruction(0,0,0,0,0)] * 512    # Instruction memory

pipeline_0 = Pipeline()

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

    #Effective clock, advancing pipeline
    while not finished :
        if(len(sys.argv) > 2 and sys.argv[2] == "-verbose") :
            # Print initial system information at users discretion
            printSysInfo(RF, MEM, INSTR, PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount)
        instructionsExeThisCycle = instructionExecuteCount
        PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, finished, RF, MEM, error = pipeline_0.advance(PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount, finished, RF, MEM, INSTR, error)
        cycles += 1
        instructionsExeThisCycle = instructionExecuteCount - instructionsExeThisCycle
        averageILP = round(instructionExecuteCount / cycles, 2)

        # If instruction not recognised, quit
        if error != 0 :
            sys.exit(1)

    # Print final system information
    printSysInfo(RF, MEM, INSTR, PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount)