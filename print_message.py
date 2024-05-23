import math

from tree_sitter import Node

from linter_runner import LinterRunner


def pretty_print_warn(runner: LinterRunner, parent: Node, specific_node: Node, msg: str):
    line_number = parent.start_point.row + 1
    num_size = int(math.log10(line_number))

    line = runner.source.split('\n')[line_number - 1]

    arrows = "^" * (specific_node.end_point.column - specific_node.start_point.column)

    spaces = " " * (specific_node.start_point.column - num_size + 3)

    print(line_number, "|", line)
    print(spaces, arrows)
    print(spaces, msg)
    print()

