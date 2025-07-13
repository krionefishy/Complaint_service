from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db


async def get_db() -> AsyncSession:
    async with db.session() as session:
        yield session