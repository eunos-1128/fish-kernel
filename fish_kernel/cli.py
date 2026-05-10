import sys
from typing import Optional

from . import __version__
from .install import main as install_main


def main(argv: Optional[list[str]] = None):
    args = list(argv) if argv is not None else sys.argv[1:]

    if not args or args[0] in {"-h", "--help"}:
        print("usage: fish-kernel <command> [options]")
        print("")
        print("commands:")
        print("  install   Install Fish kernel spec into Jupyter")
        return 0

    if args[0] in {"-V", "--version"}:
        print(__version__)
        return 0

    if args[0] == "install":
        return install_main(args[1:])

    print(f"Unknown command: {args[0]}", file=sys.stderr)
    print("Run `fish-kernel --help` for usage.", file=sys.stderr)
    return 2
