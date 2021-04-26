from Instruction import Instruction
from Register_File import *
from Pipeline import Pipeline
from Print import *
from Load_Assembly import *
from Pipeline_Registers import *
from Branch_Prediction import *

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
flushCount = 0
instructionsExeThisCycle = 0
averageILP = 0.0

ARF = ARegFile()                            # Register file. ARF[0] or r0 is always = 0
MEM = [0] * 1024                            # Data memory
INSTR = [Instruction(0,0,0,0,0)] * 512      # Instruction memory

ROB = ReOrderBuffer()                       # Global Re-order Buffer
RAT = RegAddrTable()                        # Global Register Address Table

BIPB = BranchPipelineBuffer()               # Global Branch in Pipeline Buffer
BTB = BranchTargetBuffer()                  # Gloabl Branch Target Buffer
LSQ = LoadStoreQueue()                      # Global Load / Store Queue

#pipeline_0 = Pipeline()
pipelines = [Pipeline(), Pipeline(), Pipeline(), Pipeline()]


if __name__=="__main__" :
    # Ensure file name was provided
    if len(sys.argv) < 2:
        printUsageInfo()
        sys.exit(0)
    
    # Load the instructions into memory
    loadProgram(sys.argv[1], INSTR)

    # Initialise values
    error = 0
    nextInstructionNumber = 0


    # Get branch prediction type
    branchPredType = 0                      # 0 = Off (default), 1 = Fixed, 2 = Static, 3 = 1-bit dynamic, 4 = 2-bit dynamic
    if("--BPFixed" in sys.argv) :
        branchPredType = 1
    if("--BPStatic" in sys.argv) :
        branchPredType = 2
    if("--BPDynamic1" in sys.argv) :
        branchPredType = 3
    if("--BPDynamic2" in sys.argv) :
        branchPredType = 4

    # Get number of pipelines used
    pipelineCount = 1
    if("--2Way" in sys.argv) :
        pipelineCount = 2
    if("--4Way" in sys.argv) :
        pipelineCount = 4
    

    #Effective clock, advancing pipeline
    while not finished :
        instructionsExeThisCycle = instructionExecuteCount

        for i in range(0, pipelineCount) :
            #print("pipeline " + str(i))
            PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount, finished, ARF, MEM, ROB, RAT, BIPB, BTB, LSQ, error, pipelines, nextInstructionNumber = pipelines[i].advance(PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount, finished, ARF, MEM, INSTR, ROB, RAT, BIPB, BTB, LSQ, branchPredType, error, pipelines, pipelineCount, nextInstructionNumber)

        #PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount, finished, ARF, MEM, ROB, RAT, BIPB, BTB, LSQ, error, instructionToFlush = pipeline_0.advance(PC, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount, finished, ARF, MEM, INSTR, ROB, RAT, BIPB, BTB, LSQ, branchPredType, error, instructionToFlush)
        cycles += 1
        instructionsExeThisCycle = instructionExecuteCount - instructionsExeThisCycle
        averageILP = round(instructionExecuteCount / cycles, 2)

        if(len(sys.argv) > 2 and "--verbose" in sys.argv) :
            # Print initial system information at users discretion
            printSysInfo(ARF, MEM, INSTR, RAT, PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount)
        

        # If instruction not recognised, quit
        if error != 0 :
            sys.exit(1)

    # Print final system information
    printSysInfo(ARF, MEM, INSTR, RAT, PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount)