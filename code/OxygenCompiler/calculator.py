from ASM_compiler.lexer.tokens import *
from ASM_compiler.exceptions import *


class Calculator:

    def calculate(self, node, lm, current_address = 0):

        self.current_Address = current_address
        self.lm = lm
        return self.visit(node)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self,node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self,node):
        return node.tok.value

    def visit_WordToken(self,node):
        return self.lm.get_label_address(node.value)

    def visit_AddressNode(self,node):
        return self.current_Address

    def visit_BinOpNode(self,node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op_tok.type == TT_PLUS:
            return left + right
        elif node.op_tok.type == TT_MINUS:
            return left - right
        elif node.op_tok.type == TT_MUL:
            return left * right
        elif node.op_tok.type == TT_DIV:
            return left / right
        else: raise InvalidSyntaxError(f"Invalid binOp operands {left.source} & {right.source}; {node.op_tok.type}", node.op_tok.line)

    def visit_UnaryOpNode(self,node):
        if node.op_tok.type == TT_MINUS:
            value = self.visit(node.node)
            return -value
