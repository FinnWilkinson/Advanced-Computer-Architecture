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

int main(int argc, char const *argv[])
{
    while(finished == 0){
        fetch();
        decode():
        execute();
        instructions++;
        cycles += 3;
    }
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


