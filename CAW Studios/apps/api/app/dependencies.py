from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql+asyncpg://").replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
