# Postmortem: OrderProcessor v2.14 Silent Order Drop Incident (Blameless)

## 1. Summary
On Wednesday, March 26, 2025, between 14:00 and 15:34 UTC, customers using the OrderProcessor checkout service received successful payment confirmations while their orders were silently dropped. Approximately 1,400 orders totaling $186,000 in revenue were affected. The incident was triggered by a routine configuration cleanup that removed a deprecated field. Because application error handling caught the missing field in a broad try/except block, the service returned HTTP 200 OK while failing to persist orders to the database. The incident lasted 1 hour and 34 minutes before platform intervention restored service.

## 2. Incident Timeline
*   **14:00** — OrderProcessor v2.14 is deployed to production, including a configuration update removing the deprecated `warehouse_routing` field.
*   **14:00–14:22** — Automated health checks pass; HTTP response codes report 200 OK across all instances.
*   **14:22** — Customer reports emerge on social media regarding missing confirmation emails; support tickets accumulate in Slack.
*   **14:23–14:38** — Support flags the issue in `#cs-escalations`. The on-call responder misdiagnoses the report as an email delivery delay based on historical precedent, delaying active investigation.
*   **14:38** — A second wave of customer reports triggers active investigation by the on-call responder.
*   **14:42** — Monitoring dashboards show normal HTTP 200 responses, latency, and resource utilization, masking the silent failure.
*   **14:55** — Direct database inspection reveals zero new orders written since 14:00.
*   **15:02** — The on-call responder attempts an automated rollback.
*   **15:08** — Automated rollback fails because the deployment path script was not updated following an infrastructure migration four months prior.
*   **15:15** — The on-call responder escalates to the platform team for manual intervention.
*   **15:34** — The platform team completes a manual rollback to v2.13. Orders resume processing.
*   **15:45** — Manual reprocessing of the 1,400 dropped orders begins using payment processor logs.
*   **16:02** — All dropped orders are reprocessed and confirmation emails are sent. Incident resolved.

## 3. Root Cause(s)
This incident was made possible by two systemic architectural gaps:
1.  **Swallowed Exceptions and Silent Failures:** The application error-handling pattern caught configuration-related exceptions within a broad try/except block, logged a DEBUG-level warning, and returned a success status (200 OK) to the client instead of failing loudly or triggering a circuit breaker.
2.  **Shallow Health Checks:** The observability contract monitored infrastructure health metrics (CPU, memory, HTTP status codes) rather than business logic outcomes (orders successfully persisted to the database per minute).

## 4. Contributing Factors
*   **Environment Drift:** Staging and production environments used differing configuration schemas, preventing the missing field error from being caught prior to production deployment.
*   **Stale Deployment Automation:** The automated rollback mechanism referenced a deprecated artifact path that broke during an infrastructure migration four months earlier.
*   **Diagnostic Telemetry Gaps:** Initial customer support escalations lacked automated telemetry correlation, leading to misdiagnosis as an intermittent email delivery delay.

## 5. Action Items
*   **Item 1: Implement Business-Level Monitoring & Alerting**
    *   *Description:* Add an orders-per-minute metric and configure an automated alert that fires when the order rate drops to zero for more than 5 consecutive minutes.
    *   *Owner Role:* Observability Team Lead
    *   *Deadline:* August 10, 2026
    *   *Definition of Done:* Datadog dashboard widget tracking orders/minute is live, and an automated PagerDuty alert is verified via staging load-test simulation.
*   **Item 2: Refactor Error Handling & Circuit Breakers**
    *   *Description:* Replace broad try/except blocks around critical dependency mapping with fail-loud error propagation. Unhandled config schema errors must return HTTP 500 status codes and halt order processing.
    *   *Owner Role:* Backend Core Team Lead
    *   *Deadline:* August 24, 2026
    *   *Definition of Done:* Code review completed, and unit tests added verifying that missing configuration keys immediately fail the request.
*   **Item 3: Audit and Test Automated Rollback Pipelines**
    *   *Description:* Update rollback scripts to reflect current artifact paths and integrate automated rollback validation into the CI/CD pipeline.
    *   *Owner Role:* Platform Engineering Lead
    *   *Deadline:* August 17, 2026
    *   *Definition of Done:* Rollback script successfully tested in staging, and a monthly automated cron job is scheduled to verify rollback pipeline health.
*   **Item 4: Synchronize Staging and Production Config Schemas**
    *   *Description:* Enforce exact schema parity between staging and production configuration repositories to catch deprecation breaks before release.
    *   *Owner Role:* Infrastructure Team Lead
    *   *Deadline:* August 10, 2026
    *   *Definition of Done:* Staging config fully synced with production repository, and pre-deployment validation tests passing.

## 6. Lessons Learned
*   **What surprised us:** A service can report 100% infrastructure health (CPU, RAM, HTTP 200) while completely failing its core business purpose.
*   **What went well:** Once direct database inspection confirmed the drop, manual log reprocessing and recovery by the platform team was executed methodically and recovered all 1,400 orders within an hour.
*   **What we would do differently tomorrow:** If this occurred tomorrow before action items are complete, the on-call responder will check the database order count immediately upon receiving customer support escalation reports regarding missing emails, bypassing HTTP status code assumptions.
