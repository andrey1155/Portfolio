from ASM_compiler.lexer.lexer import Lexer
from ASM_compiler.lexer.lexer import InvalidSymbolError
from ASM_compiler.parser_.Parser import Parser
from ASM_compiler.codegen.fileIO import *
from ASM_compiler.VMres.globals import LEX_ERRORS
from ASM_compiler.codegen.CodeGenerator import Compilier
import ASM_compiler.VMres.context as context
from ASM_compiler.custom_output import *
from ASM_compiler.VMres.codgen_exceptions import *
import sys
from ASM_compiler.exceptions import *
import struct

#Console arguments setup
file = sys.argv[1]
out = sys.argv[2]

if len(sys.argv) >= 4:
    if sys.argv[3] == "-c":
        context.IS_CONSOLE = True
    elif sys.argv[3] == "-e":
        context.IS_CONSOLE = False
    else:
        raise Exception("Unknown argument")

if len(sys.argv) >= 5:
    if sys.argv[4] == "-d":
        context.IS_DEBUG = True
    elif sys.argv[4] == "-r":
        context.IS_DEBUG = False
    else:
        raise Exception("Unknown argument")

#Read code
code = read_file(file)
code = to_upper(code)

#Lex
lexer = Lexer(code)
res = lexer.lex()

if len(LEX_ERRORS) != 0:
    print_to_buff(LEX_ERRORS)
else:
    print_to_buff("Lexical analysis: sucscess")

#Parce
parser = Parser(res, [file])
parse_result, errors = parser.parse()

if len(errors) != 0:
    print_to_buff("syntax errors:")
    for e in errors:
        print_to_buff(e.message)
else:
    print_to_buff("Semantic  analysis: sucscess")

lm = parser.label_manager
mm = parser.macro_manager
vm = parser.var_manager


if context.IS_DEBUG == True:
    print_to_buff("\n")
    print_to_buff("Labels:")
    lm.print_L()
    print_to_buff("\n")

#Codegen
codeGenerator = Compilier(parse_result,lm,vm.pack_vars())
code = codeGenerator.compile_code()

print_to_buff("code generation: sucscess")

if context.IS_DEBUG == True:
    print_to_buff(code)

write_file(out, code)

if context.IS_CONSOLE:
    print_buff()
else:
    message_lex, length0 = InvalidSymbolError.form_errors_array(LEX_ERRORS)
    message_syntax, length1 = InvalidSyntaxError.form_errors_array(errors)
    message_codegen, length2 = CodeGenError.form_errors_array(codeGenerator.errors)

    message = [f"{length0+length1+length2}"] + message_lex + message_syntax + message_codegen

    for e in message:
        print(e)



