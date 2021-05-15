// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@R0
D = M
@a
M = D // a = R0

@i
M = 0 // i = 1

@res
M = 0 // initially res = 0

(LOOP)
    @i
    D = M // load i
    @R1
    D = D - M // save b - i to check if loop is over
    
    @SAVE
    D;JGE   // if i >= b (loop is over) goto stop

    @a
    D = M
    @res
    M = M + D   // res += a (first integer)
    
    @i
    M = M + 1 // i++

    @LOOP
    0;JMP

(SAVE)
@res
D = M
@R2
M = D // RAM[2] = res

(inf)
@inf
0;JMP
