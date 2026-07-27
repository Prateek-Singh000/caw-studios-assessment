import os
from fastapi import FastAPI

app = FastAPI()

# THE FIX: Dynamically read PORT from environment with fallback
PORT = int(os.getenv("PORT", "8000"))

@app.get("/health")
def health():
    return {"status": "healthy", "port": PORT}
