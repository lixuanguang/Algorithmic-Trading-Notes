.DEFAULT_GOAL := check

UV := uv
# Every sync and run installs the project non-editable; see [tool.uv] in pyproject.toml.
UV_SYNC := $(UV) sync --frozen --no-editable
UV_RUN := $(UV) run --frozen --no-editable
PYTHON_PATHS := src

.PHONY: sync lock-check format format-check lint typecheck test check-compendium check-coverage \
	verify-outlines pdf model-reference pre-commit source-check check

sync:
	$(UV_SYNC)

lock-check:
	$(UV) lock --check

format:
	$(UV_RUN) ruff format $(PYTHON_PATHS)

format-check:
	$(UV_RUN) ruff format --check $(PYTHON_PATHS)

lint:
	$(UV_RUN) ruff check $(PYTHON_PATHS)

# Strict mypy over everything under src, as listed in [tool.mypy] files.
typecheck:
	$(UV_RUN) mypy

test:
	$(UV_RUN) pytest -q

check-compendium:
	$(UV_RUN) python -m trading_notes.cli.check_compendium --check

check-coverage:
	$(UV_RUN) python -m trading_notes.cli.check_coverage --check

# Needs the git-ignored outline copies in reading_materials/outlines/.
verify-outlines:
	$(UV_RUN) python -m trading_notes.cli.check_coverage --check --verify-outlines

# Needs a LuaLaTeX installation with latexmk.
pdf:
	cd compendium && latexmk -lualatex -interaction=nonstopmode -halt-on-error compendium.tex

# The standalone model reference; it shares the compendium's preamble and house macros.
model-reference:
	cd model-derivations && latexmk -lualatex -interaction=nonstopmode -halt-on-error model-reference.tex

pre-commit:
	$(UV_RUN) pre-commit run --all-files

source-check: lock-check lint format-check typecheck check-compendium check-coverage test

check: source-check verify-outlines pdf model-reference
