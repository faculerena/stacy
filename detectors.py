from tree_sitter._binding import Node

from linter_runner import LinterRunner
from print_message import pretty_print_warn


def tx_sender_check(runner: LinterRunner, node: Node):
    if node.grammar_name == "tx-sender":
        parent = runner.a_parent_contains("(asserts!")
        if parent is None:
            return
        pretty_print_warn(runner, parent, node, "Ojo con usar tx-sender adentro de un assert")
        runner.restore_after()


def divide_before_multiply(runner: LinterRunner, node: Node):
    if not node.text == b"/":
        return
    parent = runner.a_parent_contains("(*")
    if parent is None:
        return
    pretty_print_warn(runner, parent, node, "Ojo con dividir antes de multiplicar")
    runner.restore_after()


def call_inside_as_contract(runner: LinterRunner, node: Node):
    if node.text == b"contract-call?":
        parent = runner.a_parent_contains("(as-contract")
        if parent is None:
            return

        for child in node.parent.children:
            if b"." in child.text:
                return
        pretty_print_warn(runner, parent, node, "Ojo con usar as-contract con algo no constante")
        runner.restore_after()
