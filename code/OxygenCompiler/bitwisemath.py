from ASM_compiler.lexer.tokens import *
from ASM_compiler.VMres.globals import regs
from ASM_compiler.parser_.ASTNodes import *

AND_OR = []
NOT_XOR = []
I_SHIFT = "SHIFT"


def compile_math(compiler):
    instr = 0
    instr |= 3 << 12
    instr |= (instructs[compiler.current_token.value] << 6)

    i = compiler.current_token.value


    if i in unary:pass
    else:
        compiler.advance()
        if compiler.current_token.ttype == TT_SPEC_WORD and compiler.current_token.value in regs:
            instr = instr | (regs[compiler.current_token.value] << 3)
        else:
            raise Exception(f"Illegal {i} operand: {compiler.current_token.value}")

    compiler.advance()

    if compiler.current_token.ttype == TT_SPEC_WORD and compiler.current_token.value in regs:
        instr = instr | (regs[compiler.current_token.value] << 0)
    else:
        raise Exception(f"Illegal {i} operand: {compiler.current_token.value}")

    return instr






def compile_shift(instruction):
    instr = 0
    instr = instr | (5 << 12)
    instr |= 0 << 11



    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[compiler.current_token.value] << 8)
        instr = instr | (regs[compiler.current_token.value] << 0)
    else:
        raise Exception(f"Illegal shift operand: {compiler.current_token.value}")

    compiler.advance()

    if compiler.current_token.ttype == TT_DIRECTION:
        if compiler.current_token.value == '<':
            instr |= 1 << 3
        else:
            instr |= 0 << 3
    else:
        raise Exception(f"Illegal shift operand: {compiler.current_token.value}")

    compiler.advance()

    if compiler.current_token.ttype == TT_NUM:
        if compiler.current_token.ttype != "float":
            instr |= (compiler.current_token.value << 4)
        raise Exception(f"Illegal shift operand: {compiler.current_token.value}")
    else:
        raise Exception(f"Illegal shift operand: {compiler.current_token.value}")

    return instr