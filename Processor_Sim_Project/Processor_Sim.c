#include <stdlib.h>
#include <stdio.h>

int finished = 0;
int cycles = 0;
int instructions = 0;
int PC = 0;

int RF[32];
int MEM[1024];
int INSTR[512];

enum instruction{ADD, ADDI, SUB, SUBI, MUL, MULI, DIV, DIVI, LD, LDC, STR, STRC, CMP, JMP, BR, BEQ, BLT, HALT};
enum register{r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, 
              r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31};

int main(int argc, char const *argv[])
{
    printf("%d\n", r12);
    /*while(finished == 0){
        fetch();
        decode():
        execute();
        instructions++;
        cycles += 3;
    }*/
    return 0;
}

//initialise data and registers to 0.
void initialize(){
    for (int i = 0; i < 32; i++)
    {
        RF[i] = 0;
        MEM[i] = 0;
        INSTR[i] = 0;
    }
    for (int i = 32; i < 512; i++)
    {
        MEM[i] = 0;
        INSTR[i] = 0;
    }
    for (int i = 512; i < 1024; i++)
    {
        MEM[i] = 0;
    }   
}

void printSysInfo(){
    //print current system stats (finsihed, cycles, instructions, PC, RF, CurrentInstruction, PrevInstruction, NextInstruction)
}


