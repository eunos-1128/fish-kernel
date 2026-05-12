# Troubleshooting

## `fish-kernel install` only shows help

You must pass one of:

- `--user`
- `--sys-prefix`
- `--prefix /path`

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
