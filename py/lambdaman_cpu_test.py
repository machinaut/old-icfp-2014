__author__ = 'joe'

import unittest
from lambdaman_cpu import LambdaManCPU


class TestLambdaManCPU_Interpretter(unittest.TestCase):

    def test_loading_program(self):
        cpu = LambdaManCPU()
        cpu.load('./test/test.asm')

    def test_printing_program(self):
        cpu = LambdaManCPU()
        cpu.load('./test/test.asm')
        cpu.print_prog()

    def test_executing_fib(self):
        cpu = LambdaManCPU()
        cpu.load('./test/fib.asm')
        cpu.print_prog()

        limit = 100
        limited = False

        #cpu.print_state()
        for tick in cpu:
            #cpu.print_state()
            if limited:
                if limit <= 0:
                    break
                limit -= 1

if __name__ == '__main__':
    unittest.main()