//structure holding an instruction and its opcodes for easier storage, passing, etc.
struct instruction
{
    int opCode;
    int operand1;
    int operand2;
    int operand3;
    int instructionNumber;
};

//enums for opocodes and registers for easy program load and conversion
enum instructions {HALT, ADD, ADDI, SUB, SUBI, MUL, MULI, DIV, DIVI, LD, LDC, STR, STRC, CMP, JMP, BR, BEQ, BLT};
enum registers {r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, 
              r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31};