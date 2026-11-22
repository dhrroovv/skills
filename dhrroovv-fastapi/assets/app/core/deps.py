from typing import Annotated

from app.core.db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[AsyncSession, Depends(get_session)]
