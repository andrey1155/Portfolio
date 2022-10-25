from ASM_compiler.parser_.instruction_node import InstructionNode
from ASM_compiler.parser_.instruction_node import CoedeBlockNode
from ASM_compiler.parser_.labels_manager import LabelManager
from ASM_compiler.parser_.macro_manager import *
from ASM_compiler.parser_.macro_node import *
from ASM_compiler.parser_.var_list import *
from ASM_compiler.lexer.lexer import Lexer
from ASM_compiler.codegen.fileIO import *
from ASM_compiler.exceptions import *
from ASM_compiler.VMres.context import RESERVED_SPACE
from ASM_compiler.custom_output import print_to_buff

class ParseResult:

    def __init__(self):
        self.error = None
        self.node = None


    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


class Parser:

    def __init__(self, tokens, included_files = []):

        self.label_manager = LabelManager()
        self.macro_manager = MacroManager(self.label_manager)
        self.var_manager   = VarManager(RESERVED_SPACE, self.label_manager)
        self.def_dict = {}

        self.included_code = []

        self.tokens = tokens
        self.pos = -1
        self.current_tok = None
        self.advance()

        self.errors = []
        self.critical_error = False

        self.included_files = included_files

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]

        return self.current_tok

    def parse(self):

        try:
            self.pre_parse()
        except InvalidSyntaxError as err:
            self.errors.append(err)
            self.scroll_to_next_inst()

        try:
            self.vars()
        except InvalidSyntaxError as err:
            self.errors.append(err)
            self.scroll_to_next_inst()



        for v in self.var_manager.vars_address:
            self.label_manager.add_address(v, self.var_manager.vars_address[v])

        res = self.code_block()

        if self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.line, "unknown error"))

        return res, self.errors


    #eok
    def code_block(self):
        errors = []
        instructs = []
        instructs += self.included_code

        if self.current_tok.value == SW_CODE:
            self.advance()
        else:
            self.get_next_sector()
            if self.current_tok.value != SW_CODE:
                raise InvalidSyntaxError(E_NO_CODE_SECTOR,-1)

        while self.current_tok.type != TT_EOF:

            if self.current_tok.type == TT_EOS:
                self.advance()
                continue

            try:
                if self.current_tok.type == TT_DIRECTIVE:
                    self.directive()
                elif self.current_tok.type == TT_WORD and self.current_tok.value in self.macro_manager.macro_dict:
                    t = self.instr()
                    self.label_manager.set_label(t)
                    instructs += t
                elif self.current_tok.type == TT_WORD and not self.current_tok.value in self.macro_manager.macro_dict:
                    raise InvalidSyntaxError(f'unknown macro "{self.current_tok.value}" in line ', self.current_tok.line)
                elif self.current_tok.type == TT_INSTR:
                    t = self.instr()
                    self.label_manager.set_label(t)
                    instructs.append(t)
                else:
                    raise InvalidSyntaxError(E_UNEXPECTED_EXP, self.get_line())

            except InvalidSyntaxError as err:
                errors.append(err)
                self.scroll_to_next_inst()

        self.errors += errors
        return CoedeBlockNode(instructs, self.label_manager, self.var_manager.current_address)

    #eok
    def vars(self):

        if self.current_tok.value == SW_DATA:
            self.advance()
            self.advance()
        else:
            self.get_next_sector()
            if self.current_tok.type == TT_EOF:
                raise InvalidSyntaxError(E_NO_SECTORS, -1)
            else:
                if self.current_tok.value == SW_DEF:
                    raise InvalidSyntaxError(E_DEF_NOT_IN_PLACE, self.get_line())
                elif self.current_tok.value == SW_CODE:
                    return


        while not (self.current_tok.value == SW_CODE or self.current_tok.type == TT_EOF):

            if self.current_tok.type == TT_EOS:
                self.advance()
                continue

            try:
                line = self.get_line()
                if self.matches(TT_SPEC_WORD, [SW_VAR,SW_STRING]):

                    new_var = self.get_var()
                    self.var_manager.add_var(new_var)
                elif self.matches(TT_DIRECTIVE, D_LABEL):
                    self.advance()
                    if self.current_tok.type == TT_WORD:
                        self.label_manager.add_address(self.current_tok.value, self.var_manager.current_address)
                        self.advance()
                else:
                    raise InvalidSyntaxError(E_UNEXPECTED_EXP, line, E_UNEXPECTED_EXP_DATA_EXTRA)
            except InvalidSyntaxError as err:
                self.errors.append(err)
                self.scroll_to_next_inst()

        pass

    #eok
    def get_var(self):

        line = self.get_line()
        name = ""
        val = None

        self.advance()

        if self.current_tok.type == TT_WORD:
            name = self.current_tok.value
        else:
            raise InvalidSyntaxError(E_WORD,line)
        self.advance()

        if self.current_tok.type in [TT_STRING, TT_CHAR]:
            val = self.current_tok
            self.advance()
        else: val = self.math_expr()

        if self.current_tok.type != TT_EOS:
            raise InvalidSyntaxError(E_INVALID_DATA_EXPR, line)
        self.advance()

        return VariableNode(name,val)


    #eok
    def instr(self):
        instr = self.current_tok.value
        line = self.current_tok.line

        #ok
        if instr == I_SHIFT:
            return self.shift()
        if instr in self.macro_manager.macro_dict:
            return self.inv_macro()

        args = []

        self.advance()

        #ok
        if self.current_tok.type == TT_EOS:
            self.advance()
            return InstructionNode(instr, line)


        while self.current_tok.type != TT_EOS:


            if self.current_tok.type == TT_REG:
                args.append(RegisterNode(self.current_tok.value))
                self.advance()
            elif self.current_tok.type == TT_COMA:
                raise InvalidSyntaxError(E_REG,self.current_tok.line)
            else:
                args.append(self.math_expr())

            if self.current_tok.type == TT_COMA:
                self.advance()
                if self.current_tok.type == TT_EOS: raise InvalidSyntaxError(E_ARG, line)
            elif self.current_tok.type == TT_EOS:
                self.advance()
                return InstructionNode(instr, line, args)

            else:
                raise InvalidSyntaxError(E_COMA,line)
    #eok
    def shift(self):

        instr = self.current_tok.value
        line = self.current_tok.line

        args = []
        self.advance()

        if self.current_tok.type == TT_REG:
            args.append(RegisterNode(self.current_tok.value))
            self.advance()
        else: raise InvalidSyntaxError(E_REG, line)

        if self.current_tok.type == TT_DIRECTION:
            args.append(DirectionNode(self.current_tok.value))
            self.advance()
        else: raise InvalidSyntaxError(E_DIRECTION, line)

        if not self.current_tok.type in [TT_NUM, TT_PLUS, TT_MINUS, TT_LPAREN, TT_CURRENT_MEM, TT_WORD]:
            raise InvalidSyntaxError(E_MATH_EXPR, line)

        args.append(self.math_expr())

        self.advance()
        return InstructionNode(instr,line, args)
    #eok
    def inv_macro(self):
        instr = self.current_tok.value
        line = self.current_tok.line
        args = []

        self.advance()

        if self.current_tok.type == TT_EOS:
            self.advance()
            return self.macro_manager.invoke(instr,[],line)

        while self.current_tok.type != TT_EOS:
            if self.current_tok.type == TT_REG:
                args.append(RegisterNode(self.current_tok.value))
                self.advance()
            elif self.current_tok.type == TT_DIRECTION:
                args.append(DirectionNode(self.current_tok.value))
                self.advance()
            elif self.current_tok.type == TT_COMA:
                raise InvalidSyntaxError(E_REG, self.current_tok.line)
            else:
                args.append(self.math_expr())

            if self.current_tok.type == TT_COMA:
                self.advance()
                if self.current_tok.type == TT_EOS: raise InvalidSyntaxError(E_ARG,line)
            elif self.current_tok.type == TT_EOS:
                self.advance()
                return self.macro_manager.invoke(instr,args,line)
            else:
                raise InvalidSyntaxError(E_COMA,line)

    #eok
    def directive(self):
        line = self.current_tok.line
        if self.current_tok.type == TT_DIRECTIVE:
            if self.current_tok.value == D_LABEL:
                self.advance()
                if self.current_tok.type == TT_WORD:
                    self.label_manager.add_label(self.current_tok.value)
                    self.advance()
                else: raise InvalidSyntaxError(E_WORD,line)
            elif self.current_tok.value == D_MACRO:
                self.advance()
                if self.current_tok.type == TT_WORD:
                    self.macro_manager.add_macro(self.macro())
                else: raise InvalidSyntaxError(E_WORD, line)
            elif self.current_tok.value == D_ENTRY:

                self.advance()
                self.label_manager.add_label("ENTRY")
            else:
                self.advance()
                raise InvalidSyntaxError(E_UNEXPECTED_DIRECTIVE, line)

    #eok
    def macro(self):
        instructs = []

        name, args = self.get_macro_args()
        local_lm = MacroLabelManager(name)
        inst_count = 0

        cuonter = 0
        while self.current_tok.value != D_ENDMACRO:
            cuonter += 1
            if cuonter >= 10000 or self.current_tok.type == TT_EOF:
                raise InvalidSyntaxError(E_NO_ENDMACRO)

            if self.current_tok.type == TT_EOS:
                self.advance()
                continue

            line = self.current_tok.line
            if self.current_tok.type == TT_INSTR:
                t = self.instr()
                instructs.append(t)
                inst_count += 1
            elif self.current_tok.type == TT_DIRECTIVE:
                if self.current_tok.value == D_LABEL:
                    self.advance()
                    if self.current_tok.type == TT_WORD:
                        local_lm.add_label(self.current_tok.value,inst_count)
                        self.advance()
                    else: raise InvalidSyntaxError(E_WORD, line)
            else: raise InvalidSyntaxError(E_UNEXPECTED_DIRECTIVE, line)
        self.advance()
        return MacroNode(name,args,instructs,local_lm)
    #eok
    def get_macro_args(self):

        line = self.get_line()
        name = ""
        args = []

        if self.current_tok.type == TT_WORD:
            name = self.current_tok.value
            self.advance()
        else: raise InvalidSyntaxError(E_WORD, line)

        while self.current_tok.type != TT_EOS:

            if self.current_tok.type == TT_WORD:
                args.append(self.current_tok.value)
                self.advance()
            elif self.current_tok.type == TT_COMA:
                raise InvalidSyntaxError(E_WORD, line)

            if self.current_tok.type == TT_COMA:
                self.advance()
            elif self.current_tok.type == TT_EOS:
                self.advance()

                return name,args
            else:
                raise InvalidSyntaxError(E_COMA, line)

        return name,[]

    #eok
    def parse_include(self, name):

        if name in self.included_files:
            raise InvalidSyntaxError(f" '{name}' is alredy defined")

        code = read_file(name)
        code = to_upper(code)

        lexer = Lexer(code)
        res = lexer.lex()

        parser = Parser(res, self.included_files + [name])
        parse_result, err = parser.parse()

        self.errors += err

        lm = parser.label_manager
        mm = parser.macro_manager
        vm = parser.var_manager
        dl = parser.def_dict

        self.def_dict.update(dl)
        self.macro_manager.update(mm)

        self.label_manager.update(lm)
        self.included_code += parse_result.instructs

        self.var_manager.update(vm)
    #eok
    def pre_parse(self):

        self.get_next_sector()

        if self.current_tok.value == SW_DEF:
            self.advance()
        else:
            if self.current_tok.type == TT_EOF:
                raise InvalidSyntaxError(E_NO_SECTORS, -1)
            else:
                return

        while not self.is_sector_marker(self.current_tok):

            if self.current_tok.type == TT_EOS:
                self.advance()
                continue

            line = self.get_line()
            try:
                if self.current_tok.type == TT_DIRECTIVE:
                    if self.current_tok.value == D_DEFINE:
                        self.advance()
                        a1,a2 = self.get_definition()
                        self.def_dict.update({a1:a2})
                    elif self.current_tok.value == D_INCLUDE:
                        self.advance()
                        self.parse_include(self.current_tok.value)
                        self.advance()
                    else:
                        raise InvalidSyntaxError(E_UNEXPECTED_DIRECTIVE,line, E_UNEXPECTED_TOKEN_PREPARSE_EXTRA)
                else:
                    raise Exception(self.current_tok)
                    raise InvalidSyntaxError(E_UNEXPECTED_TOKEN_PREPARSE, line, E_UNEXPECTED_TOKEN_PREPARSE_EXTRA)
            except InvalidSyntaxError as err:
                self.errors.append(err)
                self.scroll_to_next_inst()



        self.aply_definition()

    #eok
    def get_definition(self):
        line = self.get_line()

        if self.current_tok.type == TT_WORD:
            a1 = self.current_tok.value
        else: raise InvalidSyntaxError(E_WORD, line)

        self.advance()

        if self.current_tok.type == TT_EOS:
            raise InvalidSyntaxError(" a word expected in line ",line)

        a2 = self.current_tok

        self.advance()

        if self.current_tok.type != TT_EOS:
            raise InvalidSyntaxError(" invalid definition in line ", line)

        return a1, a2

    def aply_definition(self):


        for i in range(len(self.tokens)):
            if self.tokens[i].type == TT_WORD:
                if self.tokens[i].value in self.def_dict:
                    self.tokens[i] = self.def_dict[self.tokens[i].value]



    #eok
    def atom(self):
        t = self.current_tok

        if t.type == TT_CURRENT_MEM:
            self.advance()
            return AddressNode()

        if t.type == TT_NUM:
            self.advance()
            return NumberNode(t)

        elif t.type == TT_WORD:
            self.advance()
            return t

        elif t.type == TT_LPAREN:
            self.advance()
            in_paren = self.math_expr()

            if self.current_tok.type == TT_RPAREN:
                self.advance()
                return in_paren
            else:
                raise InvalidSyntaxError(E_PAREN,self.current_tok.line)

        raise InvalidSyntaxError(E_ATOM,self.current_tok.line)

    def factor(self):
        return self.un_op((TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def math_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):

        left = func()

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()

            left = BinOpNode(left, op_tok, right)
        return left

    def un_op(self, ops):
        operator = None
        node = None



        if self.current_tok.type in ops:
            operator = self.current_tok
            self.advance()

            node = self.atom()
            node = UnaryOpNode(operator, node)

            return node

        else: return self.atom()




    def matches(self,tt,val):
        if self.current_tok.type in tt:
            if self.current_tok.value in val:
                return True

        return False

    def scroll_to_next_inst(self):

        l = self.get_line()

        while self.get_line() == l:
            self.advance()
        return


    def get_line(self):
        return self.current_tok.line

    def get_next_sector(self):

        while not (self.is_sector_marker(self.current_tok) or self.current_tok.type == TT_EOF):
            self.advance()

    def is_sector_marker(self, token):
        if token.value in [SW_DEF,SW_DATA,SW_CODE]:
            return True
        return False