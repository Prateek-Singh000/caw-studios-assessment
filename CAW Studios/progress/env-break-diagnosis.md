# Environment Config Break Diagnosis

1. **Precedence Bug:** System environment variables (Docker `-e`) are being overridden by `.env` values, breaking the 12-Factor App rule that system environments must win.
2. **Missing Validation:** A critical variable was made `.optional()` in the schema, allowing the app to boot without it and risking a runtime crash later.
3. **Dangerous Default:** A connection string was given a `localhost` default, turning a loud configuration error into a silent runtime failure in production.
