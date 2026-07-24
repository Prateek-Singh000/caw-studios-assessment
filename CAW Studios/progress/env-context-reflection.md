# Environment Management Reflection

1. **Variables Change:** Almost all critical variables (DB URLs, API keys, log levels, secrets) change across Dev, Staging, and Prod. 
2. **Missing Configs:** Without validation, a missing `.env` file leads to cryptic downstream crashes (like `ECONNREFUSED` or undefined variable exceptions) rather than clear, actionable errors at startup.
