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
        cpu.control.append({'tag': 'TAG_STOP'})

        limit = 100
        for _ in cpu:
            if limit <= 0:
                self.assertTrue(False, 'Too many steps execute.  Something is broken')
                break
            limit -= 1

    def test_executing_goto(self):
        cpu = LambdaManCPU()
        cpu.load('./test/goto.asm')
        cpu.control.append({'tag': 'TAG_STOP'})

        limit = 100
        for _ in cpu:
            if limit <= 0:
                break
            limit -= 1

    def test_executing_tmp(self):
        cpu = LambdaManCPU()
        cpu.load('./test/tmp.asm')
        cpu.control.append({'tag': 'TAG_STOP'})

        limit = 100
        for _ in cpu:
            if limit <= 0:
                self.assertTrue(False, 'Too many steps execute.  Something is broken')
                break
            limit -= 1

    def test_executing_test(self):
        cpu = LambdaManCPU()
        cpu.load('./test/test.asm')
        cpu.control.append({'tag': 'TAG_STOP'})

        limit = 100
        for _ in cpu:
            if limit <= 0:
                self.assertTrue(False, 'Too many steps execute.  Something is broken')
                break
            limit -= 1

    def test_executing_goright(self):
        cpu = LambdaManCPU()
        cpu.load('./test/goRight.asm')
        cpu.control.append({'tag': 'TAG_STOP'})

        limit = 100
        for _ in cpu:
            if limit <= 0:
                self.assertTrue(False, 'Too many steps execute.  Something is broken')
                break
            limit -= 1

    def test_executing_goright4(self):
        cpu = LambdaManCPU()
        cpu.load('./test/goRight.asm')
        cpu.control.append({'tag': 'TAG_STOP'})


        limit = 100
        cpu.c = 4
        cpu.print_state()
        cpu.state = 'RUNNING'
        for _ in cpu:
            cpu.print_state()
            if limit <= 0:
                self.assertTrue(False, 'Too many steps execute.  Something is broken')
                break
            limit -= 1
        cpu.print_state()





if __name__ == '__main__':
    unittest.main()