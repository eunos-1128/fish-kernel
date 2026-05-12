# Installation

## Install from PyPI

```shell
pip install fish-kernel
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
