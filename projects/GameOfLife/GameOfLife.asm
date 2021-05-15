// The game of life world consists of 2D grid 16x32, the grid is mapped in memory:
// RAM[100] == grid(0, 0)
// RAM[132] == grid(1, 0)
// RAM[611] == grid(15, 31)
//
// RAM[99] contains number of generations to iterate over the Game of life world (aka grid)
//
// Iteration rules:
// For a space that is 'populated':
// * Each cell with one or no neighbors dies, as if by solitude.
// * Each cell with four or more neighbors dies, as if by overpopulation.
// * Each cell with two or three neighbors survives.
//
// For a space that is 'empty' or 'unpopulated'
// * Each cell with three neighbors becomes populated.
//
// initial values are set by test. The are only two values allowed:
// 1 -- the cell is populated
// 0 -- the cell is empty


//save number of iterations to RAM[0]
@99
D=M
@0
M=D

(LOOP)
//Draw every state of the board
@Pre_Draw_Board
0;JMP
(Draw_FINISH)

@0
D=M
//continue iterations while RAM[0] != 0
@exit
D;JEQ //if RAM[0]==0

//decrement number of iterations
@0
M=M-1

@100
D=A //save start point address
@1 //load i to be 100, initial coordinate of "grid"
M=D

//save current board state
//new board is from RAM[612] to RAM[1123]
(SAVE_BOARD)
//continue process while i != 612
@1
D=M
@612
D=D-A
@PRE_CHANGE_CONDITIONS
D;JEQ

//save current point's state in RAM[2]
@1
A=M
D=M //save whether state is 1 or 0
@2
M=D //copy to RAM[2]
//map to new point
@1
D=M
@512
D=A+D //i+512
// A=D @612
// D=A
//save dest point's address to RAM[3]
@3
M=D

@2
D=M //toCopy's state
@3
A=M //move to toCopy's address
M=D //copy state

//i++
@1
M=M+1
@SAVE_BOARD
0;JMP

(Pre_Draw_Board)
@100
D=A
@1
M=D //save start point

@SCREEN
D=A
@2
M=D //save start point of screen

(Draw_Board)
//continue provess while all points are not updated
@1
D=M
@612
D=D-A
@Draw_FINISH
D;JEQ

@1
D=M
A=D
D=M //current point's state
@3
M=D //save current point's state
@2
D=M
@5 //save tmp address for screen
M=D
@i
M=0

//draw square
(Inner_loop)
@i
D=M
@16
D=D-A
@NEXT_ITERATION
D;JEQ

@3
D=M
@7
M=D

@3
D=M
@fill_with_zeroes //doesnt need to paint
D;JEQ

//needs to be painted
@5
A=M
M=-1 

(inner_next_iteration)
@i
M=M+1
@5
D=M
@32
D=D+A
@5
M=D
@Inner_loop
0;JMP

(NEXT_ITERATION)
//i++
@1
M=M+1

@2 //increment initial screen address
M=M+1
D=M
@SCREEN
D=D-A
@31
D=D&A
@JUMP
D;JEQ

@Draw_Board
0;JMP

//check edge case
(JUMP)
@480
D=A
@2
M=M+D
@Draw_Board
0;JMP

(fill_with_zeroes)
@5
A=M
M=0
@inner_next_iteration
0;JMP

(PRE_CHANGE_CONDITIONS)
@100
D=A
@1
M=D //save current toChange point's address in RAM[1]

(CHANGE_CONDITIONS)
//continue process while RAM[1] != 612
@1
D=M
@612
D=A-D
@LOOP
D;JEQ

@2 //save number of populated neighbours
M=0

//first check if address will be valid
//check lower bound
@1
D=M //curr
@33
D=D-A //curr-33
@4
M=D //save curr-33
@100
D=D-A
@check2
D;JLT // if < 0, it means point is out of bounds

//check out of edges
@31
D=D-A
@31
D=D&A
@check2
D;JEQ // if == 0, it means point is out of bounds
      
//find upper-left neighbour
//ADDRESS: current - 33 + 512
@4
D=M //curr-33
@512
D=A+D //curr-33+512
A=D 
D=M //upper-left neighbour's state

D=D-1
@increment.1 //POPULATED
D;JEQ
@check2
0;JMP

//increments populated
(increment.1)
@2
M=M+1

(check2)
//first check if address will be valid
//check lower bound
@1
D=M //curr
@32
D=D-A //curr-32
@4
M=D //save curr-32
@100
D=D-A
@check3
D;JLT // if < 0, it means point is out of bounds

//find upper neighbour
//ADDRESS: current + 512 - 32
@4
D=M //curr-32
@512
D=A+D //curr-32+512
A=D 
D=M //upper neighbour's state

D=D-1
@increment.2 //POPULATED
D;JEQ
@check3
0;JMP

//increments populated
(increment.2)
@2
M=M+1

(check3)
//first check if address will be valid
//check lower bound
@1
D=M //curr
@31
D=D-A //curr-31
@4
M=D //save curr-31
@100
D=D-A
@check4
D;JLT // if < 0, it means point is out of bounds

//check if address is edge
@31 
D=D&A
@check4
D;JEQ // if == 0, it means point is out of bounds

//find upper-right neighbour
//ADDRESS: current + 512 - 31
@4
D=M //curr-31
@512
D=A+D //curr-31+512
A=D 
D=M //upper-right neighbour's state

D=D-1
@increment.3 //POPULATED
D;JEQ
@check4
0;JMP

//increments populated
(increment.3)
@2
M=M+1

(check4)
//first check if address will be valid
//check lower bound
@1
D=M //curr
@1
D=D-A //curr-1
@4
M=D //save curr-1
@100
D=D-A
@check5
D;JLT // if < 0, ict means point is out of bounds


//check if address is edge
@31
D=D-A
@31
D=D&A
@check5
D;JEQ // if == 0, it means point is out of bounds

//find left neighbour
//ADDRESS: current + 512 - 1
@4
D=M //curr-1
@512
D=A+D //curr-1+512
A=D 
D=M //left neighbour's state

D=D-1
@increment.4 //POPULATED
D;JEQ

@check5
0;JMP
//increments populated
(increment.4)
@2
M=M+1

(check5)
//first check if address will be valid
//check upper bound
@1
D=M //curr
@1
D=D+A //curr+1
@4
M=D //save curr+1
@612
D=D-A
@check6
D;JGE //if >= 0, it means point is out of bounds

//check if address is edge
@4
D=M
@100
D=D-A
@31
D=D&A
@check6
D;JEQ // if == 0, it means point is out of bounds

//find right neighbour
//ADDRESS: current + 512 + 1
@4
D=M //curr+1
@512
D=A+D //curr+1+512
A=D 
D=M //right neighbour's state

D=D-1

@increment.5 //POPULATED
D;JEQ
@check6
0;JMP

//increments populated
(increment.5)
@2
M=M+1

(check6)
//first check if address will be valid
//check upper bound
@1
D=M //curr
@31
D=D+A //curr+31
@4
M=D //save curr+31

@612
D=D-A
@check7
D;JGE //if >= 0, it means point is out of bounds


//check if address is edge
@4
D=M
@131
D=D-A
@31
D=D&A

@check7
D;JEQ // if == 0, it means point is out of bounds

//find lower-left neighbour
//ADDRESS: current + 512 + 31
@4
D=M //curr+31
@512
D=A+D //curr+31+512
A=D 
D=M //lower-left neighbour's state

D=D-1
@increment.6 //POPULATED
D;JEQ
@check7
0;JMP

//increments populated
(increment.6)
@2
M=M+1

(check7)

//first check if address will be valid
//check upper bound
@1
D=M //curr
@32
D=D+A //curr+32
@4
M=D //save curr+32
@612
D=D-A
@check8
D;JGE //if >= 0, it means point is out of bounds


//find lower neighbour
//ADDRESS: current + 512 + 32
@4
D=M //curr+32
@512
D=A+D //curr+32+512
A=D 
D=M //lower neighbour's state

D=D-1
@increment.7 //POPULATED
D;JEQ

@check8
0;JMP

//increments populated
(increment.7)
@2
M=M+1

(check8)

//first check if address will be valid
//check upper bound
@1
D=M //curr
@33
D=D+A //curr+33
@4
M=D //save curr+33
@612
D=D-A
@update_point
D;JGE //if >= 0, it means point is out of bounds

//check if address is edge
@4
D=M
@100
D=D-A
@31
D=D&A
@update_point
D;JEQ // if == 0, it means point is out of bounds

//find lower-right neighbour
//ADDRESS: current + 512 + 33
@4
D=M //curr+33

@512
D=A+D //curr+33+512

A=D 
D=M //lower-right neighbour's state

D=D-1
@increment.8 //POPULATED
D;JEQ

@update_point
0;JMP


//increments populated
(increment.8)
@2
M=M+1

(update_point)
@1
D=M //curr
A=D 
D=M //curr's state

@update_unpopulated
D;JEQ

D=D-1
@update_populated
D;JEQ

(update_unpopulated)
@2
D=M
@3
D=D-A
@make_alive
D;JEQ
@increment_initial
0;JMP

(make_alive)
@1
D=M
A=D
M=1
@increment_initial
0;JMP

(update_populated)
//if has zero neighbours
@2
D=M
@0
D=D-A
@kill
D;JEQ

//if has one neighbour
@2
D=M
@1
D=D-A
@kill
D;JEQ

//if has two neighbours
@2
D=M
@2
D=D-A
@make_alive
D;JEQ

//if has three neighbours
@2
D=M
@3
D=D-A
@make_alive
D;JEQ

//if has four neighbours
@2
D=M
@4
D=D-A
@kill
D;JGE

@increment_initial
0;JMP

(kill)
@1
D=M
A=D
M=0
@increment_initial
0;JMP

(increment_initial)
@1
M=M+1
@CHANGE_CONDITIONS
0;JMP

//final infinite loop
(exit)
@exit
0;JMP