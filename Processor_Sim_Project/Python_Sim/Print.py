# Print current system stats (finsihed, cycles, instructions, PC, RF, CurrentInstruction, PrevInstruction, NextInstruction, etc.)
def printSysInfo(RF, MEM, INSTR, PC, cycles, instructionCount) :
    # For testing vector additon script
    # for i in range(0, 10) :
    #     print("a[{}] = {}" .format(i, MEM[i]))
    # print("")
    # for i in range(0, 10) :
    #     print("b[{}] = {}" .format(i, MEM[i+10]))
    # print("")
    # for i in range(0, 10) :
    #     print("c[{}] = {}" .format(i, MEM[i+20]))
    # print("")

    # For testing QuickSort Script
    print("RF : {}" .format(RF))
    print("MEM[0-100] : {}" .format(MEM[:100]))

    print("PC = {}" .format(PC))
    print("Cycles = {}" .format(cycles))
    print("Instructions = {}" .format(instructionCount))

# If no file provided, print error and info
def printUsageInfo() :
    print("To execute an assembly program, please include the name of the corresponding file.")
    print("I.e.        python Simulator_main.py Vector_Addition.txt           ")