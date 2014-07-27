; DBUG and return argument
_debug:
    LD 0 0
    LD 0 0
    DBUG
    RTN

; DBUG both arguments, return second
_debug_tag:
    LD 0 1
    LD 0 1
    LD 0 0
    DBUG
    DBUG
    RTN
