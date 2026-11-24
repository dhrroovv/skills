# Changelog

- 2026-11-22: Initial version (Python 3.12, uv flat layout, ruff, pyright, Pydantic rules, Docker scaffold).
- 2026-11-22: Underscores allowed to join words in names; leading underscore reserved for internal methods/functions only; dropped UPPER_SNAKE constants rule.
- 2026-11-24: Added Directory boundaries (application package holds only runtime code; tests, migrations, scripts, docs sit beside it at the root).
