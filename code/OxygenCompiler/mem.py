from ASM_compiler.lexer.tokens import *
from ASM_compiler.VMres.globals import VARS as vars
from ASM_compiler.VMres.globals import regs
from ASM_compiler.parser_.ASTNodes import *
from ASM_compiler.VMres.instructions_list import *
from ASM_compiler.VMres.codgen_exceptions import *

mov_opcode = 2
ld_opcode = 0
st_opcode = 1
pld_pst = 12

def mov_long(compiler, repr16, target):
    "mov target [(rep16 & 0xFF00) >> 8]"
    "shift target < 8"
    "or target [rep16 & 0xFF]"

    data1 = (repr16 & 0xFF00) >> 8
    data2= repr16 & 0xFF


    #instr2 = 0
    #instr2 |= (5 << 12)
    #instr2 |= (3 << 10)
    #instr2 |= (1 << 9)
    #instr2 |= (target << 6)
    #instr2 |= (8 << 0)

    instr1 = 0
    instr1 |= (mov_opcode << 12)
    instr1 |= target << 8
    instr1 |= data1

    instr3 = 0
    instr3 |= 14 << 12
    instr3 |= (target << 8)
    instr3 |= data2

    code  = [instr1,instr3]

    return code


def compile_load(instruction, lm):
    instr = 0

    if instruction.instr == I_LOAD:
        pass
    if instruction.instr == I_LOADB:
        instr |= 2 << 10
    if instruction.instr == I_LOADBI:
        instr |= 3 << 10



    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 7)
    else:
        raise Exception(f"Illegal load target: {instruction.args[0]}")


    if isinstance(instruction.args[1], WordToken):
            instruction.args[1] = NumberNode(NumberToken(lm.get_label_address(instruction.args[1].value),instruction.args[1].line))

    if isinstance(instruction.args[1], RegisterNode):
        instr |= 1 << 10
        instr |= regs[instruction.args[1].value]
    elif isinstance(instruction.args[1], NumberNode):
        if instruction.args[1].tok.ntype != "float" and not instruction.args[1].tok.value < 0 and not instruction.args[1].tok.value > 127:
            instr |= instruction.args[1].tok.value
        else:
            raise CodeGenError(f"Illegal load address: {instruction.args[1].tok.value} in line ", instruction.line)
    return [instr]


def compile_store(instruction,lm):
    instr = 0
    instr |= (st_opcode << 12)


    if instruction.instr == I_STORE:
        pass
    if instruction.instr == I_STOREB:
        instr |= 2 << 10
    if instruction.instr == I_STOREBI:
        instr |= 3 << 10



    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 7)
    else:
        raise Exception(f"Illegal store target: {instruction.args[0]}")

    if isinstance(instruction.args[1], WordToken):
            instruction.args[1] = NumberNode(NumberToken(lm.get_label_address(instruction.args[1].value)))

    if isinstance(instruction.args[1], RegisterNode):
        instr |= 1 << 10
        instr |= regs[instruction.args[1].value]
    elif isinstance(instruction.args[1], NumberNode):
        if instruction.args[1].tok.ntype != "float" and not instruction.args[1].tok.value < 0 and not instruction.args[1].tok.value > 127:
            instr |= instruction.args[1].tok.value
        else:
            raise Exception(f"Illegal store addres: {instruction.args[1].tok.value}")


    elif compiler.current_token.ttype == TT_WORD and compiler.current_token.value in vars:
        instr |= vars[compiler.current_token.value]
    else:
        raise Exception(f"Illegal load addres: {compiler.current_token.value}")

    return [instr]


def compile_mov(instruction, lm):
    instr = 0
    instr = instr | (mov_opcode << 12)

    target = (regs[instruction.args[0].value])

    if len(instruction.args)>1:
        arg2 = instruction.args[1]
    else: arg2 = 0

    if isinstance(instruction.args[0], RegisterNode):
        pass
    else:
        raise Exception(f"Invalid mov target: {instruction.args[0].value}")



    if isinstance(arg2, RegisterNode):
        instr |= 1 << 11
        instr |= regs[arg2.value]
        instr |= target << 4


    if isinstance(arg2, WordToken):
            v = lm.get_label_address(arg2.value)
            instr |= v
            instr |= target << 8

            if (v & 0xFF00) != 0:
               return mov_long(instruction, v, target)


    elif isinstance(arg2, NumberNode):
        if (arg2.tok.repr16 & 0xFF00) != 0 or arg2.tok.ntype == "float":
            return mov_long(instruction, arg2.tok.repr16, target)

        instr |= arg2.tok.value
        instr |= target << 8



    return [instr,0xFFFF]


def compile_drive(instruction):
    instr = 0
    instr |= (pld_pst << 12)


    if instruction.instr in [I_PLD, I_DLD]:
        instr |= 0 << 6
    if instruction.instr in [I_PST, I_DST]:
        instr |= 1 << 6

    if instruction.instr in [I_PST, I_PLD]:
        instr |= 1 << 7
    if instruction.instr in [I_DLD, I_DST]:
        instr |= 0 << 7


    if isinstance(instruction.args[0], RegisterNode):
        instr = instr | (regs[instruction.args[0].value] << 0)
    else:
        raise Exception(f"Illegal store target: {instruction.args[0]}")

    if isinstance(instruction.args[1], RegisterNode):
        instr |= 1 << 10
        instr |= regs[instruction.args[1].value] << 3
    else:
        raise Exception(f"Illegal store addres: {instruction.args[1].tok.value}")


    return [instr]