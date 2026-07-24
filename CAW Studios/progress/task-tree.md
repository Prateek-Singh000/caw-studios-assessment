# Team Collaboration: Atomic Task Tree

## Critical Path: 
Team Model -> Team Creation API -> Team Membership Model -> RBAC Middleware -> Invitation Flow.

## Riskiest Task:
**Task 4: RBAC Middleware.** This is the "wiring" of the house. If the permission logic is flawed, the entire Team Collaboration feature is a security liability. It requires precise integration with `requireAuth.js`.

---

## Tasks
1. **Task: Create Team Model**
   - **Input:** `models/user.js`, `package.json` (Sequelize context).
   - **Output:** `models/team.js`.
   - **Acceptance Criteria:** `sequelize.define` correctly models Team; IDs are UUIDs; `ownerId` references User.
   - **Dependencies:** None.

2. **Task: Create Team Creation API**
   - **Input:** `models/team.js`, `middlewares/requireAuth.js`.
   - **Output:** `routes/teamRoutes.js`, `controllers/teamController.js`.
   - **Acceptance Criteria:** `POST /teams` returns 201; uses auth middleware; creates team with `ownerId` set to `req.user.id`.
   - **Dependencies:** Task 1.

3. **Task: Create Team Membership Model**
   - **Input:** `models/team.js`, `models/user.js`.
   - **Output:** `models/teamMember.js`.
   - **Acceptance Criteria:** Supports relationship between User and Team; includes a 'role' column (enum: 'OWNER', 'MEMBER').
   - **Dependencies:** Task 1.
