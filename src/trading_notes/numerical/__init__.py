"""Numerical evidence checks for the compendium entries, and their shared reporting.

Each check module exposes `main()`, which runs its checks with a fresh report, prints a
summary and returns the exit status. Run one as a module, for example
`uv run --frozen --no-editable python -m trading_notes.numerical.multicurve`; it exits 0 when
every check passes and 1 otherwise. Importing a module runs nothing.
"""
