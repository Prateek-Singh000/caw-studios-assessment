# Module 07: Blast Radius Analysis (Updated for RBAC & Departments)

## Part A: Company Accounts & RBAC (Extended Minimal Bridge)
| Artifact | Previous Status | New Status | Impact Reason |
|----------|----------------|------------|---------------|
| User data model | Modified (Major) | MAJOR+ | Must add `role` (`employee`, `manager`, `department_head`) and `department_id` columns. |
| Auth/JWT system | Unchanged (No Impact) | MAJOR | JWT must now embed `role` and `department_id` claims for authorization checks. |
| Booking flow (API)| Modified (Major) | MAJOR | Must add RBAC middleware: Employees restricted to self; Managers can book for department; Dept Heads can view department scope. |
| Booking flow (UI) | Modified (Major) | MAJOR | Conditional UI rendering based on JWT role (hiding/showing delegation fields). |
| Provider dashboard| Minor | UNCHANGED | Remains minor scope. |
| Search/listing | Unchanged | UNCHANGED | No change. |
| Payment/billing | Unchanged | UNCHANGED | No change. |
| Interface contracts| Major | MAJOR+ | Contracts must now define role-based error shapes (`403 Forbidden`). |

## Part B: Compressed Timeline (Revised 6-Day Scope)
* **MUST SHIP:**
  1. DB Schema with `role` and `department_id` extensions.
  2. JWT token generation carrying role claims.
  3. RBAC Middleware (`verifyRole`).
  4. Booking API supporting Manager delegation.
* **CUT (Deferred immediately to make room for RBAC):**
  1. Provider Profile & Rating View (Deferred entirely).
  2. Department Head cross-view analytics dashboard (Deferred to week 2).
