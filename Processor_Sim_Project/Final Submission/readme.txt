TO RUN THE SIMULATOR:
1. Ensure you are in the `Python_Sim` directory in the command line
2. The numpy package is required
3. Type `python Simulator_main.py Assembly_Programs\<FILE-NAME>.txt`
4. The following options can also be concatenated to the end of the command in step 3, each seperated by a single space, in any order
	- `--Verbose` can be used to see the processor state after each cycle.
	- `--2Way` or `--4Way` can be used to select 2 or 4 way superscalar. Without this option the processor runs in scalar, out of order mode.
	- `--ROBx` where x is any integer can be used to define the size of the Re-Order Buffer. The default is 128.
	- `--BPFixed` or `--BPStatic` or `--BPDynamic1` or `--BPDynamic2` can be used to select the type of branch predictor you would like. 
	   By default no branch predictor is used, unless you are super-scalar in which case the defualt is Fixed Branch Prediction.


The following assembly programs are available to run, and are loacted inside the Assembly_Programs directory inside Python_Sim directory:
 - Factorial.txt
 - Game_Of_Life.txt
 - Matrix_Multiplication.txt
 - Matrix_Multiplication_Unrolled.txt
 - Max_Throughput_Test.txt
 - Qucik_Sort.txt
 - Test_Script.txt
 - Vecotr_Addition.txt

At the top of each file commented out there will be the initial state once all data has been loaded into memory, as well as the final memory state or answer that is expected.
Each assembly program is looped 100 times by a branch in order to achieve more accurate IPC output values at the end - mitigating the intial data write to memory.


In the case of Game_Of_Life.txt, after each game iteration (there are 20 in total), the 'game board' (or processor state including memory) will be shown and enter must be pressed for the next iteration to be run.
The first game board to be shown will be after iteration 1 has completed, and so on.



The following list details the assembly instructions that the processor can execute:
 HALT                    # finished = 1 
 ADD rd, ra, rb          # RF[rd] = RF[ra] + RF[rb]
 ADDI rd, ra, x          # RF[rd] = RF[ra] + x                                                           (where 'x' is an immidiate constant)
 SUB rd, ra, rb          # RF[rd] = RF[ra] - RF[rb] 
 SUBI rd, ra, x          # RF[rd] = RF[ra] - x                                                           (where 'x' is an immidiate constant)
 MUL rd, ra, rb          # RF[rd] = RF[ra] * RF[rb]
 MULI rd, ra, x          # RF[rd] = RF[ra] * x                                                           (where 'x' is an immidiate constant)
 DIV rd, ra, rb          # RF[rd] = RF[ra] / RF[rb]                                                      (rounds to nearest int)
 DIVI rd, ra, x          # RF[rd] = RF[ra] / x                                                           (where 'x' is an immidiate constant)  (rounds to nearest int)
 LD rd, ra, rb		 # RF[rd] = MEM[ RF[ra] + RF[rb] ]                                               (where 'x' is an immidiate constant)
 LDC rd, ra, x		 # RF[rd] = MEM[ RF[ra] + x ]                                                    (where 'x' is an immidiate constant)
 STR ra, rd1, rd2	 # MEM[ RF[rd1] + RF[rd2] ] = RF[ra]                                             (where 'x' is an immidiate constant)
 STRC ra, rd, x		 # MEM[ RF[rd] + x ] = RF[ra]                                                    (where 'x' is an immidiate constant)
 CMP rd, ra, rb          # if RF[ra] > RF[rb] then RF[rd] = 1;    if RF[ra] = RF[rb] then RF[rd] = 0;     if RF[ra] < RF[rb] then RF[rd] = -1;
 JMP ra                  # PC = RF[ra]                                                                       
 BR x                    # PC = x                                                                        (where 'x' is an immidiate constant)
 BEQ ra, rb, x           # if RF[ra] = RF[rb] then PC = x;                                               (where 'x' is an immidiate constant)
 BLT ra, rb, x           # if RF[ra] < RF[rb] then PC = x;                                               (where 'x' is an immidiate constant)
 LSL rd, ra, x		 # RF[rd] = RF[ra] << x
 LSR rd, ra, x 		 # RF[rd] = RF[ra] >> x
 XOR rd, ra, rb		 # RF[rd] = RF[ra] XOR RF[rb]
 AND rd, ra, rb   	 # RF[rd] = RF[ra] AND RF[rb]
 MOD rd, ra, rb		 # RF[rd] = RF[ra] MOD RF[rb]
 PASUE			 # Print out the processor state


