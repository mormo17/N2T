// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@KBD    // keyboard (24576)
D = A
@endLoop
M = D

(LOOP)
    @SCREEN
    D = A
    @addr
    M = D   //screen's base address
    
    @KBD    // keyboard (24576)
    D = M   // save input's value

    @WHITE  // id input's value equals zero, that means
    D; JEQ  // that no key is pressed and nothing should happen

    @BLACK  // otherwise fill screen with black pixels
    D; JGT

(WHITE)
    //@KBD  // keyboard
    //D = M // save input's value
    //@LOOP
    //D; JNE
    
    @endLoop
    D = M
    @addr
    D = D - M   

    @LOOP
    D; JEQ

    @addr
    A = M
    M = 0
    
    @addr
    M = M + 1

    @WHITE
    0; JMP

(BLACK)
    //@KBD  // keyboard
    //D = M // save input's value
    //@LOOP
    //D; JEQ

    @endLoop
    D = M
    @addr 
    D = D - M
    @LOOP
    D; JEQ

    @addr
    A = M
    M = -1
    @addr
    M = M + 1
      
    @BLACK
    0; JMP

