from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from app.core.db import engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
