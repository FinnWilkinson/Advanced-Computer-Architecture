#include <Processor_Sim.h>

int finished = 0;
int cycles = 0;
int instructionCount = 0;
int PC = 0;

int RF[32];         //r0 is zero register, val is always 0
int MEM[1024];
struct instruction INSTR[512];

//initialise data and registers to 0.
void initialize(){
    for (int i = 0; i < 32; i++)
    {
        RF[i] = 0;
        MEM[i] = 0;
        INSTR[i].opCode = 0;
        INSTR[i].operand1 = 0;
        INSTR[i].operand2 = 0;
        INSTR[i].operand3 = 0;
        INSTR[i].instructionNumber = 0;
    }
    for (int i = 32; i < 512; i++)
    {
        MEM[i] = 0;
        INSTR[i].opCode = 0;
        INSTR[i].operand1 = 0;
        INSTR[i].operand2 = 0;
        INSTR[i].operand3 = 0;
        INSTR[i].instructionNumber = 0;
    }
    for (int i = 512; i < 1024; i++)
    {
        MEM[i] = 0;
    }   
}

//if no file provided, print error and info
void printUsageInfo(){
    printf("To execute an assembly program, please include the name of the corresponding file.\n");
    printf("I.e.        ./sim Vector_Addition.txt           \n");
}

//print current system stats (i.e. finsihed, cycles, instructions, PC, RF, CurrentInstruction, PrevInstruction, NextInstruction, etc.)
void printSysInfo(){
    //for testing vector additon script
    for (int i = 0; i < 10; i++)
    {
        printf("a[%d] = %d \n", i, MEM[i]);
    }
    printf("\n");
    for (int i = 0; i < 10; i++)
    {
        printf("b[%d] = %d \n", i, MEM[i+10]);
    }
    printf("\n");
    for (int i = 0; i < 10; i++)
    {
        printf("c[%d] = %d \n", i, MEM[i+20]);
    }
    printf("\n");

    printf("PC = %d\n", PC);
    printf("Cycles = %d\n", cycles);
    printf("Instructins = %d\n", instructionCount);
}

//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
// Main Functionalities

struct instruction fetch(struct instruction nextInstruction){
    nextInstruction = INSTR[PC];
    nextInstruction.instructionNumber = instructionCount;
    instructionCount ++;
    cycles ++;
    PC ++;
    return nextInstruction;
}

int decode(struct instruction currentInstruction, int targetAddress){
    //calculate target address incase of load or store
    switch(currentInstruction.opCode){
        case LD: targetAddress = RF[currentInstruction.operand2] + currentInstruction.operand3;
                break;
        case LDC: targetAddress = currentInstruction.operand2;
                break;
        case STR: targetAddress = RF[currentInstruction.operand2] + currentInstruction.operand3;
                break;
        case STRC: targetAddress = currentInstruction.operand2;
                break;
        defualt: targetAddress = 0;
                break;
    }
    cycles++;
    return targetAddress;
}

int execute(int opcode, int operand1, int operand2, int operand3, int targetAddress){
    int error = 0;
    switch(opcode){
        case HALT: finished = 1;
                   cycles ++;
                break;
        case ADD: RF[operand1] = RF[operand2] + RF[operand3];
                  cycles ++;
                break;
        case ADDI: RF[operand1] = RF[operand2] + operand3;
                   cycles ++;
                break;
        case SUB: RF[operand1] = RF[operand2] - RF[operand3];
                  cycles ++;
                break;
        case SUBI: RF[operand1] = RF[operand2] - operand3;
                  cycles ++;
                break;
        case MUL: RF[operand1] = RF[operand2] * RF[operand3];
                  cycles ++;
                break;
        case MULI: RF[operand1] = RF[operand2] * operand3;
                  cycles ++;
                break;
        case DIV: RF[operand1] = RF[operand2] / RF[operand3];
                  cycles ++;
                break;
        case DIVI: RF[operand1] = RF[operand2] / operand3;
                  cycles ++;
                break;
        case LD: RF[operand1] = MEM[targetAddress];
                break;
        case LDC: RF[operand1] = MEM[targetAddress];
                break;
        case STR: MEM[targetAddress] = RF[operand1];
                break;
        case STRC: MEM[targetAddress] = RF[operand1];
                break;
        case CMP: if(RF[operand2] > RF[operand3]) RF[operand1] = 1;
                  else if(RF[operand2] == RF[operand3]) RF[operand1] = 0;
                  else if(RF[operand2] < RF[operand3]) RF[operand1] = -1;
                break;
        case JMP: PC += operand1;
                break;
        case BR: PC = operand1;
                break;
        case BEQ: if(RF[operand1] == RF[operand2]) PC = operand3;
                break;
        case BLT: if(RF[operand1] < RF[operand2]) PC = operand3;
                break;
        defualt: printf("ERROR - Opcode '%d' not recognised. Exiting...\n", opcode);
                 error = -1;
                break;
    }
    return error;
}

//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//

int main(int argc, char const *argv[])
{
    //make sure program executed correctly
    if(argc == 1){
        printUsageInfo();
        return 0;
    }

    //initialise memory, RF etc to 0
    initialize();
    //load the selected program
    loadProgram(argv[1], INSTR);
    //initialise needed variables
    int error;
    struct instruction nextInstruction;
    int targetAddress = 0;

    //main compute cycle
    while(finished == 0){
        nextInstruction = fetch(nextInstruction);
        targetAddress = decode(nextInstruction, targetAddress);
        error = execute(nextInstruction.opCode, nextInstruction.operand1, nextInstruction.operand2, nextInstruction.operand3, targetAddress);
        if(error != 0) exit(1);
    }
    //print system info
    printSysInfo();
    return 0;
}
