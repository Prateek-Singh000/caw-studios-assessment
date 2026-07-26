
---

## Runbook: Memory Leak / OOM CrashLoop

### Alert / Detection
- **Alert name:** `HighMemoryUtilization`
- **Symptoms:** Container restarts frequently (OOMKilled). Latency slowly increases over hours before a crash.
- **Signal:** Prometheus query `container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.85`.

### Diagnosis
**Step 1: Check Memory Stats**
`docker stats --no-stream`
- If problem: Memory usage is > 85% and climbing.

### Fix
**Step 1: Restart Container (Mitigation)**
`docker compose restart api`
- Expected output: Service restarts, memory drops back to baseline.
- **Follow-up:** Check application code for unbounded global dictionaries, unclosed DB connections, or unpaginated queries.

---

## Runbook: Configuration Drift (ClickOps)

### Alert / Detection
- **Alert name:** `ConfigMismatch` (Detected during deployment pipeline).
- **Symptoms:** Application behaves differently than expected despite no recent code changes.

### Diagnosis
**Step 1: Compare Environment Variables**
Check the platform dashboard environment variables against the GitHub Actions secrets or `.env.example`.

### Fix
**Step 1: Re-sync Configuration via Pipeline**
Never change variables in the UI. Update the secret in GitHub Actions, then trigger a manual pipeline run to re-deploy the service with the correct configuration.
