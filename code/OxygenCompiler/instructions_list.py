
##MATH INSTRUCTIONS

I_ADD = "ADD"
I_SUB = "SUB"
I_MUL = "MUL"
I_DIV = "DIV"


I_UDIV = "UDIV"

I_FADD = "FADD"
I_FSUB = "FSUB"
I_FMUL = "FMUL"
I_FDIV = "FDIV"

I_EXP = "EXP"
I_SQRT = "SQRT"
I_LN = "LN"

I_AND = "AND"
I_OR = "OR"
I_NOT = "NOT"
I_XOR = "XOR"

I_SHIFT = "SHIFT"


MATH = [I_ADD,I_SUB,I_MUL,I_DIV,I_UDIV,I_FADD,I_FSUB,I_FMUL,I_FDIV,I_EXP,I_SQRT,I_LN,I_AND,I_OR,I_NOT,I_XOR,I_SHIFT]




##MEM CINTROLL INSTRUCTIONS

I_LOAD = "LD"
I_LOADB = "LDB"
I_LOADBI = "LDBI"

I_STORE = "ST"
I_STOREB = "STB"
I_STOREBI = "STBI"

I_MOV = "MOV"

LOAD = [I_LOAD, I_LOADB, I_LOADBI]
STORE = [I_STORE, I_STOREB, I_STOREBI]



##TRAPS


I_INC = "INC"
I_DEC = "DEC"
I_INV = "INV"

I_PUTI = "PUTI"
I_PUTUI = "PUTUI"
I_PUTF = "PUTF"
I_PUTC = "PUTC"
I_GETC = "GETC"

I_PUSH = "PUSH"
I_POP = "POP"

I_HALT = "HALT"
I_RET = "RET"
I_CLS = "CLS"


##CONTROLL FLOW INSTRUCTIONS

I_BR = "BR"
I_BRE = "BRE"
I_BRL = "BRL"
I_BRG = "BRG"
I_BRLE = "BRLE"
I_BRGE = "BRGE"
I_BRNE = "BRNE"

I_JSR = "JSR"

BR = [I_BR,I_BRE,I_BRL,I_BRG,I_BRLE,I_BRGE,I_BRNE]



##BOOLEAN

I_CMP = "CMP"
I_BCMP = "BCMP"
I_BINV = "BINV"

##DRIVE

I_PLD = "PLD"
I_PST = "PST"

I_DLD = "DLD"
I_DST = "DST"

DRIVE = [I_PLD,I_PST,I_DLD,I_DST]

##INTERRUPT

I_INT = ["INT"]
