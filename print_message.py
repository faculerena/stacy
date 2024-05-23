import math

from tree_sitter import Node

from linter_runner import LinterRunner


def pretty_print_warn(runner: LinterRunner, parent: Node, specific_node: Node, msg: str):
    line_number = parent.start_point.row + 1
    num_size = int(math.log10(line_number))

    arrows = "^" * (specific_node.end_point.column - specific_node.start_point.column)

    spaces = " " * (specific_node.start_point.column - num_size + 2)

    prev_spaces = " " * (specific_node.start_point.column - num_size)

    print(line_number, prev_spaces, parent.text.decode("utf-8"))
    print(spaces, arrows)
    print(spaces, msg)
    print()

