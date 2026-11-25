// Box.asm for Roll No: 2501730275 (K = 75)
// Starting row = 75 -> base screen address = 16384 + 32*75 = 18784
// Height = 20 rows
// Width  = 64 pixels = 4 words per row (offsets 0, 1, 2, 3)

(MAIN)
    @KBD
    D=M
    @DRAW_BOX
    D;JNE       // If any key is pressed (KBD != 0), draw box

    @ERASE_BOX
    0;JMP       // Otherwise, erase box

// Draws 20 rows x 4 words (-1 = all 16 bits black)
(DRAW_BOX)
    @18784
    D=A
    @rowAddr
    M=D         // rowAddr = 18784

    @20
    D=A
    @rowCount
    M=D         // rowCount = 20

(DRAW_ROW_LOOP)
    @rowCount
    D=M
    @MAIN
    D;JEQ       // Done all 20 rows -> re-check keyboard

    @rowAddr
    D=M
    @wordAddr
    M=D         // wordAddr = start of current row

    @4
    D=A
    @colCount
    M=D         // colCount = 4 words (64 pixels)

(DRAW_WORD_LOOP)
    @colCount
    D=M
    @NEXT_DRAW_ROW
    D;JEQ       // Done 4 words in this row

    @wordAddr
    A=M
    M=-1        // Set all 16 pixels in word to black

    @wordAddr
    M=M+1       // Next word to the right
    @colCount
    M=M-1
    @DRAW_WORD_LOOP
    0;JMP

(NEXT_DRAW_ROW)
    @32
    D=A
    @rowAddr
    M=D+M       // Advance to next screen row (+32 words)

    @rowCount
    M=M-1
    @DRAW_ROW_LOOP
    0;JMP

// Erases 20 rows x 4 words (0 = all 16 bits white/cleared)
(ERASE_BOX)
    @18784
    D=A
    @rowAddr
    M=D         // rowAddr = 18784

    @20
    D=A
    @rowCount
    M=D         // rowCount = 20

(ERASE_ROW_LOOP)
    @rowCount
    D=M
    @MAIN
    D;JEQ       // Done all 20 rows -> re-check keyboard

    @rowAddr
    D=M
    @wordAddr
    M=D         // wordAddr = start of current row

    @4
    D=A
    @colCount
    M=D         // colCount = 4 words (64 pixels)

(ERASE_WORD_LOOP)
    @colCount
    D=M
    @NEXT_ERASE_ROW
    D;JEQ

    @wordAddr
    A=M
    M=0         // Clear all 16 pixels in word

    @wordAddr
    M=M+1
    @colCount
    M=M-1
    @ERASE_WORD_LOOP
    0;JMP

(NEXT_ERASE_ROW)
    @32
    D=A
    @rowAddr
    M=D+M       // Advance to next screen row (+32 words)

    @rowCount
    M=M-1
    @ERASE_ROW_LOOP
    0;JMP
