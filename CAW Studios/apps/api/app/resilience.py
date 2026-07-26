import asyncio
import random
import structlog
import pybreaker
from sqlalchemy.exc import OperationalError

logger = structlog.get_logger("url-shortener")

# Custom Circuit Breaker Listener for Logging
class BreakerLogger(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        logger.warning(
            "circuit_state_change",
            dependency=cb.name,
            old_state=old_state.name,
            new_state=new_state.name
        )

# Initialize Circuit Breakers
db_breaker = pybreaker.CircuitBreaker(
    fail_max=5,               # Trip after 5 failures
    reset_timeout=30,         # Half-open after 30 seconds
    listeners=[BreakerLogger()],
    name="postgres"
)

# Exponential Backoff with Jitter
async def retry_with_backoff(
    fn,
    *args,
    max_retries: int = 3,
    base_delay: float = 0.1,    # 100ms
    max_delay: float = 2.0,     # 2 seconds
    jitter: float = 0.05,       # +/- 50ms
    retryable_exceptions: tuple = (OperationalError, asyncio.TimeoutError, pybreaker.CircuitBreakerError)
):
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            return await fn(*args)
        except retryable_exceptions as e:
            last_error = e
            
            # Don't retry if the circuit is OPEN (Fail fast)
            if isinstance(e, pybreaker.CircuitBreakerError):
                logger.error("circuit_open_fallback", dependency="postgres", attempt=attempt+1)
                raise # Let the caller handle the 503 fallback
                
            if attempt == max_retries:
                break
                
            # Exponential backoff + Jitter calculation
            exponential_delay = min(base_delay * (2 ** attempt), max_delay)
            jitter_offset = random.uniform(-jitter, jitter)
            delay = max(0, exponential_delay + jitter_offset)
            
            logger.warning(
                "retry_attempt",
                attempt=attempt + 1,
                max_retries=max_retries,
                delay_ms=round(delay * 1000),
                error_type=type(e).__name__
            )
            await asyncio.sleep(delay)
            
        except Exception as e:
            # Non-retryable error, fail immediately
            raise
            
    raise last_error
