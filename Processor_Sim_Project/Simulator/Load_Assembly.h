#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <Instruction.h>

#define LINE_LEN 256

//convert between instruction string read from file and enum version
int opcodeSTRtoENUM(char *opcode);

//converts operand into associated register enum index, or the directly to an int if an immediate operand
int operandSTRtoENUM(char *operand);

//load specified assembly program
//igrnores any lines beginning with '//' in the input program
void loadProgram(const char *filename);

