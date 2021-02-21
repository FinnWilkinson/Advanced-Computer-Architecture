#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define LINE_LEN 256

int finished = 0;
int cycles = 0;
int instructionCount = 0;
int PC = 0;

//structure holding an instruction and its opcodes for easier storage, passing, etc.
struct instruction
{
    int opCode;
    int operand1;
    int operand2;
    int operand3;
};

int RF[32];         //r0 is zero register, val is always 0
int MEM[1024];
struct instruction INSTR[512];

enum instructions {HALT, ADD, ADDI, SUB, SUBI, MUL, MULI, DIV, DIVI, LD, LDC, STR, STRC, CMP, JMP, BR, BEQ, BLT};
enum registers {r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, 
              r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31};

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
    }
    for (int i = 32; i < 512; i++)
    {
        MEM[i] = 0;
        INSTR[i].opCode = 0;
        INSTR[i].operand1 = 0;
        INSTR[i].operand2 = 0;
        INSTR[i].operand3 = 0;
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

//convert between instruction string read from file and enum version
int opcodeSTRtoENUM(char *opcode){
    if(strcmp(opcode, "HALT") == 0) return HALT;
    else if(strcmp(opcode, "ADD") == 0) return ADD;
    else if(strcmp(opcode, "ADDI") == 0) return ADDI;
    else if(strcmp(opcode, "SUB") == 0) return SUB;
    else if(strcmp(opcode, "SUBI") == 0) return SUBI;
    else if(strcmp(opcode, "MUL") == 0) return MUL;
    else if(strcmp(opcode, "MULI") == 0) return MULI;
    else if(strcmp(opcode, "DIV") == 0) return DIV;
    else if(strcmp(opcode, "DIVI") == 0) return DIVI;
    else if(strcmp(opcode, "LD") == 0) return LD;
    else if(strcmp(opcode, "LDC") == 0) return LDC;
    else if(strcmp(opcode, "STR") == 0) return STR;
    else if(strcmp(opcode, "STRC") == 0) return STRC;
    else if(strcmp(opcode, "CMP") == 0) return CMP;
    else if(strcmp(opcode, "JMP") == 0) return JMP;
    else if(strcmp(opcode, "BR") == 0) return BR;
    else if(strcmp(opcode, "BEQ") == 0) return BEQ;
    else if(strcmp(opcode, "BLT") == 0) return BLT;
    else return -1;
}

//converts operand into associated register enum index, or the directly to an int if an immediate operand
int operandSTRtoENUM(char *operand){
    if(strcmp(operand, "r0") == 0) return r0;
    else if(strcmp(operand, "r1") == 0) return r1;
    else if(strcmp(operand, "r2") == 0) return r2;
    else if(strcmp(operand, "r3") == 0) return r3;
    else if(strcmp(operand, "r4") == 0) return r4;
    else if(strcmp(operand, "r5") == 0) return r5;
    else if(strcmp(operand, "r6") == 0) return r6;
    else if(strcmp(operand, "r7") == 0) return r7;
    else if(strcmp(operand, "r8") == 0) return r8;
    else if(strcmp(operand, "r9") == 0) return r9;
    else if(strcmp(operand, "r11") == 0) return r11;
    else if(strcmp(operand, "r12") == 0) return r12;
    else if(strcmp(operand, "r13") == 0) return r13;
    else if(strcmp(operand, "r14") == 0) return r14;
    else if(strcmp(operand, "r15") == 0) return r15;
    else if(strcmp(operand, "r16") == 0) return r16;
    else if(strcmp(operand, "r17") == 0) return r17;
    else if(strcmp(operand, "r18") == 0) return r18;
    else if(strcmp(operand, "r19") == 0) return r19;
    else if(strcmp(operand, "r20") == 0) return r20;
    else if(strcmp(operand, "r21") == 0) return r21;
    else if(strcmp(operand, "r22") == 0) return r22;
    else if(strcmp(operand, "r23") == 0) return r23;
    else if(strcmp(operand, "r24") == 0) return r24;
    else if(strcmp(operand, "r25") == 0) return r25;
    else if(strcmp(operand, "r26") == 0) return r26;
    else if(strcmp(operand, "r27") == 0) return r27;
    else if(strcmp(operand, "r28") == 0) return r28;
    else if(strcmp(operand, "r29") == 0) return r29;
    else if(strcmp(operand, "r30") == 0) return r30;
    else if(strcmp(operand, "r31") == 0) return r31;
    //defualt being convert the string to int
    else return atoi(operand);

}

//load specified assembly program
//igrnores any lines beginning with '//' in the input program
void loadProgram(const char *filename){
    //open file
    FILE *programFile = fopen(filename, "r");
    if(programFile == NULL){
        printf("ERROR - File '%s' not found.\n", filename);
        exit(1);
    }

    //get next line
    char line[LINE_LEN];
    while(fgets(line, LINE_LEN, programFile)){
        //temp instruction
        struct instruction newInstruction;
        //dont do anything with comment lines
        if(line[0] != '/' && line[1] != '/'){
            int wordCount = 0;
            int charCount = 0;
            char word[256];
            for(int j = 0; j < LINE_LEN; j++){
                //after each instruction part, convert to correct format
                if(line[j] == ' ' || line[j] == '\n'){
                    switch(wordCount){
                        case 0: newInstruction.opCode = opcodeSTRtoENUM(word);
                                break;
                        case 1: newInstruction.operand1 = operandSTRtoENUM(word);
                                break;
                        case 2: newInstruction.operand2 = operandSTRtoENUM(word);
                                break;
                        case 3: newInstruction.operand3 = operandSTRtoENUM(word);
                                break;
                    }
                    wordCount ++;
                    memset(word, 0, sizeof(word));
                    charCount = 0;
                    continue;
                }
                //move on if comma or end of line
                if(line[j] == ',') continue;
                if(line[j] == '\n') break;
                word[charCount] = line[j];
                charCount ++;
            }
            //ensures all instructions have a correct instruction opcode
            if(newInstruction.opCode == -1){
                printf("Program file '%s' OpCode read incorrectly for instruction %d. Please check.\n", filename, instructionCount);
                exit(1);
            }
            //store instruction
            INSTR[instructionCount] = newInstruction;
            instructionCount ++;
        }
    }
    fclose(programFile);
    instructionCount = 0;
}

//print current system stats (finsihed, cycles, instructions, PC, RF, CurrentInstruction, PrevInstruction, NextInstruction, etc.)
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

void execute(int opcode, int operand1, int operand2, int operand3, int targetAddress){
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
    }
}

void decode(struct instruction currentInstruction){
    cycles++;
    int opcode = currentInstruction.opCode;
    int operand1 = currentInstruction.operand1;
    int operand2 = currentInstruction.operand2;
    int operand3 = currentInstruction.operand3;
    int targetAddress = 0;

    //calculate target address incase of load or store
    switch(opcode){
        case LD: targetAddress = RF[operand2] + operand3;
                break;
        case LDC: targetAddress = operand2;
                break;
        case STR: targetAddress = RF[operand2] + operand3;
                break;
        case STRC: targetAddress = operand2;
                break;
    }
    execute(opcode, operand1, operand2, operand3, targetAddress);
}

void fetch(){
    struct instruction currentInstruction = INSTR[PC];
    instructionCount ++;
    cycles ++;
    PC ++;
    decode(currentInstruction);
}

//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//

int main(int argc, char const *argv[])
{
    if(argc == 1){
        printUsageInfo();
        return 0;
    }

    initialize();
    loadProgram(argv[1]);
    while(finished == 0){
        fetch();
    }
    printSysInfo();
    return 0;
}
