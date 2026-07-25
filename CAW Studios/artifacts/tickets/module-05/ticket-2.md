## Title: API-01: GET /api/providers & /api/providers/:id/slots

**Context (Why):** 
Allows the frontend to render the initial browse experience and time slot selection for the core booking flow.

**Scope (What):** 
Create two Express.js GET routes in `src/routes/providerRoutes.js` that fetch data from the Postgres database.

**Interface Contract:**
* `GET /api/providers` -> `200 OK`, JSON array: `[{ "id": "uuid", "name": "string", "category": "string" }]`
* `GET /api/providers/:id/slots` -> `200 OK`, JSON array of slots where status='available'.
* Invalid ID -> `404 Not Found`, JSON: `{ "error": "Provider not found" }`

**Acceptance Criteria:**
- [ ] `GET /api/providers` returns exactly 3 items.
- [ ] `GET /api/providers/123-uuid/slots` returns only 'available' slots.
- [ ] `GET /api/providers/invalid-id/slots` returns 404.

**Constraints:**
- Use Node.js, Express v4, and the `pg` (node-postgres) driver.
- Query using parameterized SQL to prevent injection.

**Anti-Scope:**
- No pagination, search, or filtering query parameters.
- No sorting (default DB order is fine).
