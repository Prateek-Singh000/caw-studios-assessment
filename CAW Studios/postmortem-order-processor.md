# Postmortem: OrderProcessor v2.14 Silent Order Drop Incident

## 1. Summary
On Wednesday, March 26, 2025, between 14:00 and 15:34 UTC, customers using the OrderProcessor checkout service received successful payment confirmations while their orders were silently dropped. Approximately 1,400 orders totaling $186,000 in revenue were affected. The incident was triggered by a routine configuration cleanup that removed a deprecated field. Because errors were swallowed into a broad try/except block, the service returned HTTP 200 while failing to persist orders to the database. The incident lasted 1 hour and 34 minutes before a manual platform rollback restored service.

## 2. Incident Timeline
*   **14:00** — OrderProcessor v2.14 is deployed to production, including a config change removing the deprecated `warehouse_routing` field.
*   **14:00–14:22** — Automated health checks pass; HTTP response codes are 200 OK.
*   **14:22** — Customers begin posting on social media regarding missing order confirmation emails; support tickets arrive in Slack.
*   **14:23–14:38** — Support flags the issue in `#cs-escalations`. The on-call engineer miscategorizes the report as an email delivery delay based on historical precedent, delaying investigation.
*   **14:38** — A second wave of tickets triggers active investigation by the on-call engineer.
*   **14:42** — Monitoring dashboards show normal HTTP 200 responses, latency, and resource utilization, masking the silent failure.
*   **14:55** — Direct database inspection reveals zero new orders written since 14:00.
*   **15:02** — The on-call engineer attempts an automated rollback.
*   **15:08** — Automated rollback fails because the deployment path script was never updated following an infrastructure migration four months prior.
*   **15:15** — The on-call engineer escalates to the platform team for manual intervention.
*   **15:34** — The platform team completes a manual rollback to v2.13. Orders resume processing.
*   **15:45** — Manual reprocessing of the 1,400 dropped orders begins using payment processor logs.
*   **16:02** — All dropped orders are reprocessed and confirmation emails are sent. Incident resolved.

## 3. Root Cause(s)
The root cause is a combination of silent failure handling in application code and an inadequate monitoring contract. 
1.  **Swallowed Exceptions:** The application code caught exceptions related to the missing configuration field in a broad try/except block, logged a DEBUG-level warning, and returned a success status (200 OK) instead of failing loudly or triggering a circuit breaker.
2.  **Shallow Health Checks:** The observability stack monitored infrastructure health (CPU, memory, HTTP 200 responses) rather than business logic outcomes (orders successfully written to the database per minute).

## 4. Contributing Factors
*   **Environment Drift:** Staging and production environments used differing configuration schemas, preventing the missing field error from being caught prior to production deployment.
*   **Stale Automation:** The automated rollback mechanism referenced a deprecated artifact path that broke during an infrastructure migration four months earlier.
*   **Escalation Friction:** The initial customer support escalation lacked automated telemetry correlation, leading the on-call rotation to misdiagnose the failure as an intermittent email delivery delay.

## 5. Action Items
*   **Item 1: Implement Business-Level Monitoring & Alerting**
    *   *Description:* Create a dedicated alerting rule that pages the on-call rotation if orders-per-minute drop to zero for more than 3 minutes.
    *   *Owner:* Observability Team Lead
    *   *Deadline:* 2 weeks (August 10, 2026)
    *   *Definition of Done:* Datadog dashboard widget tracking orders/minute is live, and an automated PagerDuty alert is verified via staging load-test simulation.
*   **Item 2: Refactor Error Handling & Circuit Breakers**
    *   *Description:* Eliminate broad try/except blocks around critical dependency mapping. Unhandled config schema errors must fail loudly, return 500 status codes, and halt order processing.
    *   *Owner:* Backend Core Team Lead
    *   *Deadline:* 1 month (August 24, 2026)
    *   *Definition of Done:* Code review completed, unit tests added verifying that missing configuration keys immediately fail the request.
*   **Item 3: Audit and Test Automated Rollback Pipelines**
    *   *Description:* Update rollback scripts to reflect current artifact paths and integrate automated rollback validation into the CI/CD pipeline.
    *   *Owner:* Platform Engineering Lead
    *   *Deadline:* 3 weeks (August 17, 2026)
    *   *Definition of Done:* Rollback script successfully tested in staging, and a monthly automated cron job is scheduled to verify rollback pipeline health.
*   **Item 4: Synchronize Staging and Production Config Schemas**
    *   *Description:* Ensure the staging environment mirrors production config structures to catch deprecation breaks before release.
    *   *Owner:* Infrastructure Team Lead
    *   *Deadline:* 2 weeks (August 10, 2026)
    *   *Definition of Done:* Staging config fully synced with production repository, and pre-deployment validation tests passing.

## 6. Lessons Learned
*   **What surprised us:** A service can be 100% "healthy" from an infrastructure standpoint (CPU, RAM, HTTP 200) while completely failing its core business purpose.
*   **What went well:** Once the database inspection confirmed the drop, manual log reprocessing and recovery by the platform team was executed methodically and recovered all 1,400 orders within an hour.
*   **What we would do differently tomorrow:** If this occurred tomorrow before action items are complete, the on-call engineer will check the database order count immediately upon receiving customer support escalation reports regarding missing emails, bypassing HTTP status code assumptions.
