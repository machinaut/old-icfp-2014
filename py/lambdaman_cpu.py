__author__ = 'joe'


class LambdaManCPU:
    tag = ['TAG_INT',
           'TAG_CLOSURE',
           'TAG_PAIR',
           ]
    def __init__(self):
        #Instructions
        self.inst = []  # Program instructions

        #Registers
        self.c = 0  # %c: control register (program counter / instruction pointer)
        self.s = 0  # %s: data stack register
        self.d = 0  # %d: control stack register
        self.e = 0  # %e: environment frame register

        #Memory Stacks
        self.data = []      # Data stack
        self.control = []   # Control stack
        self.environ = []   # Environment frame chain
        self.heap = []      # Data heap

        #Initialization
        self.environ.append({'size': None,
                             'FRAME_PARENT': None,
                             'FRAME_VALUE': [],
                             'FRAME_TAG': 'TAG_ROOT'})
        self.control.append({'tag': 'TAG_STOP',
                             })
        #self.machine_stop = False

        #Instruction Closures
        self.instructions = {'ADD': self.add,
                             'SUB': self.sub,
                             'LDC': self.ldc,
                             'LDF': self.ldf,
                             'AP':  self.ap,
                             'RTN': self.rtn,
                             'LD':  self.ld,
                             }
    # Instruction Executors
    def ldc(self, args):
        """
        LDC - load constant

        Synopsis: load an immediate literal;
                  push it onto the data stack
        Syntax:  LDC $n
        Example: LDC 3
        Effect:
          %s := PUSH(SET_TAG(TAG_INT,$n),%s)
          %c := %c+1
        """
        self.data.append({'tag': 'TAG_INT', 'data': args[0]})
        self.c += 1

    def add(self, args):
        """
        ADD - integer addition

        Synopsis: pop two integers off the data stack;
                  push their sum
        Syntax: ADD
        Effect:
          $y,%s := POP(%s)
          $x,%s := POP(%s)
          if TAG($x) != TAG_INT then FAULT(TAG_MISMATCH)
          if TAG($y) != TAG_INT then FAULT(TAG_MISMATCH)
          $z := $x + $y
          %s := PUSH(SET_TAG(TAG_INT,$z),%s)
          %c := %c+1
        """
        y = self.data.pop()
        x = self.data.pop()

        if x['tag'] != 'TAG_INT':
            self.fault('TAG_MISMATCH')
        if y['tag'] != 'TAG_INT':
            self.fault('TAG_MISMATCH')
        z = x['data'] + y['data']
        self.data.append({'tag': 'TAG_INT', 'data': z})
        self.s = len(self.data)
        self.c += 1

    def sub(self, args):
        print('subtraction')
        self.c += 1

    def ldf(self, args):
        """
        LDF - load function

        Synopsis: allocate a fresh CLOSURE cell;
                  fill it with the literal code address and the current
                    environment frame pointer;
                  push the pointer to the CLOSURE cell onto the data stack
        Syntax:  LDF $f
        Example: LDF 634      ; absolute instruction addresses
        Effect:
          $x := ALLOC_CLOSURE($f,%e)
          %s := PUSH(SET_TAG(TAG_CLOSURE,$x),%s)
          %c := %c+1
        """
        x = self.alloc_closure(args[0], self.e)
        self.data.append({'tag': 'TAG_CLOSURE', 'data': x})
        self.c += 1

    def alloc_closure(self, address, environment):
        """
        allocate a fresh CLOSURE cell;
        fill it with the literal code address and the current environment frame pointer;
        """
        self.heap.append({'address': address, 'environment': environment})
        return len(self.heap)-1

    def ap(self, args):
        """
        AP - call function

        Synopsis: pop a pointer to a CLOSURE cell off the data stack;
                  allocate an environment frame of size $n;
                  set the frame's parent to be the environment frame pointer
                    from the CLOSURE cell;
                  fill the frame's body with $n values from the data stack;
                  save the environment pointer and return address
                    to the control stack;
                  set the current environment frame pointer to the new frame;
                  jump to the code address from the CLOSURE cell;
        Syntax:  AP $n
        Example: AP 3      ; number of arguments to copy
        Effect:
          $x,%s := POP(%s)            ; get and examine function closure
          if TAG($x) != TAG_CLOSURE then FAULT(TAG_MISMATCH)
          $f := CAR_CLOSURE($x)
          $e := CDR_CLOSURE($x)
          $fp := ALLOC_FRAME($n)      ; create a new frame for the call
          FRAME_PARENT($fp) := $e
          $i := $n-1
          while $i != -1 do           ; copy n values from the stack into the frame in reverse order
          begin
            $y,%s := POP(%s)
            FRAME_VALUE($fp,$i) := $y
            $i := $i-1
          end
          %d := PUSH(%e,%d)                     ; save frame pointer
          %d := PUSH(SET_TAG(TAG_RET,%c+1),%d)  ; save return address
          %e := $fp                             ; establish new environment
          %c := $f                              ; jump to function
        """
        n = args[0]
        x = self.data.pop()        # get and examine function closure
        if x['tag'] != 'TAG_CLOSURE':
            self.fault('TAG_MISMATCH')
        f = self.heap[x['data']]['address']
        e = self.heap[x['data']]['environment']
        fp = self.alloc_frame(n)  # create a new frame for the call
        self.environ[fp]['FRAME_PARENT'] = e
        i = n-1
        while i != -1:
            y = self.data.pop()
            self.environ[fp]['FRAME_VALUE'].append(y)
            i = i-1
        self.control.append(self.e)                 # save frame pointer
        self.control.append({'tag': 'TAG_RET',      # save return address
                             'data': self.c+1})
        self.d = len(self.control)

        self.e = fp     # establish new environment
        self.c = f      # jump to function

    def fault(self, msg):
        print("system fault error: ", msg)
        self.print_state()

    def alloc_frame(self, size):
        self.environ.append({'size': size, 'FRAME_PARENT': None, 'FRAME_VALUE': [], 'FRAME_TAG': 'TAG_NOT_DUM'})
        return len(self.environ)-1

    def car(self, args):
        self.c += 1

    def cdr(self, args):
        self.c += 1

    def rtn(self, args):
        """
        RTN - return from function call

        Synopsis: pop a return address and environment frame pointer off of the control stack;
                  restore the environment;
                  jump to the return address
        Syntax:  RTN
        Effect:
          $x,%d := POP(%d)            ; pop return address
          if TAG($x) == TAG_STOP then MACHINE_STOP
          if TAG($x) != TAG_RET then FAULT(CONTROL_MISMATCH)
          $y,%d := POP(%d)            ; pop frame pointer
          %e := $y                    ; restore environment
          %c := $x                    ; jump to return address
        Notes:
          Standard ABI convention is to leave the function return value on the
          top of the data stack. Multiple return values on the stack is possible,
          but not used in the standard ABI.

          The latest hardware revision optimizes the deallocation of the
          environment frame. If the environment has not been captured by LDF
          (directly or indirectly) then it can be immediately deallocated.
          Otherwise it is left for GC.
        """
        x = self.control.pop()      # pop return address
        if x['tag'] == 'TAG_STOP':
            self.machine_stop()
            return
        if x['tag'] != 'TAG_RET':
            self.fault('CONTROL_MISMATCH')
        y = self.control.pop()      # pop frame pointer #TODO The manual is wrong?
        self.e = y                  # restore environment
        self.c = x['data']          # jump to return address

    def machine_stop(self):
        raise StopIteration

    def ld(self, args):
        """
        LD - load from environment

        Synopsis: load a value from the environment;
                  push it onto the data stack
        Syntax:  LD $n $i
        Example: LD 0 1
        Effect:
          $fp := %e
          while $n > 0 do            ; follow chain of frames to get n'th frame
          begin
            $fp := FRAME_PARENT($fp)
            $n := $n-1
          end
          if FRAME_TAG($fp) == TAG_DUM then FAULT(FRAME_MISMATCH)
          $v := FRAME_VALUE($fp, $i) ; i'th element of frame
          %s := PUSH($v,%s)          ; push onto the data stack
          %c := %c+1
        Notes:
          Values within a frame are indexed from 0.
        """
        n = args[0]
        i = args[1]
        fp = self.e
        while n > 0:            # follow chain of frames to get n'th frame
            fp = self.frame_parent(fp)
            n = n-1
        if self.frame_tag(fp) == 'TAG_DUM':
            self.fault('FRAME_MISMATCH')
        v = self.frame_value(fp, i)     # i'th element of frame
        self.data.append(v)             # push onto the data stack
        self.s = len(self.data)
        self.c += 1

    def frame_parent(self, frame_ptr):
        return self.environ[frame_ptr]['FRAME_PARENT']

    def frame_tag(self, frame_ptr):
        return self.environ[frame_ptr]['FRAME_TAG']

    def frame_value(self, frame_ptr, element):
        return self.environ[frame_ptr]['FRAME_VALUE'][element]

    def __iter__(self):
        return self

    def __next__(self):
        self.tick()

    def tick(self):
        execute = self.inst[self.c]
        if execute['inst'] in self.instructions:
            self.instructions[execute['inst']](execute['args'])

        if self.c >= len(self.inst):
            raise StopIteration


    def load(self, source):
        with open(source) as source_stream:
            for line in source_stream:
                asm, __, __ = line.rstrip().partition(';')  # Remove comments and newline
                instruction, __, args = asm.partition(' ')  # Extract the instruction parts
                args = args.strip().split(' ')  # Extract arguments
                if args != ['']:
                    args = list(map(int, args))  # Convert arguments to ints
                else:
                    args = []
                self.inst.append({'inst': instruction, 'args': args})

    def print_prog(self):
        for line in self.inst:
            print(line)

    def print_state(self):
        print('')
        print('Control Register: ', self.c)
        print('Instruction: ', self.inst[self.c])
        print('Data Ptr:   ', self.s)           # %s: data stack register
        print('Data Stack: ', self.data)        # Data stack
        print('Control Stack Ptr: ', self.d)    # %d: control stack register
        print('Control: ', self.control)        # Control stack
        print('Environment Ptr: ', self.e)      # %e: environment frame register
        if len(self.environ) != 0:
            print('Environment: ', self.environ[self.e])    # Environment frame chain
        else:
            print('Enivronment: NONE')
        print('Heap: ', self.heap)
        print('')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("Execute λ-LISP programs")
    parser.add_argument('source', nargs='?', default='/dev/stdin', help="File to compile (default=stdin)")
    args = parser.parse_args()

    cpu = LambdaManCPU()
    cpu.load(args.source)
    cpu.print_prog()

    cpu.print_state()
    for tick in cpu:
        cpu.print_state()

