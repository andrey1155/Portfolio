from ASM_compiler.lexer.tokens import *
from ASM_compiler.custom_output import print_to_buff
import string

letters = string.ascii_letters + '_' + '.'
digits = "0123456789"


class InvalidSymbolError:
    def __init__(self, symbol, line):
        self.base = "Invalid symbol error: "
        self.symbol = symbol
        self.line = line

    def __repr__(self):
        return f"{self.base} '{self.symbol}' in line {self.line}"

    def get_err_repr(self):
        err = self.__repr__() + '\n'
        lin = str(self.line)

        return err + lin + "\nfile"

    @staticmethod
    def form_errors_array(errors_array):
        ret = []
        l = len(errors_array)

        for err in errors_array:
            ret += [err.get_err_repr()]

        return ret, l


class Lexer:

    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.code += ' '
        self.tokens = []
        self.current_line = 1

    def lex(self):

        while self.pos < len(self.code):
            let = self.code[self.pos]

            if let == ' ':
                self.pos += 1
                continue
            elif let == '\n':
                self.tokens.append(EOSToken(self.current_line))
                self.current_line += 1
            elif let in letters:
                self.tokens.append(self.compose_a_word())
            elif let in digits:
                self.tokens.append(self.compose_a_num())
            elif let == '"':
                self.tokens.append(self.compose_a_string())
            elif let in "><":
                self.tokens.append(DirectionToken(let,self.current_line))
            elif let == ':':
                self.tokens.append(DDOTToken())
            elif let == '@':
                self.tokens.append(self.compose_a_directive())
            elif let == '$':
                self.tokens.append(CURRENT_MEM_Token(self.current_line))
            elif let == ',':
                self.tokens.append(ComaToken(self.current_line))
            elif let in math_ops:
                self.tokens.append(Math_operator_Token(let, self.current_line))
            elif let == "'":
                self.tokens.append(self.compose_char())
            elif let == '#':
                while let != '\n':
                    self.pos += 1
                    let = self.code[self.pos]
                self.tokens.append(EOSToken(self.current_line))

            else:
                globals.LEX_ERRORS.append(InvalidSymbolError(let, self.current_line))
                while let != '\n':
                    self.pos += 1
                    let = self.code[self.pos]

            self.pos += 1
        self.tokens.append(EOSToken(self.current_line))
        self.tokens.append(EOFToken())



        return self.tokens


    def compose_a_word(self):
        let = self.code[self.pos]
        word = ""
        while let in digits + letters and self.pos < len(self.code):
            word += let
            self.pos += 1
            let = self.code[self.pos]
        self.pos -= 1
        if word in instructions:
            return InstrToken(word, self.current_line)
        if word in regs:
            return RegisterToken(word, self.current_line)
        if word in spec_words:
            return SpecWordToken(word, self.current_line)
        return WordToken(word, self.current_line)


    def compose_a_directive(self):
        self.pos += 1
        let = self.code[self.pos]
        word = ""
        while let in digits + letters and self.pos < len(self.code):
            word += let
            self.pos += 1
            let = self.code[self.pos]
        self.pos -= 1

        if word in directives:
            return DirectiveToken(word, self.current_line)
        else:
            globals.LEX_ERRORS.append(SyntaxError("Illegal directive error:", word))



    def compose_a_num(self):
        dot_count = 0
        is_hex = False
        sign = 1
        if self.code[self.pos] == '-':
            sign = -1
            self.pos += 1

        if self.code[self.pos] == '0' and self.code[self.pos+1] == 'X':
            is_hex = True
            self.pos += 2

        let = self.code[self.pos]
        word = ""

        while let in digits + "." + "ABCDEF" and self.pos < len(self.code):

            if let == '.':
                dot_count += 1

            word+=(let)
            self.pos += 1
            let = self.code[self.pos]

        self.pos -= 1


        if is_hex:
            ret = sign*int("0x"+word, 16)
        elif dot_count == 1:
            ret = sign*float(word)
        else: ret = sign*int(word)



        if ret > pow(2, 16)/2 - 1:
            return NumberToken(ret, "uint")
        if dot_count == 1:
            return NumberToken(ret, "float")



        return NumberToken(ret, "int")


    def compose_a_string(self):
        self.pos += 1
        let = self.code[self.pos]
        word = ""
        while let != '"':
            word += (let)
            self.pos += 1
            let = self.code[self.pos]

        return StringToken(word, self.current_line)


    def compose_char(self):
        self.pos += 1
        let = self.code[self.pos]
        self.pos += 1

        if self.code[self.pos] != "'":
            print_to_buff(f"let {let}")
            let += self.code[self.pos].lower()


        print_to_buff(f"let {let}")
        return NumberToken(ord(let), self.current_line)
