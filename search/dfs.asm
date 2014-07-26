LDF  search
AP   0
RTN

search:
    ; Make new list with value 1
    LDC     0
    LDC     1
    CONS

    ; 3, to append to list
    LDC     3

    LDF     appendHead
    AP      2
    RTN

appendHead:
    ; Pop old list head, then new value
    LD      0 0
    LD      0 1

    ; Make new list head with new value, pointer to old list head
    ; Pushes new list head onto stack
    CONS
    RTN
