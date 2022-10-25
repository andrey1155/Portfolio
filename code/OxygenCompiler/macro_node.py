from ASM_compiler.lexer.tokens import WordToken
from ASM_compiler.exceptions import *
from ASM_compiler.custom_output import print_to_buff
import copy


class MacroNode:

    def __init__(self,name,args,code, labels):
        self.code = code
        self.name = name
        self.args = args
        self.local_lm = labels

    def __repr__(self):
        return self.code.__repr__()



    def invoke(self, args, lm, line):
        code =  copy.deepcopy(self.code)
        print_to_buff(self.code)
        if len(args) != len(self.args):
            raise InvalidSyntaxError(f"{self.name} requires {len(self.args)} arguments, but {len(args)} were given in line",line)


        lm.set_label(code[0])

        loop_count = -1

        for arg in self.args:
            loop_count += 1
            for i in range(len(code)):
                if i in self.local_lm.inv_labels:
                    lm.add_label(self.local_lm.get_name(i))
                    lm.set_label(code[i])

                for j in range(len(code[i].args)):
                    if code[i].args[j] == arg:
                        code[i].args[j] = args[loop_count]

                    if isinstance(code[i].args[j], WordToken):
                        if code[i].args[j].value in self.local_lm.labels:
                            if code[i].args[j].value == self.local_lm.inv_labels[self.local_lm.labels[code[i].args[j].value]]:
                                code[i].args[j] = WordToken(self.local_lm.get_name(self.local_lm.labels[code[i].args[j].value]),line)




        self.local_lm.invoke()

        return code





