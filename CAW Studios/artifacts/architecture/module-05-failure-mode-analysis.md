# Failure Mode Analysis (FMA)

## 1. Dependency Inventory
| Dependency | Connection Method | Configured Timeout | Retry Behavior |
|---|---|---|---|
| Postgres | TCP via asyncpg (SQLAlchemy) | **?** (Default wait) | None |
| Redis (Rate Limiter) | TCP via aioredis | **?** (Default wait) | None |
| Datadog / Prometheus | HTTP Scrape (Pull) / UDP (Push) | N/A (Fire and forget) | None |
| DNS | OS Resolver | OS Default | OS Default |

*Analysis:* Our connection pools for Postgres and Redis currently rely on driver defaults. A slow network connection will cause our ASGI worker threads to hang indefinitely.

---

## 2. Failure Mode Table
| Dependency | Failure Mode | Probability | User Impact | Current Handling | Desired Handling |
|---|---|---|---|---|---|
| **Postgres** | Down (Connection Refused) | Medium | Complete Outage (500) | `sqlalchemy.exc.OperationalError` bubbles up to 500 | Return 503 (Service Unavailable) |
| **Postgres** | Slow Queries | High | Cascading timeout, API freezes | Waits indefinitely (Thread exhaustion) | Strict 2s query timeout -> 504 Gateway Timeout |
| **Postgres** | Partial (Read-Only Mode) | Low | GET works, POST fails with 500 | Unhandled 500 | Catch ReadOnlySqlTransaction, return 503 Service Unavailable |
| **Redis** | Down | Medium | Rate limiting fails | `aioredis.ConnectionError` bubbles up to 500 | **Fail-Open:** Catch error, log warning, bypass rate limiter, allow request |
| **Redis** | Stale Data | Low | Incorrect rate limit counting | Allowed by logic | Negligible impact for this service |
| **DNS** | Unreachable | Low | Cannot resolve DB/Cache hosts | Cryptic "Host not found" 500 | Monitor DNS resolution via node exporter |
| **Memory** | OOM (Out of Memory) | Low | Container Killed | Process dies | Add cgroup limits in Docker, alert at 85% RAM |
| **Disk** | Full | Low | Logger crashes | Silent application crash | Log rotation + Disk space alerts |
| **Network** | Partition | Medium | Cannot reach external services | Request hangs | Strict HTTP timeouts on all external calls |

*Risk Surface:* Out of 8 failure modes, 6 currently result in unhandled crashes, infinite hangs, or cryptic 500 errors.

---

## 3. Simulation Drills

### Drill 1: Database Stopped
**Action:** `docker stop postgres` -> Hit `GET /live` and `POST /api/links`.
**Expected:** Instant 500 error.
**Actual:** The API returned a 500 Internal Server Error, and structlog printed a massive stack trace for `psycopg2.OperationalError`. 
**Time to Notice:** Because we configured our HighErrorRate Prometheus alert in Module 4, this would page on-call within exactly 2 minutes (the `for: 2m` evaluation window).

### Drill 2: Impossibly Low Timeout (Redis/DB)
**Action:** Set SQLAlchemy `connect_args={'connect_timeout': 0.001}` and hit `POST /api/links`.
**Expected:** Immediate 504 or fast-fail.
**Actual:** Unhandled `TimeoutError` bubble up to a 500. We don't have graceful handling for DB timeouts—it crashes the request exactly like a hard-down database, rather than returning a clean "Too Busy" response.

| Simulation | Expected Behavior | Actual Behavior | Gap |
|---|---|---|---|
| `docker stop postgres` | Instant 500 | Instant 500 + Stack Trace | Working as designed, but returning 503 is cleaner than 500 |
| 1ms DB Timeout | Fast failure | Unhandled Exception -> 500 | Needs graceful `try/except` for TimeoutError to return 504 |
