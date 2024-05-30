import os
import argparse
import sys

from stacks_analyzer.detectors.VarCouldBeConstant import VarCouldBeConstant
from .detectors.TxSender import TxSenderDetector
from .detectors.AssertBlockHeight import AssertBlockHeightDetector
from .detectors.DivideBeforeMultiply import DivideBeforeMultiplyDetector
from .detectors.ReadOnlyNotUsed import ReadOnlyNotUsed
from .detectors.UnwrapPanic import UnwrapPanicDetector
from .detectors.CallInsideAsContract import CallInsideAsContract
from .print_message import TerminalColors

from .visitor import LinterRunner, Visitor


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
    tty = sys.stdout.isatty()
    if tty:
        print(f"{TerminalColors.HEADER}====== Linting {path}... ======{TerminalColors.ENDC}")
    else:
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
        ReadOnlyNotUsed(),
        VarCouldBeConstant()
    ]

    runner.add_lints(lints)
    runner.run()


if __name__ == '__main__':
    main()
