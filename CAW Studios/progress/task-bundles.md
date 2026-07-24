# Task Bundles

## Task 1: Create Team & TeamMember Models
- **Files to read:** 
  1. `models/user.js` (Reason: Pattern for associations and Sequelize exports).
  2. `migrations/001-create-users.js` (Reason: Pattern for table creation).
- **Files to modify:** None.
- **Output:** `models/team.js`, `models/teamMember.js`, new migration file.

## Task 2: Create Team Creation API
- **Files to read:**
  1. `controllers/projectController.js` (Reason: Shows standard controller structure).
  2. `middlewares/requireAuth.js` (Reason: Must use this for route protection).
  3. `models/team.js` (Reason: Model reference).
- **Files to modify:** `routes/index.js` (to mount team routes).
- **Output:** `routes/teamRoutes.js`, `controllers/teamController.js`.

## Task 3: RBAC Middleware
- **Files to read:**
  1. `middlewares/requireAuth.js` (Reason: Base auth logic).
  2. `models/teamMember.js` (Reason: Needed to check user role).
- **Files to modify:** None.
- **Output:** `middlewares/requireRole.js`.
