; Useful assembly routines
; cannot easily be represented in our lisp

; dup, duplicate a single item onto the stack (twice)
dup:
    LD 0 0
    LD 0 0
    RTN

; swap, call with two items, return with them in reverse order on the stack
swap:
    LD 0 1
    LD 0 0
    RTN

