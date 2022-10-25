from ASM_compiler.lexer.tokens import *
from ASM_compiler.VMres.globals import regs
from ASM_compiler.parser_.ASTNodes import *

BR_OP = 8
BRJ_OP = 9
JSR_OP = 10


BR_COND = {I_BR: 0b111,
I_BRE: 0b010,
I_BRL: 0b100,
I_BRG: 0b001,
I_BRLE: 0b110,
I_BRGE: 0b011,
I_BRNE: 0b101}



def compile_BR_BRJ(instuction,lm):

    if isinstance(instuction.args[0],WordToken):
        return compile_BR(instuction,lm)

    if isinstance(instuction.args[0], RegisterNode):
        return compile_BRJ(instuction,lm)



def compile_BR(instruction,lm):

    instr = 0
    instr |= (BR_OP << 12)
    instr |= BR_COND[instruction.instr] << 9

    target_address = lm.get_label_address(instruction.args[0].value)

    dpc = -(instruction.address) + target_address
    if dpc < 0:
        instr |= 0 << 8
    else:
        instr |= 1 << 8
    instr |= (abs(dpc) & 0xFF)
    if abs(dpc) > 0xFF: raise Exception("Offset exceeds max possible value")
    return [instr]



def compile_BRJ(instruction,lm):

    instr = 0

    instr = 0
    instr |= (BRJ_OP << 12)
    instr |= BR_COND[instruction.instr] << 9
    instr |= (regs[instruction.args[0].value] << 6)

    if len(instruction.args)==2 and isinstance(instruction.args[1], NumberNode):
        instr |= instruction.args[1].tok.value

    return [instr]

def compile_JSR(instruction,lm):

    instr = 0

    instr = 0
    instr |= (JSR_OP << 12)
    instr |= (regs[instruction.args[0].value] << 9)

    if len(instruction.args)==2 and isinstance(instruction.args[1], NumberNode):
        instr |= instruction.args[1].tok.value

    return [instr]