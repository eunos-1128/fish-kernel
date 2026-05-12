# Usage

## Select kernel

In JupyterLab or Notebook, open a notebook and select **Fish** as the kernel.

## Basic commands

```fish
echo "hello from fish"
set a 7
set b 13
math $a + $b
```

## Rich output helpers

The kernel provides helper functions in each session.

### Display a local image

```fish
cat /absolute/path/to/image.png | display
```

### Display HTML

```fish
echo '<b>hello from fish-kernel</b>' | displayHTML
```

### Display JavaScript

```fish
echo "console.log('fish-kernel');" | displayJS
```
