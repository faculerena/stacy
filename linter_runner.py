import tree_sitter_clarity
from tree_sitter import Language, TreeCursor, Parser, Tree, Node

CLARITY = Language(tree_sitter_clarity.language())


class LinterRunner:
    cursor: TreeCursor = None
    parser: Parser = None
    source: str = None
    visited = {}
    tree: Tree = None
    lints: []

    def __init__(self, source: str):
        self.lints = []
        self.parser = Parser(CLARITY)
        self.visited = []
        self.source = source
        self.tree = self.parser.parse(bytes(self.source, "utf8"))
        self.cursor = self.tree.walk()

        while self.cursor.goto_first_child():
            pass

    def node(self):
        return self.cursor.node

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

    def add_lint(self, lint):
        self.lints.append(lint)

    def run_lints(self, node: Node):
        for lint in self.lints:
            lint(self, node)

    def a_parent_contains(self, pattern) -> Node | None:
        while self.cursor.goto_parent():
            if bytes(pattern, "utf8") in self.cursor.node.text:
                return self.node()
        return None

    def restore_after(self):
        self.next()
        self.next()

