; Build tuple
LDC     1
LDC     2
LDC     3
LDC     4
LDC     0
CONS
CONS
CONS
CONS

; We want 3rd element
LDC     3

; Call getN
LDF     getN
AP      2
RTN

; getN - gets Nth element from tuple onto stack
; takes 2 args - tuple, n
getN:
    LD      0 1     ; Get counter
    TSEL    getNNext getNDone
getNNext:
    LD      0 0
    CDR
    LD      0 1
    LDC     1
    SUB

    DUM     2
    LDF     getN
    TRAP    2
getNDone:
    LD      0 0
    CAR
    RTN
