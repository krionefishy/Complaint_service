from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import text
from app.core.sqlalchemy_base import Base
import logging


class Database:
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.Base = Base
        self.logger = logging.getLogger("Database")
        self.metadata = self.Base.metadata

    async def connect(self, db_url: str):
        self.engine = create_async_engine(
            url=db_url,
            echo=True
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)
    
        async with self.session() as session:
            await session.execute(text("SELECT 1"))
            self.logger.info("Database connected successfully")


    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()
            self.logger.info("Database connection closed")
    
    def session(self) -> AsyncSession:
        if not self.session_factory:
            raise RuntimeError("Database is not connected")
        return self.session_factory()



db = Database()