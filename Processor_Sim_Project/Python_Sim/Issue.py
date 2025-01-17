from Instruction import Instruction
import copy as copy

class Issue_Unit :
    def __init__(self) :
        self.readOnlyINSTR = ["STR", "STRC", "JMP", "BR", "BEQ", "BLT", "HALT", "PAUSE"]
        self.branchInstructions = ["JMP", "BR", "BEQ", "BLT"]
        self.nextInstruction = 0
        return


    def issue(self, RS, IS_EX, ARF, ROB, branchPredType, LSQ, pipelines, pipelineCount, ROBsize) :
        stallThisCycle = False
        ArithStall = False

        # Only issue instructions that have all operands Valid
        # In each RS, issue oldest (lowest INSTR number) instruction that has all values + no True dependancies with instructions ahead of it in queue
        # List will be sorted by default from oldest to youngest

        # Arithmetic 0 RS
        if(len(RS[0].Instruction) > 0) :
            # Check EU ready to recieve next instruction
            if(IS_EX[0].Empty == True) :
                for i in range(0, len(RS[0].Instruction)) :
                    # Try get all values, if cant then go to next instruction in queue

                    # Get value of operand2 if needed
                    if(RS[0].V1[i] != 0) :
                        tempROBaddr = int(RS[0].V1[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[0].S1[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # Get value of operand3 if needed
                    if(RS[0].V2[i] != 0) :
                        tempROBaddr = int(RS[0].V2[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[0].S2[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue
                    if(branchPredType == 0) :
                        # If no branch that preceeds it, Issue          Only with no branch prediction
                        preceedingBranch = False
                        for j in range(0, len(RS[2].Instruction)) :
                            if(RS[2].Instruction[j].instructionNumber < RS[0].Instruction[i].instructionNumber) :
                                if(RS[2].Op[j] in self.branchInstructions) :
                                    preceedingBranch = True
                                    break
                            else :
                                break
                        if(preceedingBranch == True) :
                            stallThisCycle = True       # preceeding branch so stalled
                            ArithStall = True           # Set so dont duplicate stall count with other EU
                            break

                    # Issue to EU
                    IS_EX[0].InstructionNumber = copy.copy(RS[0].Instruction[i].instructionNumber)
                    IS_EX[0].Op = copy.copy(RS[0].Op[i])
                    IS_EX[0].D1 = copy.copy(RS[0].D1[i])
                    IS_EX[0].S1 = copy.copy(RS[0].S1[i])
                    IS_EX[0].S2 = copy.copy(RS[0].S2[i])
                    IS_EX[0].Empty = False
                    
                    # Remove from RS
                    RS[0].Instruction.pop(i)
                    RS[0].Op.pop(i)
                    RS[0].D1.pop(i)
                    RS[0].V1.pop(i)
                    RS[0].V2.pop(i)
                    RS[0].S1.pop(i)
                    RS[0].S2.pop(i)

                    break         

################################################################################################################

        # Arithmetic 1 RS
        if(len(RS[0].Instruction) > 0 and ArithStall == False) :
            # Check EU ready to recieve next instruction
            if(IS_EX[1].Empty == True) :
                for i in range(0, len(RS[0].Instruction)) :
                    # Try get all values, if cant then go to next instruction in queue

                    # Get value of operand2 if needed
                    if(RS[0].V1[i] != 0) :
                        tempROBaddr = int(RS[0].V1[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[0].S1[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # Get value of operand3 if needed
                    if(RS[0].V2[i] != 0) :
                        tempROBaddr = int(RS[0].V2[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[0].S2[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    if(branchPredType == 0) :
                        # If no branch that preceeds it, Issue          Only with no branch prediction
                        preceedingBranch = False
                        for j in range(0, len(RS[2].Instruction)) :
                            if(RS[2].Instruction[j].instructionNumber < RS[0].Instruction[i].instructionNumber) :
                                if(RS[2].Op[j] in self.branchInstructions) :
                                    preceedingBranch = True
                                    break
                            else :
                                break
                        if(preceedingBranch == True) :
                            stallThisCycle = True       # preceeding branch so stalled
                            break

                    # Issue to EU
                    IS_EX[1].InstructionNumber = copy.copy(RS[0].Instruction[i].instructionNumber)
                    IS_EX[1].Op = copy.copy(RS[0].Op[i])
                    IS_EX[1].D1 = copy.copy(RS[0].D1[i])
                    IS_EX[1].S1 = copy.copy(RS[0].S1[i])
                    IS_EX[1].S2 = copy.copy(RS[0].S2[i])
                    IS_EX[1].Empty = False
                    
                    # Remove from RS
                    RS[0].Instruction.pop(i)
                    RS[0].Op.pop(i)
                    RS[0].D1.pop(i)
                    RS[0].V1.pop(i)
                    RS[0].V2.pop(i)
                    RS[0].S1.pop(i)
                    RS[0].S2.pop(i)

                    break
            else :
                # If both EUs not free, register stall
                stallThisCycle = True              


############################################################################################

        # Load / Store RS
        if(len(RS[1].Instruction) > 0) :
            # Check EU ready to recieve next instruction
            if(IS_EX[2].Empty == True) :
                for i in range(0, len(RS[1].Instruction)) :
                    # Try get all values, if cant then go to next instruction in queue

                    # Check if read-only instruction, and get value of operand1 if needed
                    if(RS[1].Op[i] in self.readOnlyINSTR) :
                        if("ROB" in str(RS[1].D1[i])) :
                            tempROBaddr = int(RS[1].D1[i][3:])
                            if(ROB.Complete[tempROBaddr] == 1) :
                                # Value ready to be read
                                RS[1].D1[i] = copy.copy(ROB.Value[tempROBaddr])
                            else :
                                # Value not ready, continue to next in list
                                continue

                    # Get value of operand2 if needed
                    if(RS[1].V1[i] != 0) :
                        tempROBaddr = int(RS[1].V1[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[1].S1[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # Get value of operand3 if needed
                    if(RS[1].V2[i] != 0) :
                        tempROBaddr = int(RS[1].V2[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[1].S2[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # Ensure all previous un-committed store instructions have address calculated
                    allAddrPresent = True
                    currentPtr = copy.copy(LSQ.CommitPtr)
                    while True :
                        if(currentPtr == LSQ.IssuePtr) :
                            break
                        if(LSQ.Address[currentPtr] == -1 and LSQ.InstructionType[currentPtr] == "STORE" and LSQ.InstructionNumber[currentPtr] < RS[1].Instruction[i].instructionNumber) :
                            allAddrPresent = False
                            break
                        currentPtr = copy.copy((currentPtr + 1) % 128)

                    if(allAddrPresent == False) :
                        continue

                    # As know all operands, can update address in LSQ
                    memAddress = copy.copy(RS[1].S1[i] + RS[1].S2[i])
                    LSQindex = copy.copy(LSQ.InstructionNumber.index(RS[1].Instruction[i].instructionNumber))
                    LSQ.Address[LSQindex] = copy.copy(memAddress)
                    
                    # If no branch prediction and 1 pipeline
                    if(branchPredType == 0) :
                        # If no branch that preceeds it, Issue          Only with no branch prediction
                        preceedingBranch = False
                        for j in range(0, len(RS[2].Instruction)) :
                            if(RS[2].Instruction[j].instructionNumber < RS[1].Instruction[i].instructionNumber) :
                                if(RS[2].Op[j] in self.branchInstructions) :
                                    preceedingBranch = True
                                    break
                            else :
                                break
                        if(preceedingBranch == True) :
                            stallThisCycle = True       # preceeding branch so stalled
                            break

                    # If previous store has same address and isnt complete, dont issue
                    canIssue = True
                    currentPtr = copy.copy(LSQ.IssuePtr)
                    while True :
                        if(currentPtr == ((LSQ.CommitPtr - 1 + 128) % 128)) :
                            break
                        if(LSQ.Address[currentPtr] == LSQ.Address[LSQindex] and LSQ.InstructionType[currentPtr] == "STORE" and LSQ.InstructionNumber[currentPtr] < RS[1].Instruction[i].instructionNumber and LSQ.Complete[currentPtr] == 0) :
                            canIssue = False
                            break
                        currentPtr = copy.copy((currentPtr - 1 + 128) % 128)

                    if(canIssue == False) :
                        continue

                    # Issue to EU
                    IS_EX[2].InstructionNumber = copy.copy(RS[1].Instruction[i].instructionNumber)
                    IS_EX[2].Op = copy.copy(RS[1].Op[i])
                    IS_EX[2].D1 = copy.copy(RS[1].D1[i])
                    IS_EX[2].S1 = copy.copy(RS[1].S1[i])
                    IS_EX[2].S2 = copy.copy(RS[1].S2[i])
                    IS_EX[2].Empty = False
                    
                    # Remove from RS
                    RS[1].Instruction.pop(i)
                    RS[1].Op.pop(i)
                    RS[1].D1.pop(i)
                    RS[1].V1.pop(i)
                    RS[1].V2.pop(i)
                    RS[1].S1.pop(i)
                    RS[1].S2.pop(i)

                    break
            else :
                # If no EU free, stall
                stallThisCycle = True                   


##########################################################################################

        # Branch / Logic
        if(len(RS[2].Instruction) > 0) :
            # Check EU ready to recieve next instruction
            if(IS_EX[3].Empty == True) :
                for i in range(0, len(RS[2].Instruction)) :
                    # Check for HALT
                    if(RS[2].Op[i] == "HALT") :
                        canHalt = True
                        # For each pipeline
                        for m in range(0, pipelineCount) :
                            # Check Reservation Stations empty
                            if(len(pipelines[m].RS[0].Op) != 0 or len(pipelines[m].RS[1].Op) != 0) :
                                canHalt = False
                            # Check IS_EX empty
                            if(pipelines[m].IS_EX[0].Empty == False or pipelines[m].IS_EX[1].Empty == False or pipelines[m].IS_EX[2].Empty == False or pipelines[m].IS_EX[3].Empty == False) :
                                canHalt = False
                        # Make sure ROB is finished committing
                        robComplete = True
                        for q in range(0, ROBsize) :
                            if("r" in ROB.Register[q]) :
                                robComplete = False
                                break
                        if(robComplete == False) :
                            canHalt = False
                        if(canHalt == False) :
                            continue

                    # Try get all values, if cant then go to next instruction in queue

                    # Check if read-only instruction, and get value of operand1 if needed
                    if(RS[2].Op[i] in self.readOnlyINSTR) :
                        if("ROB" in str(RS[2].D1[i])) :
                            tempROBaddr = int(RS[2].D1[i][3:])
                            if(ROB.Complete[tempROBaddr] == 1) :
                                # Value ready to be read
                                RS[2].D1[i] = copy.copy(ROB.Value[tempROBaddr])
                            else :
                                # Value not ready, continue to next in list
                                continue

                    # Get value of operand2 if needed
                    if(RS[2].V1[i] != 0) :
                        tempROBaddr = int(RS[2].V1[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[2].S1[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    # Get value of operand3 if needed
                    if(RS[2].V2[i] != 0) :
                        tempROBaddr = int(RS[2].V2[i][3:])
                        if(ROB.Complete[tempROBaddr] == 1) :
                            # Value ready to be read
                            RS[2].S2[i] = copy.copy(ROB.Value[tempROBaddr])
                        else :
                            # Value not ready, continue to next in list
                            continue

                    if(branchPredType == 0) :
                        # If no branch that preceeds it, Issue          Only with no branch prediction
                        preceedingBranch = False
                        for j in range(0, len(RS[2].Instruction)) :
                            if(RS[2].Instruction[j].instructionNumber < RS[2].Instruction[i].instructionNumber) :
                                if(RS[2].Op[j] in self.branchInstructions) :
                                    preceedingBranch = True
                                    break
                            else :
                                break
                        if(preceedingBranch == True) :
                            stallThisCycle = True       # preceeding branch so stalled
                            break             

                    # Issue to EU
                    IS_EX[3].InstructionNumber = copy.copy(RS[2].Instruction[i].instructionNumber)
                    IS_EX[3].BranchPC = copy.copy(RS[2].BranchPC[i])
                    IS_EX[3].Op = copy.copy(RS[2].Op[i])
                    IS_EX[3].D1 = copy.copy(RS[2].D1[i])
                    IS_EX[3].S1 = copy.copy(RS[2].S1[i])
                    IS_EX[3].S2 = copy.copy(RS[2].S2[i])
                    IS_EX[3].Empty = False
                    
                    # Remove from RS
                    RS[2].Instruction.pop(i)
                    RS[2].BranchPC.pop(i)
                    RS[2].Op.pop(i)
                    RS[2].D1.pop(i)
                    RS[2].V1.pop(i)
                    RS[2].V2.pop(i)
                    RS[2].S1.pop(i)
                    RS[2].S2.pop(i)

                    break
            else :
                # If no EU free, stall
                stallThisCycle = True                   

        
##########################################################################################


        return stallThisCycle
