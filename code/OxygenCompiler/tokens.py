import ASM_compiler.VMres.globals as globals
from ASM_compiler.VMres.instructions_list import *
from ASM_compiler.VMres.words_list import *

instructions = [I_LOAD,
I_LOADB,
I_LOADBI,

I_STORE,
I_STOREB,
I_STOREBI,

I_MOV,

I_AND, I_OR,
I_NOT, I_XOR,

I_ADD,              I_FADD,
I_SUB,              I_FSUB,
I_MUL,              I_FMUL,
I_DIV,   I_UDIV,    I_FDIV,

I_EXP, I_SQRT, I_LN,

I_SHIFT,


I_BR,I_BRE,I_BRL,I_BRG,I_BRLE,I_BRGE,I_BRNE,

I_JSR,

I_RET,


I_INC, I_DEC, I_INV,

I_PUTI,
I_PUTUI,
I_PUTF,
I_PUTC,
I_GETC,
I_PUSH,
I_POP,
I_HALT,

I_CLS,

I_CMP, I_BCMP, I_BINV,

I_PLD, I_PST, I_DLD, I_DST]

spec_words = [
    SW_VAR, SW_STRING, SW_DEF,SW_DATA, SW_CODE
]

regs = [R_0, R_1, R_2, R_3, R_4, R_BP, R_SP, R_BUFF, R_PC, R_COND, R_SUB]

directives = [D_LABEL, D_DEFINE, D_ENTRY, D_MACRO, D_INCLUDE, D_ENDMACRO]

math_ops = ['[',']', '(', ')', '+','-','*','/']

TT_PLUS = '+'
TT_MINUS = '-'
TT_MUL = '*'
TT_DIV = '/'
TT_LPAREN = '('
TT_RPAREN = ')'

TT_INSTR = "TT_INSTR"
TT_NUM   = "TT_NUM"
TT_WORD  = "TT_WORD"
TT_SPEC_WORD   = "TT_SPEC_WORD"
TT_STRING   = "TT_STRING"
TT_DIRECTION = "TT_DIRECTION"
TT_DDOT = "TT_DDOT"
TT_REG = "TT_REGISTER"
TT_CURRENT_MEM = "TT_CURRENT_ADDRESS"
TT_COMA = "TT_COMA"
TT_EOF = "TT_EOF"
TT_EOS = "TT_EOS"
TT_DIRECTIVE = "TT_DIRECTIVE"
TT_CHAR = "TT_CHAR"

class Token:

    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.long = False
        self.line = line


class InstrToken(Token):
    def __init__(self, instr, line):
        super(InstrToken, self).__init__(TT_INSTR, instr, line)

    def __repr__(self):
        return f"instruction: {self.value}"


class RegisterToken(Token):
    def __init__(self, r_name, line):
        super(RegisterToken, self).__init__(TT_REG, r_name, line)

    def __repr__(self):
        return f"register: {self.value}"


class NumberToken(Token):
    def __init__(self, num, line, ntype = None):
        super(NumberToken, self).__init__(TT_NUM, num, line)
        self.long = False

        if ntype == None:
            if type(num) == float:
                self.ntype = "float"
                self.long = True
            elif int(num) > pow(2,15)-1:
                self.ntype = "uint"
                self.long = True
            else:
                self.ntype = "int"
        else:
            self.ntype = ntype

        self.repr16 = 0


        if self.ntype == "int":
            self.repr16 = num
            if self.repr16 > 255: self.long = True
        if self.ntype == "uint":
            self.repr16 = num
            self.long = True
        if self.ntype == "int" and num < 0:
            t = abs(num)
            t = ~t
            t |= 1 << 15
            t += 1
            self.repr16 = t & 0xFFFF
            self.long = True
        if self.ntype == "float":
            self.repr16 = globals.float_to_fnum(num)
            self.long = True


    def __repr__(self):
        return f"{self.type}: {self.value}"


class WordToken(Token):
    def __init__(self, word, line):
        super(WordToken, self).__init__(TT_WORD, word, line)

    def __repr__(self):
        return f"word: {self.value}"

    def __eq__(self, other):
        if type(other) == str:
            if self.value == other:
                return True
            else: return False
        raise  Exception()

class SpecWordToken(Token):
    def __init__(self, word, line):
        super(SpecWordToken, self).__init__(TT_SPEC_WORD, word, line)
        self.long = False

    def __repr__(self):
        return f"spc word: {self.value}"

class StringToken(Token):
    def __init__(self, value, line):
        super(StringToken, self).__init__(TT_STRING, value, line)

    def __repr__(self):
        return f"string: {self.value}"




class DirectionToken(Token):
    def __init__(self, value, line):
        super(DirectionToken, self).__init__(TT_DIRECTION, value, line)

    def __repr__(self):
        return f"direction: {self.value}"

class DDOTToken(Token):
    def __init__(self):
        super(DDOTToken, self).__init__(TT_DDOT, '')

    def __repr__(self):
        return f": {self.value}"




class EOFToken(Token):
        def __init__(self, line = 0):
            super(EOFToken, self).__init__(TT_EOF, '', line)

        def __repr__(self):
            return "EOF"

class EOSToken(Token):
        def __init__(self, line):
            super(EOSToken, self).__init__(TT_EOS, '', line)

        def __repr__(self):
            return "TT_EOS"

class CommentaryToken(Token):
    def __init__(self, value=''):
        super(CommentaryToken, self).__init__("Commentary", value)

    def __repr__(self):
        return "Commentary"

class DirectiveToken(Token):
    def __init__(self, value, line):
        super(DirectiveToken, self).__init__(TT_DIRECTIVE, value, line)

    def __repr__(self):
        return f"Directive {self.value}"

class CURRENT_MEM_Token(Token):
    def __init__(self, line):
        super(CURRENT_MEM_Token, self).__init__(TT_CURRENT_MEM, '', line)
        self.type = TT_CURRENT_MEM

    def __repr__(self):
        return f"current mem addres"

class Math_operator_Token(Token):
    def __init__(self, value, line):
        super(Math_operator_Token, self).__init__("Operator", value, line)
        self.type = value

    def __repr__(self):
        return f"Operator: {self.value}"

class ComaToken(Token):
    def __init__(self, line):
        super(ComaToken, self).__init__(TT_COMA, '', line)

    def __repr__(self):
        return f"Coma"

class CharToken(Token):
    def __init__(self, value):
        super(CharToken, self).__init__(TT_CHAR, ord(value))

    def __repr__(self):
        return f"{TT_CHAR}: {chr(self.value)}"