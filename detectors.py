from tree_sitter import Node

from print_message import pretty_print_warn
from visitor import Visitor, NodeIterator


class TxSenderDetector(Visitor):
    MSG = "Use of tx-sender inside an assert"

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
                        self.MSG,
                        None
                    )


class DivideBeforeMultiplyDetector(Visitor):
    MSG = "Use of divide inside a multiplication. This could result in a precision loss"

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
                        self.MSG,
                        None
                    )


class UnwrapPanicDetector(Visitor):
    MSG = "Use of unwrap-panic. Use unwrap! and handle the error."

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node):
        if str(node.text, "utf8") == "unwrap-panic":
            pretty_print_warn(
                self,
                node.parent,
                node,
                self.MSG,
                None
            )


class AssertBlockHeightDetector(Visitor):
    MSG = "Use of block-height inside a assert"

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
                        self.MSG,
                        None
                    )


class CallInsideAsContract(Visitor):
    MSG = "Use of call-contract? inside an as-contract context."

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
                        self.MSG,
                        None
                    )
                    self.call = False
                    self.principal_literal = False
