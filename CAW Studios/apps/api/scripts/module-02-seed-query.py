import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

# Import our models
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import Link

load_dotenv()
database_url = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql+asyncpg://").replace("postgresql://", "postgresql+asyncpg://")

async_engine = create_async_engine(database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

async def main():
    async with AsyncSessionLocal() as session:
        # Attempt to insert a link that might already exist
        new_link = Link(
            code="xYz123",
            long_url="https://cawstudios.com/careers"
        )
        session.add(new_link)
        
        try:
            await session.commit()
            print(f"Inserted code: {new_link.code}")
        except IntegrityError:
            await session.rollback()
            print("Notice: Short code 'xYz123' already exists! Database rejected duplicate.")
        
        # Query it back to ensure we can still read it
        stmt = select(Link).where(Link.code == "xYz123")
        result = await session.execute(stmt)
        fetched_link = result.scalar_one_or_none()
        
        if fetched_link:
            print(f"Selected code: {fetched_link.code}")
            print(f"Matched long_url: {fetched_link.long_url}")
        else:
            print("Failed to fetch link!")

if __name__ == "__main__":
    asyncio.run(main())
