---
name: dhrroovv-fastapi
description: Dhruv's defaults for scaffolding and structuring a FastAPI backend: stack, project structure, how routes and services are written, starter files, Docker/compose setup, and run commands. Use when creating or initialising a FastAPI project or adding routes and services to one. Builds on dhrroovv-python.
---

# FastAPI conventions

Load and follow the `dhrroovv-python` skill first, then apply this one. Where they conflict (for example, where `config.py` lives), this skill wins for FastAPI projects. Design decisions not covered here (auth, domain-folder splits, error handling approach, testing setup, and so on) are made per project: ask me, don't assume.

## Defaults

- Stack: FastAPI, async SQLAlchemy 2.0, Alembic, PostgreSQL (asyncpg), pydantic-settings.
- Async end to end: `async def` routes, async DB driver and session.
- Run in dev: `uv run fastapi dev`. In production: `fastapi run`. The app location is set in `pyproject.toml` via `[tool.fastapi] entrypoint = "app.main:app"`.
- Scaffold only the skeleton. Don't add endpoints, models, auth, CORS, middleware, health checks, or any other feature unless asked.

## Project structure

```
<name>/
├── app/
│   ├── __init__.py
│   ├── main.py        # app instance and lifespan
│   ├── core/          # infrastructure only
│   │   ├── __init__.py
│   │   ├── config.py  # Settings (pydantic-settings)
│   │   ├── db.py      # engine, session factory, get_session
│   │   └── deps.py    # shared Annotated dependencies (SessionDep)
│   ├── models/        # SQLAlchemy models (base.py to start)
│   ├── schemas/       # Pydantic request/response models
│   ├── routers/       # one APIRouter module per resource
│   └── services/      # business logic and DB queries (single layer)
├── migrations/        # Alembic
├── alembic.ini
└── pyproject.toml
```

Imports are absolute from the root (`from app.core.config import settings`). Keep `core/` for infrastructure only. Don't restructure unless I ask.

## Layers

### Routers

- Thin HTTP layer: parse input, call one service function, return the response. No queries and no business logic in routes.
- One `router = APIRouter(prefix="/items", tags=["items"])` per resource file, registered in `main.py` with `app.include_router`.
- Plural resource paths. Short verb-first function names (`list_items`, `get_item`, `create_item`). Explicit `status_code` for anything other than 200 (201 for create, 204 for delete). PATCH for partial updates.
- Get the session with `SessionDep` and pass it to the service.
- Declare the response through the return type (`-> ItemRead`) and convert with `ItemRead.model_validate(obj)`. Use separate schemas per purpose (`ItemCreate`, `ItemUpdate`, `ItemRead`). Never return ORM models directly. Read schemas set `from_attributes=True`.

### Services

- One layer holds both business logic and DB access. No separate repository layer.
- One module per resource (`services/items.py`) of plain async functions. They take `session` as the first argument, run SQLAlchemy 2.0 `select()` queries, apply business rules, and own the transaction (commit and rollback). Routes never commit.
- Services don't import from `fastapi`.

Shape reference only (don't scaffold these):

```python
# app/services/items.py
async def list_items(session: AsyncSession) -> list[Item]:
    result = await session.scalars(select(Item).order_by(Item.id))
    return list(result)


async def create_item(session: AsyncSession, data: ItemCreate) -> Item:
    item = Item(**data.model_dump())
    session.add(item)
    await session.commit()
    return item
```

```python
# app/routers/items.py
@router.get("")
async def list_items(session: SessionDep) -> list[ItemRead]:
    return [ItemRead.model_validate(i) for i in await items.list_items(session)]


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemCreate, session: SessionDep) -> ItemRead:
    return ItemRead.model_validate(await items.create_item(session, data))
```

## Scaffolding a new project

1. Run the scaffold steps from `dhrroovv-python` (`uv init --no-package --python 3.12`, dev tools, gitignore, etc.), then delete the generated root `main.py` (and root `config.py` if present). Code lives in `app/`.
2. `uv add "fastapi[standard]" "sqlalchemy[asyncio]" asyncpg alembic pydantic-settings`
3. Copy this skill's `assets/app/` to `./app/`.
4. Append `assets/pyproject-fastapi.toml` to `pyproject.toml`.
5. `uv run alembic init -t async migrations`, then in `migrations/env.py` add after `config = context.config`:
    ```python
    from app.core.config import settings
    from app.models import Base

    config.set_main_option("sqlalchemy.url", settings.database_url.replace("%", "%%"))
    target_metadata = Base.metadata
    ```
    and remove the template's original `target_metadata = None` line.
6. Replace `.env.example`, `Dockerfile`, and `compose.yaml` with this skill's `assets/` versions (they supersede the Python skill's).
7. Run the checks from `dhrroovv-python`, then confirm the app imports: `uv run python -c "from app.main import app"`.

Expected result: everything from the Python scaffold, plus `app/`, `migrations/`, `alembic.ini`, and a `compose.yaml` with `app` and `db` services. No endpoints, models, or migrations yet.

## Superseded patterns

<!-- Record old habits here: what, date dropped, why. -->
