class NumberNode:

    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f"{self.tok}"

class BinOpNode:

    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.op_tok = op_tok

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"


class UnaryOpNode:

    def __init__(self, op_tok, node):

        self.node = node
        self.op_tok = op_tok

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"


class AddressNode:
    def __repr__(self):
        return "Current address node"


class MainNode:
    def __init__(self):
        self.code = []

class FunctionNode:
    def __init__(self):
        self.code = []

class RegisterNode:
    def __init__(self, reg):
        self.value = reg

    def __repr__(self):
        return f"{self.value}"




class DirectionNode:
    def __init__(self, value):
            self.value = value

    def __repr__(self):
            return f"{self.value}"

class VariableNode:
    def __init__(self, name, value):
            self.value = value
            self.name = name

class BlankNode:
    def __init__(self, name, value):
            self.value = value
            self.name = name