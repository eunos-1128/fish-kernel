# Fish Kernel for Jupyter

`fish-kernel` is a Jupyter kernel implementation for the fish shell.

![](./README.png)

## Requirements

- Python `>=3.10`
- `fish` command available on `PATH`
- Jupyter frontend (`jupyterlab` or notebook)
- Supported OS: Linux, macOS, and Windows (WSL)
- Native Windows is not supported (fish shell dependency)

## Install

### PyPI

```shell
pip install fish-kernel
```

### conda-forge

Install from the conda-forge channel with conda, mamba, or pixi:

```shell
conda install -c conda-forge fish-kernel
```

```shell
mamba install -c conda-forge fish-kernel
```

```shell
pixi add fish-kernel -c conda-forge
```

After installation, register the kernelspec.

`fish-kernel install` requires one of `--user`, `--sys-prefix`, or `--prefix`.

Install for your user account:

```shell
fish-kernel install --user
```

Or install into the current Python environment:

```shell
fish-kernel install --sys-prefix
```

After installation, verify the kernel is registered:

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

## Documentation

Build docs locally with Sphinx + Furo:

```shell
uv sync --dev
uv run sphinx-build -b html docs docs/_build/html
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

- [bash_kernel](https://github.com/takluyver/bash_kernel)
- [zsh-jupyter-kernel](https://github.com/dahn-zk/zsh-jupyter-kernel)
