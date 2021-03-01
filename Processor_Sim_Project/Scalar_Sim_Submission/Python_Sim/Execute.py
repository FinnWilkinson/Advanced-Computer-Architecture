from Instruction import Instruction

def executeInstruction(opcode, operand1, operand2, operand3, targetAddress, RF, MEM, PC, cycles, instructionExecuteCount, finished) :
    error = 0
    # HALT
    if opcode == 0:                                                     
        finished = True
    # ADD
    elif opcode == 1: 
        RF[operand1] = RF[operand2] + RF[operand3]
    # ADDI
    elif opcode == 2: 
        RF[operand1] = RF[operand2] + operand3
    # SUB
    elif opcode == 3: 
        RF[operand1] = RF[operand2] - RF[operand3]
    # SUBI
    elif opcode == 4: 
        RF[operand1] = RF[operand2] - operand3
    # MUL
    elif opcode == 5: 
        RF[operand1] = RF[operand2] * RF[operand3]
    # MULI
    elif opcode == 6: 
        RF[operand1] = RF[operand2] * operand3
    # DIV
    elif opcode == 7: 
        RF[operand1] = int(RF[operand2] / RF[operand3])
    # DIVI
    elif opcode == 8: 
        RF[operand1] = int(RF[operand2] / operand3)
    # LD
    elif opcode == 9: 
        RF[operand1] = MEM[targetAddress]
    # LDC
    elif opcode == 10: 
        RF[operand1] = MEM[targetAddress]
    # STR
    elif opcode == 11: 
        MEM[targetAddress] = RF[operand1]
    # STRC
    elif opcode == 12:
        MEM[targetAddress] = RF[operand1]
    # CMP
    elif opcode == 13: 
        if(RF[operand2] > RF[operand3]) :
            RF[operand1] = 1
        elif(RF[operand2] == RF[operand3]) :
            RF[operand1] = 0
        elif(RF[operand2] < RF[operand3]) :
            RF[operand1] = -1
    # JMP
    elif opcode == 14: 
        PC = RF[operand1]
    # BR
    elif opcode == 15: 
        PC = operand1
    # BEQ
    elif opcode == 16: 
        if(RF[operand1] == RF[operand2]) :
            PC = operand3
    # BLT
    elif opcode == 17: 
        if(RF[operand1] < RF[operand2]) :
            PC = operand3
    # Opcode not recognised
    else: 
        print("ERROR - Opcode '{}' not recognised. Exiting..." .format(opcode))
        error = -1

    cycles += 1
    instructionExecuteCount += 1
    return error, PC, cycles, instructionExecuteCount, finished