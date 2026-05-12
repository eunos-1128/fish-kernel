from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INIT_FILE = ROOT / "fish_kernel" / "__init__.py"
VERSION_RE = re.compile(r'^__version__\s*=\s*"([^"]+)"', re.MULTILINE)
VERSION_MATCH = VERSION_RE.search(INIT_FILE.read_text(encoding="utf-8"))
if VERSION_MATCH is None:
    raise RuntimeError("Could not read __version__ from fish_kernel/__init__.py")
PACKAGE_VERSION = VERSION_MATCH.group(1)

project = "fish-kernel"
author = "UENO, M."
release = PACKAGE_VERSION
version = PACKAGE_VERSION

extensions = ["myst_parser"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_title = "fish-kernel"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_theme_options = {
    "source_repository": "https://github.com/eunos-1128/fish-kernel/",
    "source_branch": "main",
    "source_directory": "docs/",
    "top_of_page_buttons": ["view", "edit"],
    "light_css_variables": {
        "color-brand-primary": "#0077b6",
        "color-brand-content": "#0077b6",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4cc9f0",
        "color-brand-content": "#4cc9f0",
    },
}

pygments_style = "sphinx"
pygments_dark_style = "monokai"

myst_enable_extensions = [
    "colon_fence",
]
