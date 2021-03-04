# Advanced Computer Architecture
 
 This repository contains my final year coursework project to make a emulation of a processor. I have written the simulator in Python.

 To compile and run the simulator: `python Simulator_main.py "Assembly Programs/<CHOSEN_PROGRAM>.txt"` in the Python_Sim directory. 

 To compile and run the simulator with status update after each instruction execution: `python Simulator_main.py "Assembly Programs/<CHOSEN_PROGRAM>.txt" -verbose` 
 in the Python_Sim directory. 


 All Assembly programs contain comments at the top to help explain what the script will do.
 Available Assembly test programs :
  - `Quick_Sort.txt`
  - `Vector_Addition.txt`
  

 The external Dependancies are as follows :
  - `import os`
  - `import sys`
  - `import numpy as np`


 `Processor_Sim` contains the code for a simple scalar processor, which can read in instruction files (`.txt` format) and produce an output.
 The instructions set is as follows (also found in `Instructions.txt`):
 | Instruction       | Description                                                                                                                                 
 | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------
 | `ADD rd, ra, rb`  |  RF[rd] = RF[ra] + RF[rb]                                                                                                                   
 | `ADDI rd, ra, x`  |  RF[rd] = RF[ra] + x                                                                                    
 | `SUB rd, ra, rb`  |  RF[rd] = RF[ra] - RF[rb]                                                                                                                   
 | `SUBI rd, ra, x`  |  RF[rd] = RF[ra] - x                                                                                    
 | `MUL rd, ra, rb`  |  RF[rd] = RF[ra] * RF[rb]                                                                                            
 | `MULI rd, ra, x`  |  RF[rd] = RF[ra] * x                                                           
 | `DIV rd, ra, rb`  |  RF[rd] = RF[ra] / RF[rb]                                                      
 | `DIVI rd, ra, x`  |  RF[rd] = RF[ra] / x                                                            
 | `LD rd, ra, x`    |  RF[rd] = MEM[ RF[ra] + x ]                                                    
 | `LDC rd, x`       |  RF[rd] = MEM[ x ]                                                             
 | `STR ra, rd, x`   |  MEM[ RF[rd] + x ] = RF[ra]                                                    
 | `STRC ra, x`      |  MEM[ x ] = RF[ra]                                                             
 | `CMP rd, ra, rb`  |  if RF[ra] > RF[rb] then RF[rd] = 1; if RF[ra] = RF[rb] then RF[rd] = 0; if RF[ra] < RF[rb] then RF[rd] = -1;
 | `JMP ra`           |  PC = RF[ra]                                   
 | `BR x`            |  PC = x                                    
 | `BEQ ra, rb, x`   |  if RF[ra] = RF[rb] then PC = x;           
 | `BLT ra, rb, x`   |  if RF[ra] < RF[rb] then PC = x;           
 | `HALT`            |  finished = 1

Noting that:
 - `x` is treated as an immediate constant.
 - `DIV` and `DIVI` are integer divisions, and will round to the nearest integer.
 - `RF` is the Register File / Array of General Purpose Registers. (In C it is defined as `int RF[32];`)
 - `RF[0]` or `r0` is always `0`.
 - `MEM[a]` is memory item at address `a`. (In C it is defined as `int MEM[1024];`)



 I have created a structure in order to hold the opcode and operands, which is defined as :
 ``` c
 struct instruction
 {
     int opCode;
     int operand1;
     int operand2;
     int operand3;
 };
 ```
 Once instructions are read in, they are saved to a seperate instruction memory array, which in the source code is defined as `struct instruction INSTR[512];`.
 All opcodes and operands are treated as 32-bit integers, rather than combining them into a single 32-bit operation. 
 This decision was taken (in addition to it being in the coursework specification) to make the project simpler to code, 
 and adding this bit manipulation does not add anything to the simulator in terms of what it can do 
 (i.e. its functionality does not change, only its complexity to understand and to code). 

 