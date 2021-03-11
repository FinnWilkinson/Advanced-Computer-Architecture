import os
import sys
import numpy as np
from Register_File import RegFile

def printSysInfo(RF, MEM, INSTR, PC, cycles, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount) :
    np.set_printoptions(threshold=sys.maxsize, linewidth=300)
    tempMEM = np.reshape(MEM, (-1, 32))
    os.system('cls||clear')

    print("│ PC = {} │ Cycles = {} │ Instructions Fetched = {} │ Instructions Executed = {} | Branches Executed = {} | Branches Taken = {} | Stalls = {}" .format(PC, cycles, instructionFetchCount, instructionExecuteCount, branchExecutedCount, branchTakenCount, stallCount))
    print()
    print("Register File :")
    print("────────────────")
    print("│ r0 = {} │ r1 = {} │ r2 = {} │ r3 = {} │ r4 = {} │ r5 = {} │ r6 ={} │ r7 = {} │" .format(RF.Get("r0"), RF.Get("r1"), RF.Get("r2"), RF.Get("r3"), RF.Get("r4"), RF.Get("r5"), RF.Get("r6"), RF.Get("r7")))
    print("│ r8 = {} │ r9 = {} │ r10 = {} │ r11 = {} │ r12 = {} │ r13 = {} │ r14 ={} │ r15 = {} │" .format(RF.Get("r8"), RF.Get("r9"), RF.Get("r10"), RF.Get("r11"), RF.Get("r12"), RF.Get("r13"), RF.Get("r14"), RF.Get("r15")))
    print("│ r16 = {} │ r17 = {} │ r18 = {} │ r19 = {} │ r20 = {} │ r21 = {} │ r22 ={} │ r23 = {} │" .format(RF.Get("r16"), RF.Get("r17"), RF.Get("r18"), RF.Get("r19"), RF.Get("r20"), RF.Get("r21"), RF.Get("r22"), RF.Get("r23")))
    print("│ r24 = {} │ r25 = {} │ r26 = {} │ r27 = {} │ r28 = {} │ r29 = {} │ r30 ={} │ r31 = {} │" .format(RF.Get("r24"), RF.Get("r25"), RF.Get("r26"), RF.Get("r27"), RF.Get("r28"), RF.Get("r29"), RF.Get("r30"), RF.Get("r31")))
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