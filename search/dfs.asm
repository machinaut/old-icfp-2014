; main - returns tick func
; empty state for now
LDC     0

; ai function - takes state and board
LDF     ai
CONS
RTN

; ai - returns next state and movement
ai:
    ; Empty next state
    LDC     0

    ; initiate search, return best value
    LD      0 0
    LD      0 1
    LDF     search
    AP      2
    RTN

; search - returns best movement
search:
    LD      0 1 ; Get world state onto stack (second arg)
    CAR         ; Get map (first state elem value)

    LD      0 1 ; Get world state onto stack (second arg)
    CDR         ; Get 2nd state elem onto stack
    CAR         ; Get l-man status onto stack

    CDR         ; Get 2nd l-man status onto stack
    CAR         ; Get l-man x,y

    LDF     getWorld
    AP 2
    DBUG

    ; empty state for now
    LDC     0
    ; always return right for now
    LDC     1
    CONS
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

; getWorld - gets (x,y) in world
; takes 2 args - world map, (x, y)
getWorld:
    ; Get x - row
    LD      0 0
    LD      0 1
    CDR
    LDF     getN
    AP      2

    ; Now column tuple is on stack
    ; Get y - column
    LD      0 1
    CAR
    LDF     getN
    AP      2

    ; Now element is on stack
    RTN
