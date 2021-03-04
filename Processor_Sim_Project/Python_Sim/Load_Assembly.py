import sys
from Instruction import Instruction

# Load specified assembly program
# Igrnores any lines beginning with '//' in the input program, or blank lines.
def loadProgram(filename, INSTR) :
    instructionCount = 0
    PCcount = 0
    placeHolders = getPlaceHolders(filename)

    # Open file
    programFile = open(filename, 'r')
    if(programFile == None) :
        print("ERROR - File '%s' not found.\n", filename)
        sys.exit(1)

    while True :
        line = programFile.readline()
        # Stop the loop at end of file
        if not line :
            break

        # Remove blank lines
        if (line == '\n') :
            continue

        words = line.split(' ')
        # Remove comments
        if '//' in words[0] :
            continue

        # Remove commas and line endings
        if(len(words) == 1 and words[0][-1] == '\n') :
            words[0] = words[0][:-1]
            if (words[0][-1] == ':') :
                continue
        else :
            for i in range(1, len(words)) :
                words[i] = words[i][:-1]

        newOpcode = words[0]
        newOperands = ['0'] * 3
        for i in range(1, len(words)) :
            newOperands[i-1] = words[i]

        # Replace place holders with correct PC value
        for i in range(0, 3) :
            for j in range(0, len(placeHolders)) :
                if(newOperands[i] == placeHolders[j][0]) :
                    newOperands[i] = str(placeHolders[j][1])

        INSTR[instructionCount] = Instruction(newOpcode, newOperands[0], newOperands[1], newOperands[2], 0)
        instructionCount += 1

    programFile.close()
        
# Converts any placeholders (i.e. Loop:) into their corresponding PC count, to later replace the placeholder calls
def getPlaceHolders(filename) :
    holders = []
    count = 0

    # Open file
    programFile = open(filename, 'r')
    if(programFile == None) :
        print("ERROR - File '%s' not found.\n", filename)
        sys.exit(1)

    while True :
        line = programFile.readline()
        # Stop the loop at end of file
        if not line :
            break

        # Remove blank lines
        if (line == '\n') :
            continue

        words = line.split(' ')
        # Remove comments
        if '//' in words[0] :
            continue

        if(len(words) == 1) :
            words[0] = words[0][:-1]
            if(words[0][-1] == ':') :
                holders.append((words[0][:-1], count))
            else :
                count += 1
        else :
            count += 1

    print(holders)
    return holders
