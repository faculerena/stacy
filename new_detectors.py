from tree_sitter import Node

from visitor import Visitor, NodeIterator


class TxSenderDetector(Visitor):

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node):
        if str(node.text, "utf8") == "asserts!":
            descendants = NodeIterator(node.parent)
            while True:
                n = descendants.next()
                if n is None:
                    break
                if str(n.text, "utf8") == "tx-sender" and n.grammar_name == "global":
                    print("ojito", str(node.parent.text, "utf8"))


class DivideBeforeMultiplyDetector(Visitor):
    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node):
        if node.grammar_name == "arithmetic_function" and str(node.text, "utf8") == "*":
            descendants = NodeIterator(node.parent)
            while True:
                n = descendants.next()
                if n is None:
                    break
                if str(n.text, "utf8") == "/" and n.grammar_name == "arithmetic_function":
                    print("ojito", str(node.parent.text, "utf8"))


class UnwrapPanicDetector(Visitor):
    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node):
        if str(node.text, "utf8") == "unwrap-panic":
            print("ojito", str(node.parent.text, "utf8"))


class AssertBlockHeightDetector(Visitor):

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node):
        if str(node.text, "utf8") == "asserts!":
            descendants = NodeIterator(node.parent)
            while True:
                n = descendants.next()
                if n is None:
                    break
                if str(n.text, "utf8") == "block-height" and n.grammar_name == "global":
                    print("ojito", str(node.parent.text, "utf8"))


class CallInsideAsContract(Visitor):

    def __init__(self):
        super().__init__()
        self.call = False
        self.principal_literal = False

    def visit_node(self, node: Node):
        if str(node.text, "utf8") == "as-contract":
            descendants = NodeIterator(node.parent)
            while True:
                n = descendants.next()
                if n is None:
                    break
                if str(n.text, "utf8") == "contract-call?":
                    self.call = True
                if n.grammar_name == "contract_principal_lit":
                    self.principal_literal = True
                if self.call and not self.principal_literal:
                    print("ojito", str(node.parent.text, "utf8"))
                    self.call = False
                    self.principal_literal = False
