import collections.abc

from tree_sitter import Node

from print_message import pretty_print_warn
from visitor import Visitor, NodeIterator


class TxSenderDetector(Visitor):
    MSG = "Use of tx-sender inside an assert"

    def __init__(self):
        super().__init__()

    def visit_node(self, node: Node, i):
        if i > 1:
            return
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

    def visit_node(self, node: Node, i):
        if i > 1:
            return
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

    def visit_node(self, node: Node, i):
        if i > 1:
            return
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

    def visit_node(self, node: Node, i):
        if i > 1:
            return
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

    def visit_node(self, node: Node, i):
        if i > 1:
            return
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


class ReadOnlyNotUsed(Visitor):
    MSG = "This private function is not used."
    read_only_names: [Node] = []

    def __init__(self):
        super().__init__()
        self.read_only_names: [Node] = []

    def visit_node(self, node: Node, run_number: int):
        #if run_number == 1 and node.grammar_name == "define-private":
        if run_number == 1 and node.grammar_name == "define-private":
            self.read_only_names.append(node)
            return

        # this can be improved with a better grammar (if not, stx-get-balance and other
        # intrinsic functions will throw as "not used" because they are not defined in the file
        if run_number == 2:
            if node.grammar_name == "define-public" or node.grammar_name == "define-read-only":
                descendants = NodeIterator(node.parent)
                while True:
                    n = descendants.next()
                    if n is None:
                        break
                    if n.grammar_name == "contract_function_call":
                        for saved in self.read_only_names:
                            if saved.child(2).child(1).text == n.child(1).text:
                                self.read_only_names.remove(saved)

            if node.grammar_name == "fold" or node.grammar_name == "map" or node.grammar_name == "filter":
                for saved in self.read_only_names:
                    if saved.child(2).child(1).text == node.parent.parent.child(2).text:
                        self.read_only_names.remove(saved)

        if run_number == 3:
            for n in self.read_only_names:
                pretty_print_warn(
                    self,
                    n,
                    n,
                    self.MSG,
                    None
                )
            self.read_only_names = []
