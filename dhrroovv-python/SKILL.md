---
name: dhrroovv-python
description: Dhruv's Python conventions: default Python version and tooling (uv, ruff, pyright), coding style, Pydantic usage, error handling, and how to scaffold a new project. Use whenever creating, scaffolding, or modifying Python code or Python projects, or adding Python dependencies. When scaffolding, set the repo's git identity from the GitHub accounts on this machine, and ask which account to use when more than one is logged in.
---

# Python conventions

Existing project conventions win over these defaults. In an existing repo, follow what is already there (layout, tooling, versions) and do not restructure unless asked.

## Defaults

- Python 3.12.
- Package manager: `uv` only. Use `uv add`, `uv remove`, `uv sync`, `uv run`. Never use pip, poetry, or manually activated venvs. Commit `uv.lock` and `.python-version`.
- Layout: flat. Use `src/` only for a library meant to be published, and only when asked. Why: uv 0.12+ packages projects by default, and apps don't need a build system.
- Lint and format: `ruff`. Type checking: `pyright`.

## Directory boundaries

Organise top-level directories by what each one is for. The application package (for example `app/`) holds only code the running service imports. Anything that supports or operates on it without being part of its runtime sits beside it at the repo root: `tests/`, `migrations/`, `scripts/`, `docs/`, `fixtures/`. Why: the application package is the unit that gets bundled and deployed, so keeping tooling outside it keeps that unit small, self-contained, and importable on its own.

When adding a new directory, ask "does the running service import this?" If yes, it goes inside the application package. If it only tests, migrates, seeds, or documents the service, it goes at the root. Apply this to any new directory, not only the ones listed above.

This is about where code lives, not what ends up in the image: the Dockerfile may still copy `migrations/` so they can run from the built image. Application code never imports from root-level tooling directories; tooling may import the application.

## Before finishing any task

```bash
uv run ruff check --fix
uv run ruff format
uv run pyright
```

Fix everything reported. Don't silence a rule with an ignore comment unless there is a reason, and state it in a short comment.

## Style

- Type hints are required on every function and method: all parameters and the return type (including `-> None`). Local variables don't need annotations; add one only when inference would be wrong or unclear.
- Use current idioms for the target Python version: `X | None` (never `Optional`), built-in generics (`list[str]`), the `type` alias statement, PEP 695 generics (`def first[T](items: list[T]) -> T`), `pathlib`, f-strings. If unsure what the current recommended way is, check docs.python.org or peps.python.org instead of relying on memory.
- No docstrings. Add a short one-line `#` comment only where the why isn't obvious. Never narrate what the code does.
- Names: short, reflecting the general task or meaning. Use underscores to join words when one word isn't clear enough (`parse_row`, `user_id`).
- A leading underscore marks something internal to a class or module, and is for methods and functions only (`_build_query`). Don't use leading underscores on variables or attributes.
- Classes are PascalCase. No special convention for constants.
- Don't add abstractions, helpers, dependencies, or files that weren't asked for.

## Pydantic

- Use Pydantic where it already does the job instead of hand-writing it elsewhere: config (`pydantic-settings`), validating and parsing external data (API payloads, files, env), and structured data crossing a boundary.
- Stay at the simple end: `BaseModel`, built-in types, `Field` constraints, `model_validate`. Use custom validators, computed fields, generics, or discriminated unions only when clearly simpler than the alternative.
- Config lives in one `Settings(BaseSettings)` class in `config.py` that reads `.env`. No scattered `os.getenv`. Every key must also appear in `.env.example`.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = "development"
    loglevel: str = "INFO"


settings = Settings()
```

## Error handling

- Catch specific exceptions. Never a bare `except:` or a silent `except Exception: pass`.
- Validate input at the boundary and fail early with a clear message.
- Add context when re-raising: `raise X("...") from err`.
- Define custom exception classes only when callers need to react differently.
- Log with `logging` (module-level logger). No `print` outside intentional CLI output.

## Testing

Not scaffolded by default. When asked to add tests, use `pytest` with `tests/` at the repo root and add `pythonpath = ["."]` under `[tool.pytest.ini_options]` so flat-layout imports work.

## Git identity

When scaffolding, if the directory is not already a git repo, initialise it and pin one GitHub account to that repo. Never change global git config, and never switch the active `gh` account.

List the accounts on this machine with `gh auth status`. If more than one is logged in, ask which login to use. If only one is logged in, use it. If none are logged in, ask for the name and email. Do not copy the global git identity.

`user.name` is the chosen login. For `user.email`, read that account without printing its token. Try `email` from `gh api user`, then the primary entry from `gh api user/emails`. Call both with `GH_TOKEN=$(gh auth token --user <login>)`. If neither returns an email, ask for it.

Then, in this repo only:

```bash
git init
git config --local user.name "<login>"
git config --local user.email "<email>"
git config --local --unset-all credential.https://github.com.helper || true
git config --local --add credential.https://github.com.helper ''
git config --local --add credential.https://github.com.helper '!f() { echo "username=<login>"; echo "password=$(gh auth token --user <login>)"; }; f'
```

The blank helper drops inherited GitHub credentials for this repo, so a later push uses the chosen login while another account stays the default `gh` user. Do not commit `.git/config`.

## Scaffolding a new project

1. `uv init --no-package --python 3.12 <name>` (in an existing empty directory, omit `<name>`). The `--no-package` flag is mandatory; it keeps the flat layout.
2. Set the git identity above.
3. `uv add --dev ruff pyright`
4. If the project needs config: `uv add pydantic-settings`.
5. Append `assets/pyproject-tools.toml` to `pyproject.toml`.
6. Replace the generated `.gitignore` with `assets/gitignore`. Copy `assets/env.example` to `.env.example`, `assets/dockerignore` to `.dockerignore`, and `assets/Dockerfile` and `assets/compose.yaml` to the project root. Adjust the command, ports, and services to fit the project.
7. Do not create `tests/`, a Makefile, or a justfile unless asked.
8. Run the checks above once to confirm a clean baseline.

Expected result:

```
<name>/
├── .env.example
├── .dockerignore
├── .gitignore
├── .python-version
├── Dockerfile
├── compose.yaml
├── config.py        # only if the project needs config
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

## Superseded patterns

<!-- Record old habits here: what, date dropped, why. -->
