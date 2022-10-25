import struct
from os import path


def read_file(file_name):

    if path.isfile("ASM_compiler/builtin/"+file_name):
        with open("ASM_compiler/builtin/"+file_name, "r") as file:
            data = file.read()
        return data

    with open(file_name, "r") as file:
        data = file.read()
    return data


def to_upper(string):
    prev_inv = ""
    invert = True
    code = ""
    for let in string:
        if invert:
            a = let.upper()
            code += a
        else:
            code += let

        if not invert and let == prev_inv:
            invert = True

        elif invert and (let == '"' or let == "'"):
            prev_inv = let
            invert = False

        continue
        if let == '"' or let == "'":
            if invert:
                invert = False
            else:
                invert = True
    return code


def write_file(file_name, instructs):
    file = open(file_name, "wb+")

    for i in instructs:
        code = struct.pack('H', i)
        file.write(code)

    file.close()
