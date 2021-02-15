#include <stdlib.h>
#include <stdio.h>

int finished = 0;
int cycles = 0;
int instructions = 0;
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

enum instructions {ADD, ADDI, SUB, SUBI, MUL, MULI, DIV, DIVI, LD, LDC, STR, STRC, CMP, JMP, BR, BEQ, BLT, HALT};
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

//load specified assembly program
void loadProgram(char *filename){
    //igrnore any '//' in the input program
    printf("%s\n", filename);
}

//print current system stats (finsihed, cycles, instructions, PC, RF, CurrentInstruction, PrevInstruction, NextInstruction, etc.)
void printSysInfo(){
    //for testing vector additon script
    for (int i = 0; i < 10; i++)
    {
        printf("a[%d] = %d \n", i, MEM[i]);
        printf("b[%d] = %d \n", i, MEM[10 + i]);
        printf("c[%d] = %d \n", i, MEM[20 + i]);
    }
    
}

//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//

void fetch(){

}

void decode(){

}

void execute(){

}

//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//

int main(int argc, char const *argv[])
{
    initialize();
    loadProgram("VectorAddition.txt");
    /*while(finished == 0){
        fetch();
        decode():
        execute();
        instructions++;
        cycles += 3;
    }*/
    return 0;
}
