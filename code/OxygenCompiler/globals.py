import math
from ASM_compiler.VMres.words_list import *

LABELS = {}
VARS = {}
DEFINES = {}
VARS_ADDRESS = {}
FUNCTIONS_ADDRESS = {}

LEX_ERRORS = []



regs = {    R_0: 0,
    R_1: 1,
    R_2: 2,
    R_3: 3,
    R_4: 4,
    R_BP: 5,
    R_SP: 6,
    R_BUFF: 7,
    R_PC: 8,
    R_COND: 9,
    R_SUB: 10}


def int_to_8bit(num):
    if num >= 0: return num
    t = abs(num)
    t = ~t
    t |= 1 << 7
    t += 1
    return t & 0xFF

def float_to_fnum(f):
    m, exp = math.frexp(f)
    ret = 0

    while abs(m) < 63:
        m *= 2
        exp -= 1

    m = m + 0.5 if m >= 0.0 else m - 0.5
    m = int(m)

    ret |= int_to_8bit(exp)
    ret |= (int_to_8bit(m) << 8)

    return ret