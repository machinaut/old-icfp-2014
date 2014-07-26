; Fibonacci up in da haus
  LDC  0        ; Fibonacci index to calculate, falls through to fib_next
  LDF  fib      ; declare function fib
  AP   1        ; call fib with 1 arg (our num to calculate)
  RTN           ; end of program
fib:
  LD 0 0        ; pop our arg off the stack
  LDC 1
  CGT
  SEL fib_next fib_end
  RTN
fib_next:
  ; calc fib(n-1)
  LD 0 0        ; pop n
  LDC 1
  SUB           ; get n-1
  LDF fib
  AP 1          ; call fibonacci on it: fib(n-1)
  ; calc fib(n-2)
  LD 0 0        ; pop n
  LDC 2
  SUB           ; get n-2
  LDF fib
  AP 1          ; call fibonacci on it: fib(n-2)
  ; return fib(n-1) + fib(n-2)
  ADD
  JOIN
fib_end:
  LDC 1
  JOIN
