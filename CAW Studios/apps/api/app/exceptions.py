from fastapi import Request
from fastapi.responses import JSONResponse
import structlog
from sqlalchemy.exc import OperationalError, ProgrammingError
import psycopg2.errors

logger = structlog.get_logger("url-shortener")

async def db_read_only_handler(request: Request, exc: ProgrammingError):
    # Check if the underlying error is a Read-Only transaction
    if isinstance(exc.orig, psycopg2.errors.ReadOnlySqlTransaction):
        logger.error("Database is in Read-Only mode. Write rejected.", path=request.url.path)
        return JSONResponse(
            status_code=503,
            content={"message": "Service is temporarily unable to process writes. Please try again later."},
        )
    # If it's a different programming error, raise it normally
    raise exc

async def db_operational_handler(request: Request, exc: OperationalError):
    logger.error("Database connection failed or timed out.", path=request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=503,
        content={"message": "Service is temporarily unavailable due to a backend connection issue."},
    )
