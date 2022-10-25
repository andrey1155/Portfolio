from ASM_compiler.lexer.tokens import *
from ASM_compiler.VMres.globals import regs
from ASM_compiler.VMres.instructions_list import *
from ASM_compiler.parser_.ASTNodes import *
from ASM_compiler.VMres.codgen_exceptions import *

OPS = {I_CMP:0, I_BCMP:1, I_BINV:2}


def compile_LOGIC(instruction):
    instr = 0
    instr |= (13 << 12)
    instr |= OPS[instruction.instr] << 10

    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 6)
    else:
        raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[0]}", instruction.line)

    if len(instruction.args) == 1:
        return [instr]

    if isinstance(instruction.args[1], RegisterNode):
        instr = instr | (regs[instruction.args[1].value] << 0)
    elif isinstance(instruction.args[1], NumberNode):
        instr |= (instruction.args[1].tok.value&0x3F << 0)
        instr |= 1 << 9
    else:
        raise CodeGenError(f"Illegal {instruction.instr} operand: {instruction.args[1]}", instruction.line)

    return [instr]
