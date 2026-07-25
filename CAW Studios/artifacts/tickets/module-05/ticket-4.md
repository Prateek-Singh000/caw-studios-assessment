## Title: API-03: POST /api/providers - Provider Registration

**Context (Why):** 
Initiates Slice 2 (Supply MVP). Replaces our hardcoded seeds with real user-generated provider profiles.

**Scope (What):** 
Create a POST endpoint that validates provider details, hashes their password, and creates a record in the `providers` table.

**Interface Contract:**
* **Request:** JSON `{ "name": "string", "email": "string", "password": "string", "category": "string" }`
* **Success:** `201 Created`, JSON `{ "provider_id": "uuid" }` (do NOT return password hash).
* **Errors:** `400 Bad Request` (missing fields), `409 Conflict` (email already exists).

**Acceptance Criteria:**
- [ ] POST with valid payload returns 201.
- [ ] Duplicate email returns 409.
- [ ] Password is hashed in DB using bcrypt.

**Constraints:**
- Use `bcryptjs` for hashing (min 10 rounds).

**Anti-Scope:**
- No JWT/Session generation on registration (force them to log in separately).
- No automated time slot generation in this ticket.
