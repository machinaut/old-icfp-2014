Game Engine
===========

# lambdaMan-CPU interpreter
The lambdaMan-CPU interpreter executes lambdaMan assembly. (stored as a *.s file)
It can be given either a file to read from or have data piped to it from stdin.

    python3 lambdaman_cpu.py < ../gcc/samples/test.s
    
or

    python3 lambdaman_cpu.py ../gcc/samples/test.s

The interpreter currently supports the following commands:

 + LDC
 + LD
 + ADD
 + SUB
 + MUL
 + DIV
 + CEQ
 + CGTE
 + CGT
 + CONS
 + CAR
 + CDR
 + SEL
 + JOIN
 + LDF
 + AP
 + RTN
 + DUM
 + RAP
 + STOP