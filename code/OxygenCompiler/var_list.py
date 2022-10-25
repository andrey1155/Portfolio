from ASM_compiler.lexer.tokens import *
from ASM_compiler.parser_.ASTNodes import *
from ASM_compiler.codegen.calculator import Calculator
from ASM_compiler.custom_output import *

class VarManager:

    def __init__(self, start_address, lm):
        self.vars = {}  ##name value
        self.vars_address = {} ## name address
        self.current_address = start_address
        self.lm = lm


    def get_var_size(self,var_name):
        return self.var_size[var_name]

    def get_var_address(self, var_name):
        return self.vars_address[var_name]

    def get_var(self, var_name):
        return self.vars[var_name]

    def add_var(self, node):
        self.vars.update({node.name: node.value})
        self.vars_address.update({node.name:self.current_address})

        if not isinstance(node.value,StringToken):
            self.current_address += 1
        else:
            self.current_address += len(node.value.value) + 1 #add NULL in the end

        print_to_buff(f"var added: current_address = {self.current_address}, val = {node.value}")

    def update(self, vm):

        if len(vm.vars) == 0:
            return
        print_to_buff(f"update called: {vm.vars}")
        for v in vm.vars:

            self.add_var(BlankNode(v,vm.vars[v]))








    def pack_vars(self):
        data = []

        for var in self.vars:

            v = self.vars[var]

            if isinstance(v, BinOpNode) or isinstance(v, UnaryOpNode) or isinstance(v, AddressNode) or isinstance(v, NumberNode):
                calculator = Calculator()
                print_to_buff("unfinished var list 59")
                self.vars[var] = NumberToken(calculator.calculate(v,self.lm,self.get_var_address(var)),0)
                v = self.vars[var]

            if v.type == TT_NUM:
                data.append(v.repr16)
            elif v.type == TT_STRING:
                for let in v.value:
                    data.append(ord(let))
                data.append(0)
            else: raise Exception(f"Invalid data token: {var}")

        return data
