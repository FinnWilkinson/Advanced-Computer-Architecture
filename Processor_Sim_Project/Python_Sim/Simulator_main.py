from Instruction import Instruction
from Register_File import *
from Pipeline import Pipeline
from Print import *
from Load_Assembly import *
from Pipeline_Registers import *
from Branch_Prediction import *
from Write_Back import *

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
INSTR = [Instruction(0,0,0,0,0)] * 1024     # Instruction memory

ROB = ReOrderBuffer()                       # Global Re-order Buffer
RAT = RegAddrTable()                        # Global Register Address Table

BIPB = BranchPipelineBuffer()               # Global Branch in Pipeline Buffer
BTB = BranchTargetBuffer()                  # Gloabl Branch Target Buffer
LSQ = LoadStoreQueue()                      # Global Load / Store Queue

pipelines = [Pipeline(), Pipeline(), Pipeline(), Pipeline()]

writeBackUnit = Write_Back_Unit()

# Flush processor after branch mispredict
def flushAll(flushOutput, nextInstructionNumber, flushCount,) :
    

    return nextInstructionNumber



if __name__=="__main__" :
    # Ensure file name was provided
    if len(sys.argv) < 2:
        printUsageInfo()
        sys.exit(0)
    
    # Load the instructions into memory
    loadProgram(sys.argv[1], INSTR)

    # Initialise values
    pipelineCount = 1
    branchPredType = 0                      # 0 = Off (default), 1 = Fixed, 2 = Static, 3 = 1-bit dynamic, 4 = 2-bit dynamic
    error = 0
    nextInstructionNumber = 0


    # Get number of pipelines used
    if("--2Way" in sys.argv) :
        pipelineCount = 2
        # Needs defualt of Fixed branch prediction to work
        branchPredType = 1
    if("--4Way" in sys.argv) :
        pipelineCount = 4
        # Needs defualt of Fixed branch prediction to work
        branchPredType = 1


    # Get branch prediction type
    if("--BPFixed" in sys.argv) :
        branchPredType = 1
    if("--BPStatic" in sys.argv) :
        branchPredType = 2
    if("--BPDynamic1" in sys.argv) :
        branchPredType = 3
    if("--BPDynamic2" in sys.argv) :
        branchPredType = 4
    
    # Effective clock, used to advance the pipelines
    while not finished :
        instructionsExeThisCycle = instructionExecuteCount
        stallThisCycle = [False, False, False, False]

        # WRITE BACK
        for w in range(0, pipelineCount) :
            writeBackUnit.writeBack(pipelines, pipelineCount, ROB, RAT, ARF, BIPB)    # ROB write back
            writeBackUnit.LSQCommit(LSQ, MEM, BIPB)                                   # LSQ write back

        # EXECUTE
        for e in range(0, pipelineCount) :
            #print(e)
            flushOutput = -1
            error, finished, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, flushOutput, PC, MEM = pipelines[e].execute(error, finished, instructionExecuteCount, branchExecutedCount, branchTakenCount, correctBranchPreds, branchPredType, flushOutput, pipelines, pipelineCount, PC, MEM, ARF, ROB, BTB, BIPB, LSQ)
            # Check if opCode error
            if(error == -1) :
                sys.exit(1)
            # Check if program finished
            if(finished == True) :
                break

            # Check for flush
            if(error == 1) :
                # Flush Pipelines
                for f in range(0, pipelineCount) :
                    nextInstructionNumber = pipelines[f].flush(flushOutput, nextInstructionNumber)
                # Flush ROB and re-assign RAT values
                ROB.flush(flushOutput, RAT)
                # Flush LSQ
                LSQ.flush(flushOutput)
                # Flush BIPB
                BIPB.flush(flushOutput)

                # Increase Flush Count
                flushCount += 1
                # Re-set error + flush output
                flushOutput = -1
                error = 0
            
            # Check if program finished
            if(finished) :
                break

        # ISSUE
        for i in range(0, pipelineCount) :
            stallThisCycle[i] = pipelines[i].issue(pipelines, pipelineCount, branchPredType, stallThisCycle[i], instructionFetchCount, ARF, ROB, LSQ)


        # DECODE - Instructions need to be re-named in order
        pipelineDecodeVals = []
        # Get all instructions to decode next and sort into assending order
        for d in range(0, pipelineCount) :
            pipelineDecodeVals.append((pipelines[d].IF_DE.Instruction.instructionNumber, d))
        pipelineDecodeVals.sort()
        # Execute Decode in program order
        for d in pipelineDecodeVals :
            tempStallIndicatorDE = False
            tempStallIndicatorDE, PC, needToFlush, flushOutput = pipelines[d[1]].decode(branchPredType, tempStallIndicatorDE, instructionFetchCount, PC, ARF, RAT, ROB, BTB, BIPB, LSQ)
            # Check if BTB updated, prediction made and so need to flush
            if(needToFlush == True) :
                # Flush Pipelines
                for f in range(0, pipelineCount) :
                    nextInstructionNumber = pipelines[f].flush(flushOutput, nextInstructionNumber)
                # Flush ROB and re-assign RAT values
                ROB.flush(flushOutput, RAT)
                # Flush LSQ
                LSQ.flush(flushOutput)
                # Flush BIPB
                BIPB.flush(flushOutput)

                # Re-set error + flush output
                flushOutput = -1
            # If come back stalled, dont try decode any others
            if(tempStallIndicatorDE == True) :
                stallThisCycle[d[1]] = copy.copy(tempStallIndicatorDE or True)
                break
            

        # FETCH
        for f in range(0, pipelineCount) :
            instructionFetchCount, nextInstructionNumber, PC = pipelines[f].fetch(instructionFetchCount, nextInstructionNumber, branchPredType, PC, INSTR, BTB, BIPB)

        # Check if stall in pipelines
        for s in range(0, pipelineCount) :
            if(stallThisCycle[s] == True) :
                stallCount += 1

        # Update values
        cycles += 1
        instructionsExeThisCycle = instructionExecuteCount - instructionsExeThisCycle
        averageILP = round(instructionExecuteCount / cycles, 2)

        # Check for verbose printing
        if(len(sys.argv) > 2 and "--Verbose" in sys.argv) :
            printSysInfo(ARF, MEM, INSTR, RAT, PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount)


    # Print final system information
    printSysInfo(ARF, MEM, INSTR, RAT, PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount)
