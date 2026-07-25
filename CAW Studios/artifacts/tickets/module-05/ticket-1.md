## Title: DB-01: Schema and Seed Hardcoded Providers [AI-Ready]

**Context (Why):** 
To support Slice 1 (the demand-first booking flow), we need the underlying database tables and 3 hardcoded providers to render the UI without building the supply-side registration yet.

**Scope (What):** 
Create two raw SQL files: one migration file (`migrations/001_initial_schema.sql`) for creating tables, and one seed file (`seeds/001_hardcoded_providers.sql`) containing exactly 3 providers and 9 time slots (3 per provider).

**Interface Contract (Data Shapes):**
* `providers` table: `id` (UUID, PK), `name` (VARCHAR 255), `category` (VARCHAR 255).
* `time_slots` table: `id` (UUID, PK), `provider_id` (UUID, FK), `start_time` (TIMESTAMPTZ), `status` (VARCHAR 50, default 'available').
* `bookings` table: `id` (UUID, PK), `time_slot_id` (UUID, FK), `user_email` (VARCHAR 255), `created_at` (TIMESTAMPTZ).

**Acceptance Criteria (Testable Conditions):**
- [ ] `psql -f migrations/001_initial_schema.sql` executes without error.
- [ ] `psql -f seeds/001_hardcoded_providers.sql` executes without error.
- [ ] `SELECT COUNT(*) FROM providers;` returns exactly 3.
- [ ] `SELECT COUNT(*) FROM time_slots;` returns exactly 9.

**Constraints (Rules to Follow):**
- Use raw PostgreSQL syntax (no ORM syntax).
- All Primary Keys MUST use `gen_random_uuid()`.
- Enforce Foreign Key constraints with `ON DELETE CASCADE`.

**Anti-Scope (What NOT to Build):**
- No application code or ORM models (SQL files only).
- No user table (demand-side is anonymous for now).
- No index optimization (not needed for MVP data volumes).
