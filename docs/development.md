# Development

## Local setup

```shell
git clone https://github.com/eunos-1128/fish-kernel.git
cd fish-kernel
uv sync --dev
```

## Test

```shell
uv run pytest
```

## Build package

```shell
uv build
```

## Build docs

```shell
uv run sphinx-build -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in your browser.
