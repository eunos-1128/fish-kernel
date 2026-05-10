# Fish Kernel for Jupyter

`fish-kernel` is a Jupyter kernel implementation for the fish shell.

![](./README.png)

## Requirements

- Python `>=3.10`
- `fish` command available on `PATH` (tested with fish `4.7.1`)
- Jupyter frontend (`jupyterlab` or notebook)

## Install

### From PyPI

```shell
pip install fish-kernel
```

### Register kernelspec

Install for your user account:

```shell
fish-kernel install --user
```

Or install into the current Python environment:

```shell
fish-kernel install --sys-prefix
```

### Verify

```shell
jupyter kernelspec list
```

You should see a `fish` kernel entry.

## Development install (source)

```shell
uv venv .venv
uv pip install --python .venv -e .
.venv/bin/fish-kernel install --user
.venv/bin/jupyter kernelspec list
```

## Usage examples

Simple calculation:

```fish
set a 7
set b 13
math $a + $b
```
