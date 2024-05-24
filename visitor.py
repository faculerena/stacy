import math

import tree_sitter_clarity
from tree_sitter import Language, TreeCursor, Parser, Tree, Node

CLARITY = Language(tree_sitter_clarity.language())


class Visitor:
    source: str | None

    def __init__(self):
        self.source = None

    def add_source(self, source: str):
        self.source = source

    def visit_node(self, node: Node):
        pass


class NodeIterator:
    root_node: Node
    cursor: TreeCursor
    visited = []

    def __init__(self, node: Node):
        self.root_node = node
        self.cursor = node.walk()
        self.visited = []

        while self.cursor.goto_first_child():
            pass

    def next(self) -> Node | None:
        while True:
            node = self.node()

            if not self.visited.__contains__(node):
                if self.cursor.goto_first_child():
                    continue
                self.visited.append(node)
                return node

            if self.cursor.goto_next_sibling():
                while self.cursor.goto_first_child():
                    pass
            else:

                if not self.cursor.goto_parent():
                    return None
                parent_node = self.cursor.node
                self.visited.append(parent_node)
                return parent_node

    def node(self) -> Node | None:
        return self.cursor.node


class LinterRunner:
    source: str
    tree: Tree
    root_node: Node
    iterator: NodeIterator
    lints: []  # lo que vaya acá adentro REQUIERE tener el metodo visit_node (at least)

    def __init__(self, source: str):
        self.source = source
        parser = Parser(CLARITY)
        self.tree = parser.parse(bytes(self.source, "utf8"))
        self.root_node = self.tree.root_node
        self.iterator = NodeIterator(self.root_node)
        self.lints = []

    def run_lints(self, node: Node):
        for lint in self.lints:
            lint.visit_node(node)

    def add_lint(self, lint):
        self.lints.append(lint)
        return self

    def add_lints(self, lints):
        self.lints.extend(lints)

    def run(self):
        while True:
            v = self.iterator.next()
            if v is None:
                break
            self.run_lints(v)
