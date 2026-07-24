# Interface Contract: Team Foundation (Task 1 -> Task 2)

## Upstream (Task 1) Produces:
- **Table:** `Teams` (columns: `id` [UUID], `name`, `description`, `ownerId`)
- **Table:** `TeamMembers` (columns: `id` [UUID], `teamId` [FK], `userId` [FK], `role` [ENUM: 'admin', 'member'])
- **Behavior:** When a Team is created, the owner is automatically added to `TeamMembers` with the role 'admin'.

## Downstream (Task 2) Consumes:
- **Requirement:** Expects `TeamMembers` table to exist.
- **Requirement:** Expects `role` column to contain values 'admin' and 'member'.
- **Requirement:** Expects foreign key relationship `userId` -> `Users.id` to be indexed.
