# AI Delegation Strategy

**Decision:** Option B (Task-by-Task)

**Reasoning:**
1. **Compounding Errors:** The Team Collaboration scenario has strict constraints (role enforcement, secure invite flows). If the AI hallucinates a data model in Step 1, doing this task-by-task lets me catch it before it builds the endpoints, UI, and audit logs on top of that broken model.
2. **Reviewability:** Reviewing a 30-line diff ensures I can actually verify the security constraints. Reviewing a 500-line diff across 12 files guarantees my eyes will glaze over, and I will accidentally approve a security vulnerability.
3. **Context Management:** We are in an unfamiliar codebase. By feeding the AI one task at a time, I can provide the exact, specific context it needs for that specific task, rather than overwhelming it with the entire product spec.
