from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import Link
from app.dependencies import get_db

router = APIRouter(tags=["redirect"])

@router.get("/r/{code}")
async def redirect_to_long_url(code: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Link).where(Link.code == code)
    result = await db.execute(stmt)
    link = result.scalar_one_or_none()
    
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
        
    return RedirectResponse(url=link.long_url, status_code=301)
