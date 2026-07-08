""""""

import argparse
import os
import sys
from typing import Optional

from jupyter_client.kernelspec import KernelSpecManager

KERNEL_NAME = "fish"


def _scope_description(user: bool, prefix: Optional[str]) -> Optional[str]:
    if user:
        return "user"
    if prefix:
        return f"prefix {prefix!r}"
    return None


def remove_my_kernel_spec(user: bool = False, prefix: Optional[str] = None) -> str:
    if user and prefix:
        msg = "Can't specify both user and prefix. Please choose one or the other."
        raise ValueError(msg)

    manager = KernelSpecManager()
    if user:
        manager = KernelSpecManager(kernel_dirs=[manager.user_kernel_dir])
    elif prefix:
        kernels_dir = os.path.join(
            os.path.abspath(prefix), "share", "jupyter", "kernels"
        )
        manager = KernelSpecManager(kernel_dirs=[kernels_dir])

    print("Removing IPython kernel spec")
    return manager.remove_kernel_spec(KERNEL_NAME)


def main(argv: Optional[list[str]] = None) -> int:
    args_list = list(argv) if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description="Remove KernelSpec for Fish Kernel")
    prefix_locations = parser.add_mutually_exclusive_group(required=False)

    prefix_locations.add_argument(
        "--user",
        help="Remove KernelSpec from user's home directory",
        action="store_true",
    )
    prefix_locations.add_argument(
        "--sys-prefix",
        help="Remove KernelSpec from sys.prefix. Useful in conda / virtualenv",
        action="store_true",
        dest="sys_prefix",
    )
    prefix_locations.add_argument(
        "--prefix", help="Remove KernelSpec from this prefix", default=None
    )

    args = parser.parse_args(args_list)

    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user:
        user = True

    try:
        remove_my_kernel_spec(user=user, prefix=prefix)
    except KeyError:
        scope = _scope_description(user, prefix)
        if scope:
            print(
                f"No such kernel spec installed for {scope}: {KERNEL_NAME}",
                file=sys.stderr,
            )
        else:
            print(f"No such kernel spec installed: {KERNEL_NAME}", file=sys.stderr)
        return 1
    except OSError as e:
        print(e, file=sys.stderr)
        print("Perhaps you want sudo?", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
