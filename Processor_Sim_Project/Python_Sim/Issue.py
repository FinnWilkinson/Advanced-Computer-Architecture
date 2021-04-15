from Instruction import Instruction
from Reg_To_Reg_Index import *
import copy as copy

class Issue_Unit :
    def __init__(self) :
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT"]
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.nextInstruction = 0
        return

    def issueInstruction(self, RS, IS_EX, ARF) :
        stallThisCycle = False
        # When instruction issued, validation bit in ARF for that register set to NOT valid
        # Only issue instructions that have all operands Valid

        proceed = [True] * 3    # 0 = ARITHMETIC, 1 = LOAD / STORE, 2 = BRANCH / LOGIC
        # See if next item in each RS is available to issue
        for i in range(0,3) :
            if(len(RS[i].Instruction) > 0) :
                # ARITHMETIC
                if(i == 0) :
                    if(IS_EX.Empty[0] == True) :
                        # Check if all fields are available to read from or write to
                        if("r" in str(RS[i].Instruction[0].operand1)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand1)] != 0) :
                                proceed[0] = False
                        if("r" in str(RS[i].Instruction[0].operand2)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand2)] != 0) :
                                proceed[0] = False
                        if("r" in str(RS[i].Instruction[0].operand3)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand3)] != 0) :
                                proceed[0] = False
                    elif(IS_EX.Empty[1] == True) :
                        # Check if all fields are available to read from or write to
                        if("r" in str(RS[i].Instruction[0].operand1)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand1)] != 0) :
                                proceed[0] = False
                        if("r" in str(RS[i].Instruction[0].operand2)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand2)] != 0) :
                                proceed[0] = False
                        if("r" in str(RS[i].Instruction[0].operand3)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand3)] != 0) :
                                proceed[0] = False
                    else :
                        proceed[0] = False
                
                # LOAD/STORE
                elif(i == 1) :
                    if(IS_EX.Empty[2] == True) :
                        # Check if all fields are available to read from or write to
                        if("r" in str(RS[i].Instruction[0].operand1)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand1)] != 0) :
                                proceed[1] = False
                        if("r" in str(RS[i].Instruction[0].operand2)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand2)] != 0) :
                                proceed[1] = False
                        if("r" in str(RS[i].Instruction[0].operand3)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand3)] != 0) :
                                proceed[1] = False
                    else :
                        proceed[1] = False
                
                # BRANCH/LOGIC
                else :
                    if(IS_EX.Empty[3] == True) :
                        # Check if all fields are available to read from or write to
                        if("r" in str(RS[i].Instruction[0].operand1)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand1)] != 0) :
                                proceed[2] = False
                        if("r" in str(RS[i].Instruction[0].operand2)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand2)] != 0) :
                                proceed[2] = False
                        if("r" in str(RS[i].Instruction[0].operand3)) :
                            if(ARF.regInUse[regToRegIndex(RS[i].Instruction[0].operand3)] != 0) :
                                proceed[2] = False
                    else :
                        proceed[2] = False
            else :
                proceed[i] = False



        # Execute in order
        if(proceed[0] == True) :
            if(RS[0].Instruction[0].instructionNumber != self.nextInstruction) :
                proceed[0] = False
        
        if(proceed[1] == True) :
            if(RS[1].Instruction[0].instructionNumber != self.nextInstruction) :
                proceed[1] = False
        
        if(proceed[2] == True) :
            if(RS[2].Instruction[0].instructionNumber != self.nextInstruction) :
                proceed[2] = False

       


        issueCount = 0
        if(proceed[0] == True) :
            # If opcode does operation that writes to ARF then set that register to invalid
            if(RS[0].Instruction[0].opCode not in self.readOnlyINSTR) :
                ARF.regInUse[regToRegIndex(RS[0].Instruction[0].operand1)] = 1
            # Issue to appropriate EU
            if(IS_EX.Empty[0] == True) :
                IS_EX.Instruction[0] = copy.copy(RS[0].Instruction[0])
                IS_EX.TargetAddress[0] = copy.copy(RS[0].TargetAddress[0])
                IS_EX.Empty[0] = False
            else :
                IS_EX.Instruction[1] = copy.copy(RS[0].Instruction[0])
                IS_EX.TargetAddress[1] = copy.copy(RS[0].TargetAddress[0])
                IS_EX.Empty[1] = False
            # Pop from RS queue
            RS[0].Instruction.pop(0)
            RS[0].TargetAddress.pop(0)
            issueCount += 1

        if(proceed[1] == True) :
            # If opcode does operation that writes to ARF then set that register to invalid
            if(RS[1].Instruction[0].opCode not in self.readOnlyINSTR) :
                ARF.regInUse[regToRegIndex(RS[1].Instruction[0].operand1)] = 1
            # Issue to appropriate EU
            IS_EX.Instruction[2] = copy.copy(RS[1].Instruction[0])
            IS_EX.TargetAddress[2] = copy.copy(RS[1].TargetAddress[0])
            IS_EX.Empty[2] = False
            # Pop from RS queue
            RS[1].Instruction.pop(0)
            RS[1].TargetAddress.pop(0)
            issueCount += 1

        if(proceed[2] == True) :
            # If opcode does operation that writes to ARF then set that register to invalid
            if(RS[2].Instruction[0].opCode not in self.readOnlyINSTR) :
                ARF.regInUse[regToRegIndex(RS[2].Instruction[0].operand1)] = 1
            # Issue to appropriate EU
            IS_EX.Instruction[3] = copy.copy(RS[2].Instruction[0])
            IS_EX.TargetAddress[3] = copy.copy(RS[2].TargetAddress[0])
            IS_EX.Empty[3] = False
            # Pop from RS queue
            RS[2].Instruction.pop(0)
            RS[2].TargetAddress.pop(0)
            issueCount += 1
        
        if(issueCount == 0) :
            stallThisCycle = True
        else :
            self.nextInstruction += issueCount

        return stallThisCycle                    


    def issueNext(self, RS, IS_EX, ARF) :
        stallThisCycle = False
        instructionsIssued = 0
        # When instruction issued, validation bit in ARF for that register set to NOT valid
        # Only issue instructions that have all operands Valid

        # In each RS, issue oldest (lowest INSTR number) instruction that has all values + no dependancies
        # List will be sorted by default from oldest to youngest

        # Arithmetic RS
        if(len(RS[0].Instruction) > 0) :
            # Check that an EU is free, if it is move to next check
            if(IS_EX.Empty[0] == True or IS_EX.Empty[1] == True) :
                # Look through list from oldest -> youngest
                for i in range(0, len(RS[0].Instruction)) :

                    # See if operand 1 is available, and if it is dependant
                    if("r" in str(RS[0].D1[i])) :
                        if(ARF.regInUse[regToRegIndex(RS[0].D1[i])] != 0) :
                            continue    # If in use, go to next instruction
                        isDependant1 = self.dependant(RS, RS[0].Instruction[i].operand1, RS[0].Instruction[i].instructionNumber)
                        if(isDependant1 == True) :
                            continue    # If dependant, go to next instruction
                   
                    # If operands not valid already, get it if it is ready
                    # Check it has no dependancies to any instruction older than it in ALL RS's, if it doesn't, move to next check
                    # Operand 2
                    if(RS[0].V1[i] != 0 ) : # if V1 == 0, then correct value already in S1
                        # Check if register currently in use
                        if(ARF.regInUse[regToRegIndex(RS[0].Instruction[i].operand2)] != 0) :
                            continue    # If in use, go to next instruction
                        isDependant2 = self.dependant(RS, RS[0].Instruction[i].operand2, RS[0].Instruction[i].instructionNumber)
                        if (isDependant2 == True) :
                            continue    # If dependant, go to next instruction
                        else :
                            # Get and store value
                            RS[0].S1[i] = copy.copy(ARF.Register[regToRegIndex(RS[0].Instruction[i].operand2)])
                            RS[0].V1[i] = 0
                    # Operand 3
                    if(RS[0].V2[i] != 0 ) : # if V2 == 0, then correct value already in S2
                        # Check if register currently in use
                        if(ARF.regInUse[regToRegIndex(RS[0].Instruction[i].operand3)] != 0) :
                            continue    # If in use, go to next instruction
                        isDependant3 = self.dependant(RS, RS[0].Instruction[i].operand3, RS[0].Instruction[i].instructionNumber)
                        if (isDependant3 == True) :
                            continue    # If dependant, go to next instruction
                        else :
                            # Get and store value
                            RS[0].S2[i] = copy.copy(ARF.Register[regToRegIndex(RS[0].Instruction[i].operand2)])
                            RS[0].V2[i] = 0

                    # If branch waiting that is older than it, Don't issue. 
                    # Only need to check first item in branch RS, as it will be the oldest
                    if(len(RS[2].Instruction) > 0 and RS[2].Instruction[0].instructionNumber < RS[0].Instruction[i].instructionNumber) :
                        continue        # If in use, go to next instruction

                    # else, Issue instruction
                    # If opcode does operation that writes to ARF then set that register to invalid
                    if(RS[0].Instruction[i].opCode not in self.readOnlyINSTR) :
                        ARF.regInUse[regToRegIndex(RS[0].D1[i])] = 1
                    # Issue to appropriate EU
                    if(IS_EX.Empty[0] == True) :
                        IS_EX.Instruction[0] = copy.copy(RS[0].Instruction[i])
                        IS_EX.TargetAddress[0] = copy.copy(RS[0].TargetAddress[i])
                        IS_EX.Op[0] = copy.copy(RS[0].Op[i])
                        IS_EX.D1[0] = copy.copy(RS[0].D1[i])
                        IS_EX.S1[0] = int(copy.copy(RS[0].S1[i]))
                        IS_EX.S2[0] = int(copy.copy(RS[0].S2[i]))  
                        IS_EX.Empty[0] = False
                    else :
                        IS_EX.Instruction[1] = copy.copy(RS[0].Instruction[i])
                        IS_EX.TargetAddress[1] = copy.copy(RS[0].TargetAddress[i])
                        IS_EX.Op[1] = copy.copy(RS[0].Op[i])
                        IS_EX.D1[1] = copy.copy(RS[0].D1[i])
                        IS_EX.S1[1] = int(copy.copy(RS[0].S1[i]))
                        IS_EX.S2[1] = int(copy.copy(RS[0].S2[i]))  
                        IS_EX.Empty[1] = False
                    # Show that register in use
                    if("r" in str(RS[0].D1[i])) :
                        ARF.regInUse[regToRegIndex(RS[0].D1[i])] = 1
                    # Pop from RS queue
                    print("Issued {}" .format(RS[0].Instruction[i].instructionNumber))   
                    RS[0].Instruction.pop(i)
                    RS[0].TargetAddress.pop(i)
                    RS[0].Op.pop(i)
                    RS[0].D1.pop(i)
                    RS[0].V1.pop(i)
                    RS[0].V2.pop(i)
                    RS[0].S1.pop(i)
                    RS[0].S2.pop(i)
                    instructionsIssued += 1
                    break
                    
            else :
                stallThisCycle = True



        # Load / Store RS
        if(len(RS[1].Instruction) > 0) :
            # Check that an EU is free, if it is move to next check
            if(IS_EX.Empty[2] == True) :
                # Look through list from oldest -> youngest
                for i in range(0, len(RS[1].Instruction)) :

                    # See if operand 1 is available, get value if instruction is read only
                    if(RS[1].Op[i] in self.readOnlyINSTR) :
                        # If operand 1 is not a constant
                        if(RS[1].D1[i] == None) : 
                            # Make sure not dependant on anything
                            isDependant1 = self.dependant(RS, RS[1].Instruction[i].operand1, RS[1].Instruction[i].instructionNumber)
                            if (isDependant1 == False and ARF.regInUse[regToRegIndex(RS[1].Instruction[i].operand1)] == 0) :
                                RS[1].D1[i] = copy.copy(ARF.Register[regToRegIndex(RS[1].Instruction[i].operand1)])
                            else :
                                #print("continue 1 in LD/STR")
                                continue # If in use or has dependancy, go to next instruction
                    else :
                        if("r" in str(RS[1].D1[i])) :
                            if(ARF.regInUse[regToRegIndex(RS[1].D1[i])] != 0) :
                                #print("continue 2 in LD/STR")
                                continue    # If in use, go to next instruction
                            isDependant1 = self.dependant(RS, RS[1].Instruction[i].operand1, RS[1].Instruction[i].instructionNumber)
                            if(isDependant1 == True) :
                                #print("continue 3 in LD/STR")
                                continue    # If dependant, go to next instruction
                   
                    # If operands not valid already, get it if it is ready
                    # Check it has no dependancies to any instruction older than it in ALL RS's, if it doesn't, move to next check
                    # Operand 2
                    if(RS[1].V1[i] != 0 ) : # if V1 == 0, then correct value already in S1
                        # Check if register currently in use
                        if(ARF.regInUse[regToRegIndex(RS[1].Instruction[i].operand2)] != 0) :
                            #print("continue 4 in LD/STR")
                            continue    # If in use, go to next instruction
                        isDependant2 = self.dependant(RS, RS[1].Instruction[i].operand2, RS[1].Instruction[i].instructionNumber)
                        if (isDependant2 == True) :
                            #print("continue 5 in LD/STR")
                            continue    # If in use, go to next instruction
                        else :
                            # Get and store value
                            RS[1].S1[i] = copy.copy(ARF.Register[regToRegIndex(RS[1].Instruction[i].operand2)])
                            RS[1].V1[i] = 0
                    # Operand 3
                    if(RS[1].V2[i] != 0 ) : # if V2 == 0, then correct value already in S2
                        # Check if register currently in use
                        if(ARF.regInUse[regToRegIndex(RS[1].Instruction[i].operand3)] != 0) :
                            #print("continue 6 in LD/STR")
                            continue    # If in use, go to next instruction
                        isDependant3 = self.dependant(RS, RS[1].Instruction[i].operand3, RS[1].Instruction[i].instructionNumber)
                        if (isDependant3 == True) :
                            #print("continue 7 in LD/STR")
                            continue    # If in use, go to next instruction
                        else :
                            # Get and store value
                            RS[1].S2[i] = copy.copy(ARF.Register[regToRegIndex(RS[1].Instruction[i].operand2)])
                            RS[1].V2[i] = 0

                    # If branch waiting that is older than it, Don't issue. 
                    # Only need to check first item in branch RS, as it will be the oldest
                    if(len(RS[2].Instruction) > 0 and RS[2].Instruction[0].instructionNumber < RS[1].Instruction[i].instructionNumber) :
                        #print("continue 8 in LD/STR")
                        continue        # If in use, go to next instruction

                    # else, Issue instruction
                    # If opcode does operation that writes to ARF then set that register to invalid
                    if(RS[1].Instruction[i].opCode not in self.readOnlyINSTR) :
                        ARF.regInUse[regToRegIndex(RS[1].D1[i])] = 1
                    # Issue to appropriate EU
                    IS_EX.Instruction[2] = copy.copy(RS[1].Instruction[i])
                    IS_EX.TargetAddress[2] = copy.copy(RS[1].TargetAddress[i])
                    IS_EX.Op[2] = copy.copy(RS[1].Op[i])
                    IS_EX.D1[2] = copy.copy(RS[1].D1[i])
                    IS_EX.S1[2] = int(copy.copy(RS[1].S1[i]))
                    IS_EX.S2[2] = int(copy.copy(RS[1].S2[i]))  
                    IS_EX.Empty[2] = False
                    
                     # Show that register in use
                    if("r" in str(RS[1].D1[i])) :
                        ARF.regInUse[regToRegIndex(RS[1].D1[i])] = 1
                    # Pop from RS queue
                    print("Issued {}" .format(RS[1].Instruction[i].instructionNumber))   
                    RS[1].Instruction.pop(i)
                    RS[1].TargetAddress.pop(i)
                    RS[1].Op.pop(i)
                    RS[1].D1.pop(i)
                    RS[1].V1.pop(i)
                    RS[1].V2.pop(i)
                    RS[1].S1.pop(i)
                    RS[1].S2.pop(i)
                    instructionsIssued += 1
                    break
                    
            else :
                stallThisCycle = True



        # Branch / Logic
        if(len(RS[2].Instruction) > 0) :
            # Check that an EU is free, if it is move to next check
            if(IS_EX.Empty[3] == True) :
                # Look through list from oldest -> youngest
                for i in range(0, len(RS[2].Instruction)) :

                    # See if operand 1 is available, get value if instruction is read only
                    if(RS[2].Op[i] in self.readOnlyINSTR) :
                        # If operand 1 is not a constant
                        if(RS[2].D1[i] == None) : 
                            # Make sure not dependant on anything
                            isDependant1 = self.dependant(RS, RS[2].Instruction[i].operand1, RS[2].Instruction[i].instructionNumber)
                            if (isDependant1 == False and ARF.regInUse[regToRegIndex(RS[2].Instruction[i].operand1)] == 0) :
                                RS[2].D1[i] = copy.copy(ARF.Register[regToRegIndex(RS[2].Instruction[i].operand1)])
                            else :
                                continue # If in use or has dependancy, go to next instruction
                    else :
                        if("r" in str(RS[2].D1[i])) :
                            if(ARF.regInUse[regToRegIndex(RS[2].D1[i])] != 0) :
                                continue    # If in use, go to next instruction
                            isDependant1 = self.dependant(RS, RS[2].D1[i], RS[2].Instruction[i].instructionNumber)
                            if(isDependant1 == True) :
                                continue    # If dependant, go to next instruction
                
                    # If operands not valid already, get it if it is ready
                    # Check it has no dependancies to any instruction older than it in ALL RS's, if it doesn't, move to next check
                    # Operand 2
                    if(RS[2].V1[i] != 0 ) : # if V1 == 0, then correct value already in S1
                        # Check if register currently in use
                        if(ARF.regInUse[regToRegIndex(RS[2].Instruction[i].operand2)] != 0) :
                            continue    # If in use, go to next instruction
                        isDependant2 = self.dependant(RS, RS[2].Instruction[i].operand2, RS[2].Instruction[i].instructionNumber)
                        if (isDependant2 == True) :
                            continue    # If dependant, go to next instruction
                        else :
                            # Get and store value
                            RS[2].S1[i] = copy.copy(ARF.Register[regToRegIndex(RS[2].Instruction[i].operand2)])
                            RS[2].V1[i] = 0
                    # Operand 3
                    if(RS[2].V2[i] != 0 ) : # if V2 == 0, then correct value already in S2
                        # Check if register currently in use
                        if(ARF.regInUse[regToRegIndex(RS[2].Instruction[i].operand3)] != 0) :
                            continue    # If in use, go to next instruction
                        isDependant3 = self.dependant(RS, RS[2].Instruction[i].operand3, RS[2].Instruction[i].instructionNumber)
                        if (isDependant3 == True) :
                            continue    # If dependant, go to next instruction
                        else :
                            # Get and store value
                            RS[2].S2[i] = copy.copy(ARF.Register[regToRegIndex(RS[2].Instruction[i].operand2)])
                            RS[2].V2[i] = 0

                    # If branch waiting that is older than it, Don't issue. 
                    # Only need to check first item in branch RS, as it will be the oldest
                    if(len(RS[2].Instruction) > 0 and RS[2].Instruction[0].instructionNumber < RS[2].Instruction[i].instructionNumber) :
                        continue        # If in use, go to next instruction

                    # else, Issue instruction
                    # If opcode does operation that writes to ARF then set that register to invalid
                    if(RS[2].Instruction[i].opCode not in self.readOnlyINSTR) :
                        ARF.regInUse[regToRegIndex(RS[2].D1[i])] = 1
                    # Issue to appropriate EU
                    IS_EX.Instruction[3] = copy.copy(RS[2].Instruction[i])
                    IS_EX.TargetAddress[3] = copy.copy(RS[2].TargetAddress[i])
                    IS_EX.Op[3] = copy.copy(RS[2].Op[i])
                    IS_EX.D1[3] = copy.copy(RS[2].D1[i])
                    IS_EX.S1[3] = int(copy.copy(RS[2].S1[i]))
                    IS_EX.S2[3] = int(copy.copy(RS[2].S2[i]))  
                    IS_EX.Empty[3] = False
                    
                     # Show that register in use
                    if("r" in str(RS[2].D1[i])) :
                        ARF.regInUse[regToRegIndex(RS[2].D1[i])] = 1
                    # Pop from RS queue
                    print("Issued {}" .format(RS[2].Instruction[i].instructionNumber))   
                    RS[2].Instruction.pop(i)
                    RS[2].TargetAddress.pop(i)
                    RS[2].Op.pop(i)
                    RS[2].D1.pop(i)
                    RS[2].V1.pop(i)
                    RS[2].V2.pop(i)
                    RS[2].S1.pop(i)
                    RS[2].S2.pop(i)
                    instructionsIssued += 1
                    break
                    
            else :
                stallThisCycle = True

        if(instructionsIssued != 3) :
            stallThisCycle = True

        return stallThisCycle


    # Checks if register is dependant on any instruction before it in RS
    def dependant(self, RS, register, instrNumber) :
        isDependant = False
        for j in range(0,3) :
            for i in range(0, len(RS[j].Instruction)) :
                if(RS[j].Instruction[i].instructionNumber < instrNumber) :
                    if(RS[j].Instruction[i].operand1 == register) :
                        isDependant = True
                        return isDependant
                else :
                    break

        # CURRENTLY HAVE FALSE DEPENDANCY CRASHING PROGRAM.
        # OoO EXECUTION SENDING OUT INSTRUCTION 46 IN VECTOR ADDITION (ADDI r1, r1, 1) WHEN NEXT INSTRUCTION IS 41 (LDC r3, r1, 11)
        # REGISTER RE-NAMING WILL SOLVE THIS ISSUE

        return isDependant