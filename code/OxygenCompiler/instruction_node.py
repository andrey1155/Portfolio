from ASM_compiler.codegen.calculator import Calculator
from ASM_compiler.lexer.tokens import NumberToken
from ASM_compiler.lexer.tokens import WordToken
from ASM_compiler.parser_.ASTNodes import *
from ASM_compiler.VMres.instructions_list import I_MOV


class CoedeBlockNode:
    def __init__(self, instructs, lm, initial_address = 0):
        self.instructs = instructs
        self.calculate_addresses(initial_address, lm)

    def calculate_addresses(self, start, lm):
        current = start
        for instr in self.instructs:
            instr.set_address(current)
            current = instr.get_next_address(lm)



    def __repr__(self):
        repr = "\n"
        for i in self.instructs:
            repr += i.__repr__()
        return repr




class InstructionNode:

    def __init__(self, instr, line, args = []):
        self.instr = instr
        self. args = args
        self.length = 1
        self.address = 0
        self.line = line

        if instr == I_MOV:
            self.length = 2

    def set_address(self,address):
        self.address = address

    def get_next_address(self, lm):
        self.simplify(lm)
        return self.address + self.length



    def __repr__(self):
        rep = f"{self.instr}"
        if len(self.args)==0: return rep + '\n'
        for arg in self.args:
            rep += ' '
            rep += arg.__repr__()
            rep += ","
        rep = rep[0:-1]
        rep += '\n'
        return rep

    def simplify(self, lm):


        for i in range(len((self.args))):

            if isinstance(self.args[i], NumberNode):
                repr16 = self.args[i].tok.repr16
                if repr16 > 0xFF:
                    self.length = 2

            if (not isinstance(self.args[i],RegisterNode)) and (not isinstance(self.args[i],NumberNode)) \
                    and (not isinstance(self.args[i],DirectionNode))and (not isinstance(self.args[i],WordToken)):
                c = Calculator()
                res = c.calculate(self.args[i],lm,self.address)
                self.args[i] = NumberNode(NumberToken(res,self.line))


