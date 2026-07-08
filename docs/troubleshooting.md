# Troubleshooting

## `fish-kernel add` only shows help

You must pass one of:

- `--user`
- `--sys-prefix`
- `--prefix /path`

`fish-kernel install` behaves the same way, since it is an alias of `fish-kernel add`.

## `fish-kernel remove` reports no such kernel spec

The `fish` kernelspec is not currently registered (in the scope you
specified, if any). Run `fish-kernel add --user` (or `--sys-prefix` /
`--prefix`) first, then try `fish-kernel remove` (or its alias
`fish-kernel uninstall`) again.

## `fish-kernel remove` did not remove the copy I expected

If `fish` is installed in more than one scope (for example both `--user`
and `--sys-prefix`), running `fish-kernel remove` with no options only
removes whichever copy is found first. Pass the matching option to target
a specific scope:

```shell
fish-kernel remove --user
fish-kernel remove --sys-prefix
fish-kernel remove --prefix /path/to/prefix
```

## `fish` kernel does not appear in Jupyter

1. Re-run installation with the same Python environment as Jupyter.
2. Run `jupyter kernelspec list`.
3. Confirm `fish` is listed.

## `fish` command not found

Install fish and ensure `fish` is on `PATH`.

## Platform support

- Linux and macOS are supported.
- Windows is supported when you run inside WSL.
- Native Windows is not supported because this project depends on fish shell.
