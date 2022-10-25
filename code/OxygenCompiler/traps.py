from ASM_compiler.lexer.tokens import *
from ASM_compiler.VMres.globals import *
from ASM_compiler.parser_.ASTNodes import *
from ASM_compiler.VMres.instructions_list import *
from ASM_compiler.VMres.codgen_exceptions import *

TRAP = [
"PUTI",
"PUTUI",
"PUTF",
"PUTC",
"GETC",
"PUSH",
"POP",
"HALT",
"CLS",
"RET",
I_INC,
I_DEC,
I_INV]

traps = {"PUTC" : 0, "PUTI" : 1, "PUTUI" : 2, "PUTF" : 3,
    "GETC" : 4, "PUSH" : 5, "POP" : 6,
    "CLS" : 7, "HALT" : 8, "RET": 9, "INC":10, "DEC":11, "INV":12}


opcode = 11


def compile_trap(instruction):

    instr = 0
    instr |= opcode << 12

    instr |= traps[instruction.instr] << 0

    if len(instruction.args) > 1:
        raise CodeGenError(f"Too many trap operands")

    if len(instruction.args) == 0:
        return [instr]

    if isinstance(instruction.args[0], RegisterNode):
        instr |= regs[instruction.args[0].value] << 8
    else:
        raise CodeGenError(f"Invalid trap operand: {instruction.args[0]}")

    return [instr]
