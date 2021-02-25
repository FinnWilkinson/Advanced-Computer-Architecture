#include <Load_Assembly.h>

//load specified assembly program
//igrnores any lines beginning with '//' in the input program
void loadProgram(const char *filename, struct instruction *INSTR){
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