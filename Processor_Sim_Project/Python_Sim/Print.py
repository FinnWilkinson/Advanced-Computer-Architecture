import os
import sys
import numpy as np
from Register_File import *

def printSysInfo(ARF, MEM, INSTR, RAT, PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP, branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount) :
    np.set_printoptions(threshold=sys.maxsize, linewidth=300)
    tempMEM = np.reshape(MEM, (-1, 32))
    #os.system('cls||clear')

    print("│ PC = {} │ Cycles = {} │ Instructions Fetched = {} │ Instructions Executed = {} | Instructions Executed This Cycle = {} | Average IPC = {} |" .format(PC, cycles, instructionFetchCount, instructionExecuteCount, instructionsExeThisCycle, averageILP))
    print("| Branches Executed = {} | Branches Taken = {} | Correct Branch Predictions = {} | Cycles Stalled = {} | Flushes = {} |" .format(branchExecutedCount, branchTakenCount, correctBranchPreds, stallCount, flushCount))
    print()
    print("Register Address Table :")
    print("────────────────────────")
    print("│ r0 = {} │ r1 = {} │ r2 = {} │ r3 = {} │ r4 = {} │ r5 = {} │ r6 = {} │ r7 = {} │" .format(RAT.Address[0], RAT.Address[1], RAT.Address[2], RAT.Address[3], RAT.Address[4], RAT.Address[5], RAT.Address[6], RAT.Address[7]))
    print("│ r8 = {} │ r9 = {} │ r10 = {} │ r11 = {} │ r12 = {} │ r13 = {} │ r14 = {} │ r15 = {} │" .format(RAT.Address[8], RAT.Address[9], RAT.Address[10], RAT.Address[11], RAT.Address[12], RAT.Address[13], RAT.Address[14], RAT.Address[15]))
    print("│ r16 = {} │ r17 = {} │ r18 = {} │ r19 = {} │ r20 = {} │ r21 = {} │ r22 = {} │ r23 = {} │" .format(RAT.Address[16], RAT.Address[17], RAT.Address[18], RAT.Address[19], RAT.Address[20], RAT.Address[21], RAT.Address[22], RAT.Address[23]))
    print("│ r24 = {} │ r25 = {} │ r26 = {} │ r27 = {} │ r28 = {} │ r29 = {} │ r30 = {} │ r31 = {} │" .format(RAT.Address[24], RAT.Address[25], RAT.Address[26], RAT.Address[27], RAT.Address[28], RAT.Address[29], RAT.Address[30], RAT.Address[31]))
    print()
    print("Architectural Register File :")
    print("─────────────────────────────")
    print("│ r0 = {} │ r1 = {} │ r2 = {} │ r3 = {} │ r4 = {} │ r5 = {} │ r6 = {} │ r7 = {} │" .format(ARF.Register[0], ARF.Register[1], ARF.Register[2], ARF.Register[3], ARF.Register[4], ARF.Register[5], ARF.Register[6], ARF.Register[7]))
    print("│ r8 = {} │ r9 = {} │ r10 = {} │ r11 = {} │ r12 = {} │ r13 = {} │ r14 = {} │ r15 = {} │" .format(ARF.Register[8], ARF.Register[9], ARF.Register[10], ARF.Register[11], ARF.Register[12], ARF.Register[13], ARF.Register[14], ARF.Register[15]))
    print("│ r16 = {} │ r17 = {} │ r18 = {} │ r19 = {} │ r20 = {} │ r21 = {} │ r22 = {} │ r23 = {} │" .format(ARF.Register[16], ARF.Register[17], ARF.Register[18], ARF.Register[19], ARF.Register[20], ARF.Register[21], ARF.Register[22], ARF.Register[23]))
    print("│ r24 = {} │ r25 = {} │ r26 = {} │ r27 = {} │ r28 = {} │ r29 = {} │ r30 = {} │ r31 = {} │" .format(ARF.Register[24], ARF.Register[25], ARF.Register[26], ARF.Register[27], ARF.Register[28], ARF.Register[29], ARF.Register[30], ARF.Register[31]))
    print()
    print("Main Memory - 1024 represented as 32x32 (Indecies 0 to 31 are top row):")
    print("───────────────────────────────────────────────────────────────────────")
    print(tempMEM)

    print()
    #input("Press Enter key to continue ...")


# If no file provided, print error and info
def printUsageInfo() :
    os.system('cls||clear')
    print("To execute an assembly program, please include the name of the corresponding file.")
    print()
    print("I.e.        python Simulator_main.py Vector_Addition.txt           ")
    print()
    input("Press Enter key to continue ...")