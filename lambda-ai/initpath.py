#!/usr/bin/env python
# generate the initpath function.  muahahaha

def letterToDir(l):
    if l == 'u':
        return 0
    elif l == 'r':
        return 1
    elif l == 'd':
        return 2
    elif l == 'l':
        return 3
    return -1

# format is pairs of (direction, count) to go count times in that direction
p = [ ('r',6),
      ('d',2),
      ('r',2),
      ('u',2),
      ('r',2),
      ('u',2),
      ('l',4),
      ('u',8),

      ('r',4),
      ('u',5),
      ('l',9),
      ('d',3),
      ('l',2),
      ('u',3),
      ('l',9),
      ('d',5),
      ]

close = 1
print '(defun initPath ( )'
for seg in p:
    d = letterToDir(seg[0])
    for i in range(seg[1]):
        print '   (cons %d ' % d
        close += 1
print '    0 '+')'*close
