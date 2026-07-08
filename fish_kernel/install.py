""""""

import argparse
import json
import os
import pathlib
import shutil
import sys
import tempfile
from typing import Optional

from jupyter_client.kernelspec import KernelSpecManager

from .resources import LOGO_PATH

kernel_json = {
    "argv": [sys.executable, "-m", "fish_kernel", "-f", "{connection_file}"],
    "display_name": "Fish",
    "language": "fish",
    "codemirror_mode": "shell",
}


def install_my_kernel_spec(user: bool = True, prefix: Optional[str] = None):
    with tempfile.TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, "kernel.json"), "w") as f:
            json.dump(kernel_json, f, sort_keys=True)

        shutil.copyfile(LOGO_PATH, pathlib.Path(td) / LOGO_PATH.name)

        print("Installing IPython kernel spec")
        KernelSpecManager().install_kernel_spec(td, "fish", user=user, prefix=prefix)


def main(argv: Optional[list[str]] = None) -> int:
    args_list = list(argv) if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description="Install KernelSpec for Fish Kernel")
    prefix_locations = parser.add_mutually_exclusive_group(required=True)

    prefix_locations.add_argument(
        "--user",
        help="Install KernelSpec in user's home directory",
        action="store_true",
    )
    prefix_locations.add_argument(
        "--sys-prefix",
        help="Install KernelSpec in sys.prefix. Useful in conda / virtualenv",
        action="store_true",
        dest="sys_prefix",
    )
    prefix_locations.add_argument(
        "--prefix", help="Install KernelSpec in this prefix", default=None
    )

    if not args_list:
        parser.print_help()
        return 2

    args = parser.parse_args(args_list)

    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user:
        user = True

    install_my_kernel_spec(user=user, prefix=prefix)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
