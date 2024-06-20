import os
from contextlib import asynccontextmanager

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

engine = create_async_engine(
    f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}"
    f":{os.environ['POSTGRES_PASSWORD']}"
    f"@{os.environ['POSTGRES_HOST']}:5432/"
    f"{os.environ['POSTGRES_DB']}",
    echo=False,
    future=True,
)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncSession:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
