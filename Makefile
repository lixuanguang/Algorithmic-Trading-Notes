.DEFAULT_GOAL := check

UV := uv
# Install the project package non-editable; see [tool.uv] in pyproject.toml.
export UV_NO_EDITABLE := 1
PYTHON_PATHS := src tools tests notes/artefacts
# Numerical evidence scripts; preserved superseded runs live one level deeper and are excluded.
CHECK_SCRIPTS := $(sort $(wildcard notes/artefacts/*/*check*.py))

.PHONY: sync lock-check format format-check lint typecheck test check-compendium check-coverage \
	verify-outlines examples pdf pre-commit source-check check

sync:
	$(UV) sync --frozen

lock-check:
	$(UV) lock --check

format:
	$(UV) run --frozen ruff format $(PYTHON_PATHS)

format-check:
	$(UV) run --frozen ruff format --check $(PYTHON_PATHS)

lint:
	$(UV) run --frozen ruff check $(PYTHON_PATHS)

# Strict mypy over the migrated scope listed in [tool.mypy] files.
typecheck:
	$(UV) run --frozen mypy

test:
	$(UV) run --frozen pytest -q

check-compendium:
	$(UV) run --frozen python tools/check_compendium.py --check

check-coverage:
	$(UV) run --frozen python tools/check_coverage.py --check

# Needs the git-ignored outline copies in reading_materials/outlines/.
verify-outlines:
	$(UV) run --frozen python tools/check_coverage.py --check --verify-outlines

# Each script runs from its own folder because some read files next to them.
examples:
	@set -e; for f in $(CHECK_SCRIPTS); do \
		if ! (cd "$$(dirname "$$f")" && $(UV) run --frozen --project "$(CURDIR)" \
			python -W error "$$(basename "$$f")" > /dev/null 2>&1); then \
			echo "FAILED: $$f"; exit 1; \
		fi; \
	done; echo "$(words $(CHECK_SCRIPTS)) numerical check scripts passed"

# Needs a LuaLaTeX installation with latexmk.
pdf:
	cd compendium && latexmk -lualatex -interaction=nonstopmode -halt-on-error compendium.tex

pre-commit:
	$(UV) run --frozen pre-commit run --all-files

source-check: lock-check lint format-check typecheck check-compendium check-coverage test examples

check: source-check verify-outlines pdf
