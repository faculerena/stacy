import sys

from detectors import tx_sender_check, divide_before_multiply, call_inside_as_contract, unwrap_panic_usage, \
    assert_block_height
from linter_runner import LinterRunner


def main():
    if len(sys.argv) < 2:
        path = "examples/example.clar"
    else:
        path = sys.argv[1]

    with open(path, 'r') as file:
        source = file.read()

    parser: LinterRunner = LinterRunner(source)

    parser.add_lint(tx_sender_check)
    parser.add_lint(divide_before_multiply)
    parser.add_lint(call_inside_as_contract)
    parser.add_lint(unwrap_panic_usage)
    parser.add_lint(assert_block_height)


    while True:
        node = parser.next()
        if node is None:
            break
        parser.run_lints(node)


if __name__ == '__main__':
    main()
