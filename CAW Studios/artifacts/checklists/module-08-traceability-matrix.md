# Module 08: Requirements Traceability Matrix

| Req ID | Original Requirement (Module 1) | Current Status | Location / Artifact | Notes |
|--------|---------------------------------|----------------|---------------------|-------|
| REQ-01 | Users can view provider slots | Built | `GET /api/providers/:id/slots` | Fixed slotId alias bug in Mod 6. |
| REQ-02 | Users can book a slot | Built | `POST /api/bookings` | Enforces slot status change transaction. |
| REQ-03 | Providers can register | Cut / Deferred | N/A | Deferred to week 2 to save timeline for RBAC (Mod 7 adaptation). Seed data used for demo. |
| REQ-04 | Email notifications sent | Cut / Deferred | N/A | Manual UI confirmation suffices for investor demo. |
| REQ-05 | Corporate Company Accounts | Built (Adapted)| `POST /api/bookings` | Adapted via 'Extended Minimal Bridge'. Added delegation payload (`booked_for_email`). |
| REQ-06 | Role-Based Access Control | Built (Adapted)| Auth Middleware | Added late in Mod 7. Validates JWT role claims on booking endpoints. |
| REQ-07 | Advanced Provider Search | Lost | N/A | Requirement fell through the cracks during Mod 4 planning. Must add to post-launch backlog. |
