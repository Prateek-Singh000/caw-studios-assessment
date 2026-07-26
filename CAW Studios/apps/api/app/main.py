import time
import uuid
import structlog
from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from app.logger import configure_logger
from app.routers import links, redirect
from app.database import engine
from app import models

# Initialize structured logger
configure_logger()
logger = structlog.get_logger("url-shortener")

# Initialize Metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'path', 'status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP request duration in seconds',
    ['method', 'path']
)

# Ensure DB tables are created (Temporary for demo)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

@app.middleware("http")
async def observe_request(request: Request, call_next):
    # 1. Structured Logging: Inject Request ID
    req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=req_id, method=request.method, path=request.url.path)
    
    # 2. Metrics: Start Timer
    start_time = time.time()
    
    logger.info("Request started")
    try:
        response = await call_next(request)
        status_code = response.status_code
        logger.info("Request completed", status=status_code)
    except Exception as e:
        status_code = 500
        logger.error("Request failed with unhandled exception", exc_info=e, status=status_code)
        raise e
    finally:
        # 3. Metrics: Record Data
        duration = time.time() - start_time
        REQUEST_COUNT.labels(method=request.method, path=request.url.path, status=status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, path=request.url.path).observe(duration)
        
    return response

# Metrics Endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

from app.exceptions import db_read_only_handler, db_operational_handler
from sqlalchemy.exc import OperationalError, ProgrammingError

app.add_exception_handler(ProgrammingError, db_read_only_handler)
app.add_exception_handler(OperationalError, db_operational_handler)

# Include Routers
app.include_router(links.router)
app.include_router(redirect.router)
