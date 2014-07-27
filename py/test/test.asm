;Multi-line comments
; should be okay

    ;blank lines and tabs as well
LDC  21
LDF  4  ; load body
AP   1  ; call body with 1 variable in a new frame
RTN

; body
LD  0 0; var x    :body
LD   0  0  ; var x
ADD
RTN