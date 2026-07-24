# TaskFlow API - Architecture & Extension Summary

## 1. Folder Structure
* `src/routes/`: Contains all Express router definitions, separated by resource.
* `src/controllers/`: Contains the business logic for each route.
* `src/models/`: Contains database schema definitions.
* `src/middlewares/`: Contains reusable request-interceptors (e.g., auth, logging).
* `src/db/`: Database connection setup and migration scripts.

## 2. Key Data Models
* **User:** `id`, `email`, `password_hash`, `role` (Admin, User), `created_at`.
* **Task:** `id`, `title`, `description`, `status` (Pending, Completed), `owner_id` (FK to User).

## 3. API Routes
* `POST /auth/register` - Creates a new user.
* `POST /auth/login` - Authenticates a user and returns a token.
* `GET /tasks` - Retrieves tasks for the authenticated user.
* `POST /tasks` - Creates a new task.

## 4. Authentication Mechanism
Authentication uses **JSON Web Tokens (JWT)**. Clients must send a Bearer token in the `Authorization` header. This is enforced by `src/middlewares/requireAuth.js`, which verifies the token and attaches the user object to `req.user`.

## 5. Database Setup
The project uses **PostgreSQL** with **Prisma ORM**. The connection string is loaded from the `.env` file via `DATABASE_URL`. Migrations are handled via Prisma CLI.

---

## Extension Points
* **New API Routes:** Add a new file in `src/routes/` (e.g., `teamRoutes.js`) and mount it in `src/app.js`.
* **New Data Models:** Define them in `prisma/schema.prisma` and run the migration command.
* **New Middleware:** Create a new file in `src/middlewares/` and apply it either globally in `app.js` or directly on specific routes.
* **Background Jobs:** Currently, there is **no queue or background job system** (like Redis/BullMQ) configured. Async work is just awaited directly in the controllers.
