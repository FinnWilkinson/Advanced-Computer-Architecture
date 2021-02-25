#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <Instruction.h>

//initialise data and registers to 0.
void initialize();

//if no file provided, print error and info
void printUsageInfo();

//print current system stats (finsihed, cycles, instructions, PC, RF, CurrentInstruction, PrevInstruction, NextInstruction, etc.)
void printSysInfo();

struct instruction fetch(struct instruction nextInstruction);

int decode(struct instruction currentInstruction, int targetAddress);

int execute(int opcode, int operand1, int operand2, int operand3, int targetAddress);