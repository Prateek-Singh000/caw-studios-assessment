# Reflection: The GitLab Incident

**1. Monitoring vs. Verifying:**
Monitoring that a cron job triggered only verifies the *intent* to backup. Verifying a backup means actively automating a test restore to a sandbox environment and validating the data integrity. A backup doesn't actually exist until you have proven you can restore from it.

**2. Protecting the "Wrong Terminal":**
Relying on a human to double-check their terminal is an anti-pattern. Environment separation should be enforced by infrastructure:
*   **Visuals:** Production terminal prompts should be glaringly red.
*   **Access:** Engineers shouldn't have standing SSH access to production databases. It should require a temporary, audited "break-glass" credential.
*   **Immutability:** Production infrastructure should ideally be modified via CI/CD pipelines, not manual CLI commands.
