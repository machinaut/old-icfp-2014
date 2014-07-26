  LDC  21
  LDF  body     ; load body
  AP   1        ; call body with 1 variable in a new frame
  RTN
body:
  LD   0 0      ; var x
  LD   0 0      ; var x
  ADD
  RTN
