# Module 07: Updated Execution Plan (RBAC Revision)

## 1. Preserved
* **DB-01 & API-01:** Base schema and provider availability endpoints.

## 2. Modified (Escalated Scope)
* **API-02 (`POST /api/bookings`):** Now requires RBAC middleware check. Validates that if `booked_for_email` is provided, the caller's role is `manager` or `department_head` within the same department.
* **Auth System:** Updated login route to sign JWT with `{ userId, role, departmentId }`.

## 3. Cut (Expanded to accommodate RBAC)
* **Provider Profile & Rating View:** Cut completely from the 6-day sprint to reclaim 8 hours for RBAC middleware implementation.
* **Email Notification Service:** Cut (previously decided).

## 4. Added (RBAC Tickets)
* **TICKET-RBAC-01:** Add `role` and `department_id` columns and seed test users for all 3 roles. (Size: S)
* **TICKET-RBAC-02:** Implement Express RBAC middleware to enforce delegation permissions. (Size: M)
