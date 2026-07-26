from fastapi import FastAPI
from app.config import settings
from app.routers import links, redirect

app = FastAPI(title="URL Shortener API")

app.include_router(links.router)
app.include_router(redirect.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "port": settings.port}
