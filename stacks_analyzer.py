import os
import sys

from detectors import TxSenderDetector, DivideBeforeMultiplyDetector, UnwrapPanicDetector, \
    AssertBlockHeightDetector, CallInsideAsContract, ReadOnlyNotUsed
from visitor import LinterRunner, Visitor


def main():
    if len(sys.argv) < 2:
        lint_file("examples/example.clar")
    else:
        path = sys.argv[1]
        if path.endswith(".clar"):
            lint_file(path)
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    lint_file(os.path.join(root, file))


def lint_file(path):
    print(f" ====== Linting {path}... ======")

    with open(path, 'r') as file:
        source = file.read()

    runner: LinterRunner = LinterRunner(source)

    lints: [Visitor] = [
        TxSenderDetector(),
        DivideBeforeMultiplyDetector(),
        UnwrapPanicDetector(),
        AssertBlockHeightDetector(),
        CallInsideAsContract(),
        ReadOnlyNotUsed()
    ]
    runner.add_lints(lints)
    runner.run()
    runner.run()
    runner.run()


if __name__ == '__main__':
    main()
