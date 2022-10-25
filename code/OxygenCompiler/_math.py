from ASM_compiler.lexer.tokens import *
from ASM_compiler.VMres.globals import *
from ASM_compiler.VMres.instructions_list import *
from ASM_compiler.parser_.ASTNodes import *
from ASM_compiler.VMres.codgen_exceptions import *

AND_OR_OP = 3           ;       AND_OR   = [I_AND,I_OR]
NOT_XOR_OP = 4          ;       NOT_XOR  = [I_NOT,I_XOR]
MATH_AND_SHIFT_OP = 5   ;       MATH     = [I_ADD,I_SUB,I_DIV,I_MUL]
DIV_UDIV_OP = 6         ;       DIV_UDIV = [I_DIV,I_UDIV]
FMATH_OP = 7            ;       FMATH2   = [I_FADD,I_FSUB,I_FMUL,I_FDIV]   ;   FMATH1    = [I_EXP,I_SQRT,I_LN]

instructs = {
    I_ADD: 0,
    I_SUB: 1,
    I_MUL: 2,
    I_SHIFT: 3,

    I_DIV: 0,
    I_UDIV: 1,

    I_FADD: 0,
    I_FSUB: 1,
    I_FMUL: 2,
    I_FDIV: 3,

    I_EXP: 4,
    I_SQRT:5,
    I_LN:  6,

    I_AND: 0,
    I_OR:  1,

    I_NOT: 0,
    I_XOR: 1
             }

unary = [
    I_EXP,
    I_SQRT,
    I_LN,
    I_NOT
]


def compile(instruction):

    if instruction.instr in AND_OR:
        return [compile_and_or_not_xor_div_udiv(instruction,AND_OR_OP)]
    if instruction.instr in NOT_XOR:
        return [compile_and_or_not_xor_div_udiv(instruction,NOT_XOR_OP)]
    if instruction.instr in MATH:
        return [compile_math(instruction)]
    if instruction.instr in DIV_UDIV:
        return [compile_and_or_not_xor_div_udiv(instruction,DIV_UDIV_OP)]
    if instruction.instr in FMATH2:
        return [compile_float_dual(instruction)]
    if instruction.instr in FMATH1:
        return [compile_float_unary(instruction)]
    if instruction.instr == I_SHIFT:
        return [compile_shift(instruction)]



def compile_float_dual(instruction):
    instr = 0
    instr |= (FMATH_OP << 12)
    instr |= instructs[instruction.instr] << 6


    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 3)
    else: raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[0]}", instruction.line)

    if isinstance(instruction.args[1], RegisterNode):
        instr = instr | (regs[instruction.args[1].value] << 0)
    else:
        raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[1]}", instruction.line)

    return instr

def compile_float_unary(instruction):
    instr = 0
    instr |= (FMATH_OP << 12)
    instr |= instructs[instruction.instr] << 6

    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 3)
    else: raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[0]}", instruction.line)

    return instr

def compile_and_or_not_xor_div_udiv(instruction,op):
    instr = 0
    instr |= (op << 12)
    instr |= instructs[instruction.instr] << 11

    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 7)
    else:
        raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[0]}", instruction.line)

    if isinstance(instruction.args[1], RegisterNode):
        instr = instr | (regs[instruction.args[1].value] << 0)
    elif isinstance(instruction.args[1], NumberNode):
        instr |= (1 << 10) #imm7 flag
        instr |= (instruction.args[1].tok.value << 0)
    else:
        raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[1]}", instruction.line)

    return instr

def compile_math(instruction):
    instr = 0
    instr |= (MATH_AND_SHIFT_OP << 12)
    instr |= instructs[instruction.instr] << 10

    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 6)
    else:
        raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[0]}", instruction.line)

    if isinstance(instruction.args[1], RegisterNode):
        instr = instr | (regs[instruction.args[1].value] << 0)
    elif isinstance(instruction.args[1], NumberNode):
        instr |= (1 << 9) #imm6 flag
        instr |= (instruction.args[1].tok.value << 0)
    else:
        raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[1]}", instruction.line)

    return instr

def compile_shift(instruction):
    instr = 0
    instr |= (MATH_AND_SHIFT_OP << 12)
    instr |= instructs[instruction.instr] << 10

    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 6)
    else:
        raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[0]}", instruction.line)


    if isinstance(instruction.args[1], DirectionNode):
        if instruction.args[1].value == '<':
            instr |= (1 << 9) #direction flag
        else:
            instr |= (0 << 9) #direction flag
    else:
        raise CodeGenError(f"Illegal shift operand: {instruction.args[1]}", instruction.line)


    if isinstance(instruction.args[2], NumberNode):
        if instruction.args[2].tok.ntype != "float":
            instr |= (instruction.args[2].tok.value << 0)
        else: raise CodeGenError(f"Illegal shift operand: {instruction.args[2]}", instruction.line)
    else:
        raise CodeGenError(f"Illegal shift operand: {instruction.args[2]}", instruction.line)

    return instr