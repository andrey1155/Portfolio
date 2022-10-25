from ASM_compiler.parser_.instruction_node import *
from ASM_compiler.VMres.codgen_exceptions import *


class LabelManager:

    def __init__(self):
        self.labels = {}
        self.current_labels = []

    def get_label_address(self, var_name):

        if var_name not in self.labels:
            raise CodeGenError(E_UNKNOWN_LABEL+var_name)

        if type(self.labels[var_name]) == int:
            return self.labels[var_name]

        return self.labels[var_name].address

    def add_label(self, name):
        self.current_labels += [name]

    def update(self, lm):
        self.labels.update(lm.labels)

    def set_label(self, instruction):

        if len(self.current_labels) == 0: return

        if not isinstance(instruction, InstructionNode):

            for name in self.current_labels:
                self.labels.update({name: instruction[0]})
            self.current_labels.clear()
            return

        for name in self.current_labels:
            self.labels.update({name: instruction})

        self.current_labels.clear()

    def add_address(self, name, address):
        self.labels.update({name: address})

    def print_L(self):
        print_to_buff(self.labels)
        return

        for i in self.labels:
            print_to_buff(self.labels[i])

            if type(self.labels[i]) == int:
                print_to_buff(self.labels[i])
                continue

            print_to_buff(i,self.labels[i].address)






