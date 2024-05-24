from tree_sitter import Node

from print_message import pretty_print_warn
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
                    pretty_print_warn(
                        self,
                        node.parent,
                        node,
                        "Ojo con usar tx-sender adentro de un assert",
                        None
                    )


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
                    pretty_print_warn(
                        self,
                        node.parent,
                        node,
                        "Ojo con dividir antes de multiplicar",
                        None
                    )


class UnwrapPanicDetector(Visitor):
    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node):
        if str(node.text, "utf8") == "unwrap-panic":
            pretty_print_warn(
                self,
                node.parent,
                node,
                "Preferible usar unwrap!",
                None
            )


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
                    pretty_print_warn(
                        self,
                        node.parent,
                        node,
                        "Ojo con chequear con block-height en un assert",
                        None
                    )


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
                    pretty_print_warn(
                        self,
                        node.parent,
                        node,
                        "Ojo con usar as-contract con algo no constante",
                        None
                    )
                    self.call = False
                    self.principal_literal = False
