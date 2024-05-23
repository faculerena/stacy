import sys

import tree_sitter
import tree_sitter_clarity
from tree_sitter import Language, Parser, Tree, TreeCursor, Node

CLARITY = Language(tree_sitter_clarity.language())


class LinterRunner:
    cursor: TreeCursor = None
    parser: Parser = None
    source: str = None
    visited = {}
    tree: Tree = None

    def __init__(self, source: str):
        self.parser = Parser(CLARITY)
        self.visited = []
        self.source = source
        self.tree = self.parser.parse(bytes(self.source, "utf8"))
        self.cursor = self.tree.walk()

        while self.cursor.goto_first_child():
            pass

    def node(self):
        return self.cursor.node

    def next(self) -> Node | None:  # fn next(&mut self) -> Option<Node>
        while True:  # loop {
            node = self.node()  # let node = self.cursor.node();
            # si no fue visitado
            if not self.visited.__contains__(node):  # if !self.visited.contains(&node) {
                if self.cursor.goto_first_child():  # if self.cursor.goto_first_child() {
                    continue  # continue; }
                self.visited.append(node)  # self.visited.insert(node);
                return node  # return Some(node) }

            # si fue visitado
            if self.cursor.goto_next_sibling():  # if self.cursor.goto_next_sibling() {
                while self.cursor.goto_next_sibling():  # while self.cursor.goto_first_child() {}
                    pass
            else:  # } else {
                # sin siblings
                if not self.cursor.goto_parent():  # if !self.cursor.goto_parent() {
                    # es root
                    return None  # return None;
                parent_node = self.cursor.node  # let parent_node = self.cursor.node()
                self.visited.append(parent_node)  # self.visited.insert(parent_node);
                return parent_node  # return Some(parent_node);


def main():
    if len(sys.argv) < 2:
        path = "examples/example.clar"
    else:
        path = sys.argv[1]

    with open(path, 'r') as file:
        source = file.read()

    #parser: LinterRunner = LinterRunner(source)

    parser = Parser(CLARITY)
    visited = []
    tree = parser.parse(bytes(source, "utf8"))
    cursor = tree.walk()

    cursor.goto_first_child()
    print(cursor.node)
    cursor.goto_next_sibling()
    print(cursor.node)
    cursor.goto_first_child()
    print(cursor.node)
    print(tree.root_node.kind_id)


if __name__ == '__main__':
    main()
