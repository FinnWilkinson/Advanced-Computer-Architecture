# Advanced Computer Architecture
 
This repository contains my final year coursework project to make an emulation of either a scalar, or a super scalar out-of-order pipelined processor. Details of compilation, as well as the project code, can be found in the `Processor_Sim_Project/Python_Sim/` directory of this repository. 


 The following assembly programs are available to run, and are loacted within the `Assembly_Programs` sub-directory of the project. 
 All Assembly programs contain comments at the top to help explain what the script will do.
 - Factorial.txt
 - Game_Of_Life.txt
 - Matrix_Multiplication.txt
 - Matrix_Multiplication_Unrolled.txt
 - Max_Throughput_Test.txt
 - Qucik_Sort.txt
 - Test_Script.txt
 - Vecotr_Addition.txt


 The custom instructions set is as follows :
 | Instruction       | Description                                                                                                                                 
 | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------
 | `HALT`            |  finished = 1
 | `ADD rd, ra, rb`  |  RF[rd] = RF[ra] + RF[rb]                                                                                                                   
 | `ADDI rd, ra, x`  |  RF[rd] = RF[ra] + x                                                                                    
 | `SUB rd, ra, rb`  |  RF[rd] = RF[ra] - RF[rb]                                                                                                                   
 | `SUBI rd, ra, x`  |  RF[rd] = RF[ra] - x                                                                                    
 | `MUL rd, ra, rb`  |  RF[rd] = RF[ra] * RF[rb]                                                                                            
 | `MULI rd, ra, x`  |  RF[rd] = RF[ra] * x                                                           
 | `DIV rd, ra, rb`  |  RF[rd] = RF[ra] / RF[rb]                                                      
 | `DIVI rd, ra, x`  |  RF[rd] = RF[ra] / x      (Rounds to nearest integer)                                                            
 | `LD rd, ra, rb`   |  RF[rd] = MEM[ RF[ra] + RF[rb] ]                                                    
 | `LDC rd, ra, x`   |  RF[rd] = MEM[ RF[ra] + x ]                                                             
 | `STR ra, rd1, rd2`|  MEM[ RF[rd1] + RF[rd2] ] = RF[ra]                                                    
 | `STRC ra, rd, x`  |  MEM[ RF[rd] + x ] = RF[ra]                                                             
 | `CMP rd, ra, rb`  |  if RF[ra] > RF[rb] then RF[rd] = 1; if RF[ra] = RF[rb] then RF[rd] = 0; if RF[ra] < RF[rb] then RF[rd] = -1;
 | `JMP ra`          |  PC = RF[ra]                                   
 | `BR x`            |  PC = x                                    
 | `BEQ ra, rb, x`   |  if RF[ra] = RF[rb] then PC = x;           
 | `BLT ra, rb, x`   |  if RF[ra] < RF[rb] then PC = x; 
 | `LSL rd, ra, x`   |  RF[rd] = RF[ra] << x
 | `LSR rd, ra, x`   |  RF[rd] = RF[ra] >> x
 | `XOR rd, ra, rb`  |  RF[rd] = RF[ra] XOR RF[rb]
 | `AND rd, ra, rb`  |  RF[rd] = RF[ra] AND RF[rb]
 | `MOD rd, ra, rb`  |  RF[rd] = RF[ra] MOD RF[rb]
 | `PAUSE`           |  Print out the processor state

Noting that:
 - `x` is treated as an immediate constant.
 - `DIV` and `DIVI` are integer divisions, and will round to the nearest integer.
 - `RF` is the Register File / Array of General Purpose Registers. (In C it is defined as `int RF[32];`)
 - `RF[0]` or `r0` is always `0`.
 - `MEM[a]` is memory item at address `a`. (In C it is defined as `int MEM[1024];`)
 - When branching, labels can be used and referenced in the assembly code to denote functions as follows :
   - `Label:`
   - `ADD r4, r5, r6`
   - ...
   - `BR Label`

A presentation titled *slides.pdf* can also be found in the project directory. Contained within this presentation is a graphical representation of the super scalar processor, as well as key features and various experiments that were run.

 
