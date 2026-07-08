# Installation

To register a Jupyter kernel, run a concrete install command such as:

```shell
fish-kernel install --user
```

If you want to install into the current Python environment instead, use:

```shell
fish-kernel install --sys-prefix
```

## Install from PyPI

```shell
pip install fish-kernel
```

## Install from conda-forge

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

## Register kernelspec

`fish-kernel install` requires exactly one target option.

### User scope

```shell
fish-kernel install --user
```

Installs into your user Jupyter directory.

### Environment scope

```shell
fish-kernel install --sys-prefix
```

Installs into the current `sys.prefix` environment.

### Custom scope

```shell
fish-kernel install --prefix /path/to/prefix
```

Installs into a custom prefix.

## Verify installation

```shell
jupyter kernelspec list
```

Confirm that `fish` exists in the list.
