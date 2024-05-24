import sys

from detectors import TxSenderDetector, DivideBeforeMultiplyDetector, UnwrapPanicDetector, \
    AssertBlockHeightDetector, CallInsideAsContract
from visitor import LinterRunner, Visitor


def main():
    if len(sys.argv) < 2:
        path = "examples/example.clar"
    else:
        path = sys.argv[1]

    with open(path, 'r') as file:
        source = file.read()

    runner: LinterRunner = LinterRunner(source)

    lints: [Visitor] = [
        TxSenderDetector(),
        DivideBeforeMultiplyDetector(),
        UnwrapPanicDetector(),
        AssertBlockHeightDetector(),
        CallInsideAsContract()
    ]

    runner.add_lints(lints)
    runner.run()


if __name__ == '__main__':
    main()
