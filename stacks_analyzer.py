import os
import sys
import argparse

from detectors.TxSender import TxSenderDetector
from detectors.AssertBlockHeight import AssertBlockHeightDetector
from detectors.DivideBeforeMultiply import DivideBeforeMultiplyDetector
from detectors.ReadOnlyNotUsed import ReadOnlyNotUsed
from detectors.UnwrapPanic import UnwrapPanicDetector
from detectors.CallInsideAsContract import CallInsideAsContract

from visitor import LinterRunner, Visitor


def main():
    arg_parser = argparse.ArgumentParser(description='Static Analyzer for the Clarity language from Stacks')
    subparsers = arg_parser.add_subparsers(dest="command", help="Commands")

    lint_parser = subparsers.add_parser("lint", help="Run detectors in a given contract or contracts directory")
    lint_parser.add_argument("path", type=str, help="Path")

    args = arg_parser.parse_args()

    if args.command == "lint":
        path = args.path
        if path.endswith(".clar"):
            lint_file(path)
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".clar"):
                        lint_file(os.path.join(root, file))


def lint_file(path):
    print(f"====== Linting {path}... ======")

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


if __name__ == '__main__':
    main()
