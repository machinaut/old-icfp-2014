; Useful assembly routines
; cannot easily be represented in our lisp

; dup, call with one argument, duplicate a single item onto the stack (twice)
dup:
    LD 0 0
    LD 0 0
    RTN

; swap, call with two items, return with them in reverse order on the stack
swap:
    LD 0 1
    LD 0 0
    RTN

; pop, call with a single argument, returns without it on the stack
;  effectively pops the top of the stack off
pop:
    RTN

; dprint, call with two arguments: thing to print, and ID to print with
;   returns the thing to print (so this evaluates as an expression)
dprint:
    LD 0 1  ; load ID
    DBUG    ; print ID
    LD 0 0  ; load thing to print
    DBUG    ; print thing
    LD 0 0  ; load thing again as our "return" value
    RTN
