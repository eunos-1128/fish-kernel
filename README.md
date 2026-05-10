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

`fish-kernel install` requires one of `--user`, `--sys-prefix`, or `--prefix`.

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

## Development

```shell
git clone https://github.com/eunos-1128/fish-kernel.git
cd fish-kernel
uv sync --dev
uv run pytest
uv run fish-kernel install --sys-prefix
uv run jupyter kernelspec list
```

## Usage examples

Simple calculation:

```fish
set a 7
set b 13
math $a + $b
```

## Acknowledgements

This project was developed with inspiration from:

- [`bash_kernel`](https://github.com/takluyver/bash_kernel)
- [`zsh-jupyter-kernel`](https://github.com/dahn-zk/zsh-jupyter-kernel)
