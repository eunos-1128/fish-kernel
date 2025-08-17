# Fish Kernel for Jupyter

`fish-kernel` is a Jupyter kernel implementation for the fish shell.

## Requirements

- Python `>=3.9`
- `fish` command available on `PATH` (tested with fish `4.7.1`)
- Jupyter frontend (`jupyterlab` or notebook)

## Install

### From PyPI

```bash
python -m pip install fish-kernel
```

## Register kernelspec

Install for your user account:

```bash
python -m fish_kernel.install --user
```

Or install into the current Python environment:

```bash
python -m fish_kernel.install --sys-prefix
```

## Verify

```bash
jupyter kernelspec list
```

You should see a `fish` kernel entry.

## Development install (source)

```bash
uv venv .venv
uv pip install --python .venv -e .
.venv/bin/python -m fish_kernel.install --sys-prefix
.venv/bin/jupyter kernelspec list
```

## Usage examples

Simple calculation:

```fish
set a 7
set b 13
math $a + $b
```
