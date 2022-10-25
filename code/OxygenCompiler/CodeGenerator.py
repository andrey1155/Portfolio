from ASM_compiler.codegen._math import compile
from ASM_compiler.codegen.traps import *
from ASM_compiler.codegen.mem import *
from ASM_compiler.codegen.controll_flow import *
from ASM_compiler.codegen.logic import *
from ASM_compiler.VMres.context import *
from ASM_compiler.VMres.codgen_exceptions import *
import sys
import ASM_compiler.VMres.context as context

class Compilier:

    def __init__(self, code, lm, var_list):
        self.code = code.instructs

        self.data_section = []
        self.mashinecode = []
        self.vars = var_list

        self.code_start = 0
        self.current_address = 0

        self.lm = lm
        self.errors = []

    def advance(self, d=1):
        try:
            self.pos += d
            self.current_instr = self.code[self.pos]
        except BaseException as e:
            raise Exception(len(self.code))


    def compile_code(self):

        self.mashinecode = [0 for i in range(0,RESERVED_SPACE)]

        try:
            self.mashinecode[0] = self.lm.get_label_address("ENTRY")
        except CodeGenError as err:
            self.errors.append(CodeGenError("no 'ENTRY' label found"))

        self.mashinecode += self.vars

        for current_instr in self.code:

            try:
                if context.IS_DEBUG == True:
                    print_to_buff(current_instr)
                if current_instr.instr in TRAP:
                    self.mashinecode += compile_trap(current_instr)

                elif current_instr.instr == I_MOV:
                    self.mashinecode += compile_mov(current_instr,self.lm)
                elif current_instr.instr in LOAD:
                    self.mashinecode += compile_load(current_instr, self.lm)
                elif current_instr.instr in STORE:
                    self.mashinecode += compile_store(current_instr, self.lm)

                elif current_instr.instr in MATH:
                    self.mashinecode += compile(current_instr)

                elif current_instr.instr in BR:
                    self.mashinecode += compile_BR_BRJ(current_instr,self.lm)
                elif current_instr.instr == I_JSR:
                    self.mashinecode += compile_JSR(current_instr,self.lm)

                elif current_instr.instr in [I_CMP,I_BCMP,I_BINV]:
                    self.mashinecode += compile_LOGIC(current_instr)
                elif current_instr.instr in DRIVE:
                    self.mashinecode += compile_drive(current_instr)
            except CodeGenError as err:
                self.errors.append(err)




        return self.mashinecode





