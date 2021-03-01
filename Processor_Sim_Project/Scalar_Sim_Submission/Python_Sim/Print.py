import os
import sys
import numpy as np

def printSysInfo(RF, MEM, INSTR, PC, cycles, instructionFetchCount, instructionExecuteCount) :
    np.set_printoptions(threshold=sys.maxsize)
    tempMEM = np.array(MEM)
    os.system('cls||clear')

    print("│ PC = {} │ Cycles = {} │ Instructions Fetched = {} │ Instructions Executed = {} |" .format(PC, cycles, instructionFetchCount, instructionExecuteCount))
    print()
    print("Register File :")
    print("────────────────")
    print("│ r0 = {} │ r1 = {} │ r2 = {} │ r3 = {} │ r4 = {} │ r5 = {} │ r6 ={} │ r7 = {} │" .format(RF[0], RF[1], RF[2], RF[3], RF[4], RF[5], RF[6], RF[7]))
    print("│ r8 = {} │ r9 = {} │ r10 = {} │ r11 = {} │ r12 = {} │ r13 = {} │ r14 ={} │ r15 = {} │" .format(RF[8], RF[9], RF[10], RF[11], RF[12], RF[13], RF[14], RF[15]))
    print("│ r16 = {} │ r17 = {} │ r18 = {} │ r19 = {} │ r20 = {} │ r21 = {} │ r22 ={} │ r23 = {} │" .format(RF[16], RF[17], RF[18], RF[19], RF[20], RF[21], RF[22], RF[23]))
    print("│ r24 = {} │ r25 = {} │ r26 = {} │ r27 = {} │ r28 = {} │ r29 = {} │ r30 ={} │ r31 = {} │" .format(RF[24], RF[25], RF[26], RF[27], RF[28], RF[29], RF[30], RF[31]))
    print()
    print("Main Memory :")
    print("────────────────")
    print(tempMEM)
    



    print()
    input("Press Enter key to continue ...")


# If no file provided, print error and info
def printUsageInfo() :
    os.system('cls||clear')
    print("To execute an assembly program, please include the name of the corresponding file.")
    print("I.e.        python Simulator_main.py Vector_Addition.txt           ")
    print()
    input("Press Enter key to continue ...")