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

```shell
pip install fish-kernel
```

Or from conda-forge with conda, mamba, or pixi:

```shell
conda install -c conda-forge fish-kernel
mamba install -c conda-forge fish-kernel
pixi add fish-kernel
```

Then register the kernelspec:

```shell
fish-kernel add --user
```

Verify it is registered:

```shell
jupyter kernelspec list
```

To unregister it later, run `fish-kernel remove`.

## Usage example

```fish
set a 7
set b 13
math $a + $b
```

## Documentation

Full documentation, including all install options, usage, development, and
troubleshooting, is available at
<https://eunos-1128.github.io/fish-kernel/>.

## Acknowledgements

This project was developed with inspiration from:

- [bash_kernel](https://github.com/takluyver/bash_kernel)
- [zsh-jupyter-kernel](https://github.com/dahn-zk/zsh-jupyter-kernel)
