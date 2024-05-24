import sys

from detectors import TxSenderDetector, DivideBeforeMultiplyDetector, UnwrapPanicDetector, \
    AssertBlockHeightDetector, CallInsideAsContract
from visitor import LinterRunner


def main():
    if len(sys.argv) < 2:
        path = "examples/example.clar"
    else:
        path = sys.argv[1]

    with open(path, 'r') as file:
        source = file.read()

    runner: LinterRunner = LinterRunner(source)

    lints = [
        TxSenderDetector(),
        DivideBeforeMultiplyDetector(),
        UnwrapPanicDetector(),
        AssertBlockHeightDetector(),
        CallInsideAsContract()
    ]
    for lint in lints:
        lint.add_source(source)

    runner.add_lints(lints)

    runner.run()




if __name__ == '__main__':
    main()
