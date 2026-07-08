import sys
from typing import Optional

from . import __version__
from .install import main as install_main
from .remove import main as remove_main


def main(argv: Optional[list[str]] = None):
    args = list(argv) if argv is not None else sys.argv[1:]

    if not args or args[0] in {"-h", "--help"}:
        print("usage: fish-kernel <command> [options]")
        print("")
        print("commands:")
        print("  add         Install Fish kernel spec into Jupyter")
        print("  remove      Remove Fish kernel spec from Jupyter")
        print("  install     Alias of `add`")
        print("  uninstall   Alias of `remove`")
        return 0

    if args[0] in {"-V", "--version"}:
        print(__version__)
        return 0

    if args[0] in {"add", "install"}:
        return install_main(args[1:])

    if args[0] in {"remove", "uninstall"}:
        return remove_main(args[1:])

    print(f"Unknown command: {args[0]}", file=sys.stderr)
    print("Run `fish-kernel --help` for usage.", file=sys.stderr)
    return 2
