.DEFAULT_GOAL := check

UV := uv
# Every sync and run installs the project non-editable; see [tool.uv] in pyproject.toml.
UV_SYNC := $(UV) sync --frozen --no-editable
UV_RUN := $(UV) run --frozen --no-editable
PYTHON_PATHS := src notes/artefacts
# Numerical evidence scripts not yet moved into the package, so not run by the tests; scripts
# that forward to trading_notes.numerical are run once by `make test`. Preserved superseded runs
# live one level deeper and are excluded.
CHECK_SCRIPTS := $(sort $(shell grep -L '^from trading_notes\.numerical' notes/artefacts/*/*check*.py))

.PHONY: sync lock-check format format-check lint typecheck test check-compendium check-coverage \
	verify-outlines examples pdf pre-commit source-check check

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

# Strict mypy over the migrated scope listed in [tool.mypy] files.
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

# Each script runs once from an empty temporary folder, so none depends on the working
# directory (scripts find their data next to themselves) or writes into it.
examples:
	@set -e; tmp=$$(mktemp -d); trap 'rm -rf "$$tmp"' EXIT; \
	for f in $(CHECK_SCRIPTS); do \
		if ! (cd "$$tmp" && $(UV_RUN) --project "$(CURDIR)" \
			python -W error "$(CURDIR)/$$f" > /dev/null 2>&1); then \
			echo "FAILED: $$f"; exit 1; \
		fi; \
	done; \
	if [ -n "$$(ls -A "$$tmp")" ]; then echo "FAILED: files written to the working folder"; exit 1; fi; \
	echo "$(words $(CHECK_SCRIPTS)) check scripts passed"

# Needs a LuaLaTeX installation with latexmk.
pdf:
	cd compendium && latexmk -lualatex -interaction=nonstopmode -halt-on-error compendium.tex

pre-commit:
	$(UV_RUN) pre-commit run --all-files

source-check: lock-check lint format-check typecheck check-compendium check-coverage test examples

check: source-check verify-outlines pdf
