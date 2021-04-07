import os
import sys
import numpy as np
from Register_File import *
from Reg_To_Reg_Index import *

def printSysInfo(ARF, MEM, INSTR, PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount) :
    np.set_printoptions(threshold=sys.maxsize, linewidth=300)
    tempMEM = np.reshape(MEM, (-1, 32))
    os.system('cls||clear')

    print("│ PC = {} │ Cycles = {} │ Instructions Fetched = {} │ Instructions Executed = {} | Instructions Executed This Cycle = {} | Average ILP = {} |" .format(PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP))
    print("| Branches Executed = {} | Branches Taken = {} | Correct Branch Predictions = {} | Cycles Stalled = {} | Flushes = {} |" .format(branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount))
    print()
    print("Architectural Register File :")
    print("────────────────")
    print("│ r0 = {} │ r1 = {} │ r2 = {} │ r3 = {} │ r4 = {} │ r5 = {} │ r6 ={} │ r7 = {} │" .format(ARF.Register[regToRegIndex("r0")], ARF.Register[regToRegIndex("r1")], ARF.Register[regToRegIndex("r2")], ARF.Register[regToRegIndex("r3")], ARF.Register[regToRegIndex("r4")], ARF.Register[regToRegIndex("r5")], ARF.Register[regToRegIndex("r6")], ARF.Register[regToRegIndex("r7")]))
    print("│ r8 = {} │ r9 = {} │ r10 = {} │ r11 = {} │ r12 = {} │ r13 = {} │ r14 ={} │ r15 = {} │" .format(ARF.Register[regToRegIndex("r8")], ARF.Register[regToRegIndex("r9")], ARF.Register[regToRegIndex("r10")], ARF.Register[regToRegIndex("r11")], ARF.Register[regToRegIndex("r12")], ARF.Register[regToRegIndex("r13")], ARF.Register[regToRegIndex("r14")], ARF.Register[regToRegIndex("r15")]))
    print("│ r16 = {} │ r17 = {} │ r18 = {} │ r19 = {} │ r20 = {} │ r21 = {} │ r22 ={} │ r23 = {} │" .format(ARF.Register[regToRegIndex("r16")], ARF.Register[regToRegIndex("r17")], ARF.Register[regToRegIndex("r18")], ARF.Register[regToRegIndex("r19")], ARF.Register[regToRegIndex("r20")], ARF.Register[regToRegIndex("r21")], ARF.Register[regToRegIndex("r22")], ARF.Register[regToRegIndex("r23")]))
    print("│ r24 = {} │ r25 = {} │ r26 = {} │ r27 = {} │ r28 = {} │ r29 = {} │ r30 ={} │ r31 = {} │" .format(ARF.Register[regToRegIndex("r24")], ARF.Register[regToRegIndex("r25")], ARF.Register[regToRegIndex("r26")], ARF.Register[regToRegIndex("r27")], ARF.Register[regToRegIndex("r28")], ARF.Register[regToRegIndex("r29")], ARF.Register[regToRegIndex("r30")], ARF.Register[regToRegIndex("r31")]))
    print()
    print("Main Memory - 1024 represented as 32x32 (Indecies 0 to 31 are top row):")
    print("────────────────────────────────────────────────────────────────────────")
    print(tempMEM)

    print()
    input("Press Enter key to continue ...")


# If no file provided, print error and info
def printUsageInfo() :
    os.system('cls||clear')
    print("To execute an assembly program, please include the name of the corresponding file.")
    print()
    print("I.e.        python Simulator_main.py Vector_Addition.txt           ")
    print()
    input("Press Enter key to continue ...")