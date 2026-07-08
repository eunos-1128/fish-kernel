# Installation

To register a Jupyter kernel, run a concrete install command such as:

```shell
fish-kernel add --user
```

If you want to install into the current Python environment instead, use:

```shell
fish-kernel add --sys-prefix
```

`fish-kernel install` is an alias of `fish-kernel add`, so either name works.

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
pixi add fish-kernel
```

## Register kernelspec

`fish-kernel add` requires exactly one target option.

### User scope

```shell
fish-kernel add --user
```

Installs into your user Jupyter directory.

### Environment scope

```shell
fish-kernel add --sys-prefix
```

Installs into the current `sys.prefix` environment.

### Custom scope

```shell
fish-kernel add --prefix /path/to/prefix
```

Installs into a custom prefix.

## Verify installation

```shell
jupyter kernelspec list
```

Confirm that `fish` exists in the list.

## Remove kernelspec

To unregister the kernelspec, run:

```shell
fish-kernel remove
```

`fish-kernel uninstall` is an alias of `fish-kernel remove`.

Unlike `add`, a target option is optional. With no options, `remove` deletes
whichever installed copy it finds first. If you installed the kernel into
more than one scope (for example both `--user` and `--sys-prefix`), pass the
matching option to target a specific one:

```shell
fish-kernel remove --user
fish-kernel remove --sys-prefix
fish-kernel remove --prefix /path/to/prefix
```
