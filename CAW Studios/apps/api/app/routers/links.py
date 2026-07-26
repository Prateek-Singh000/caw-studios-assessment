from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
import random
import string
from app.database import Link
from app.schemas.link import LinkCreate, LinkResponse
from app.dependencies import get_db

router = APIRouter(prefix="/links", tags=["links"])

def generate_code(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

@router.post("/", response_model=LinkResponse)
async def create_link(link_in: LinkCreate, db: AsyncSession = Depends(get_db)):
    for _ in range(3): # Retry logic for collision prevention
        code = generate_code()
        new_link = Link(code=code, long_url=str(link_in.long_url))
        db.add(new_link)
        try:
            await db.commit()
            await db.refresh(new_link)
            return new_link
        except IntegrityError:
            await db.rollback()
            continue
    raise HTTPException(status_code=500, detail="Could not generate unique short code")
