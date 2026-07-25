## Title: API-02: POST /api/bookings - Create Booking [AI-Ready]

**Context (Why):** 
This is the core transaction in SkillSwap Slice 1. A user selects a slot and finalizes the intent to book.

**Scope (What):** 
Create a POST endpoint in `src/routes/bookingRoutes.js` that creates a record in the `bookings` table and updates the `time_slots` table status to 'booked' atomically.

**Interface Contract:**
* **Request:** JSON `{ "time_slot_id": "uuid", "user_email": "string (valid email format)" }`
* **Success:** `201 Created`, JSON `{ "booking_id": "uuid (returned from INSERT)", "status": "confirmed" }`
* **Errors:**
  * `400 Bad Request` -> `{ "error": "time_slot_id and valid user_email are required" }` (Single string error)
  * `404 Not Found` -> `{ "error": "time_slot_id not found" }`
  * `409 Conflict` -> `{ "error": "slot is already booked" }`
  * `500 Server Error` -> `{ "error": "Internal server error" }` (Do NOT leak stack traces)

**Acceptance Criteria:**
- [ ] POST with valid payload returns 201 and valid UUID.
- [ ] DB verify: The slot's status is changed to 'booked'.
- [ ] POSTing to an already 'booked' slot returns 409.
- [ ] Missing payload fields returns 400.
- [ ] Invalid email format returns 400.

**Constraints:**
- **Global Standards:** Apply existing Express middleware for Rate Limiting and standard Winston JSON logging.
- **Security:** Use parameterized queries to prevent SQL injection on `user_email`. Endpoint is public (no JWT required for Slice 1).
- **Idempotency:** If `user_email` already has an active booking for this `time_slot_id`, return `200 OK` with existing `booking_id` instead of failing.
- **Database:** Import the connection pool from `src/config/database.js`. Wrap INSERT/UPDATE in a `BEGIN;` ... `COMMIT;` transaction.

**Anti-Scope:**
- No email dispatch logic.
- No payment processing.
