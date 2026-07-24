# Decomposition Bug: Conflicting Assumptions

## The Discrepancy
* **Task 1 State:** Created `Team` model with `ownerId` (1:1 ownership logic).
* **Task 2 Agent Output:** The agent generated controller code that performs `TeamMember.findAll({ where: { role: 'member' } })`.
* **The Conflict:** The `TeamMember` model and table were never created in Task 1. The agent assumed a Many-to-Many membership schema for a Team app, despite Task 1 only providing an `ownerId`.

## Cause
* **Decomposition Bug:** I failed to account for the "Membership" requirement in the initial Task Tree. I assumed a simple owner-based model but then asked for "Team Collaboration" in the prompt for Task 2. The agent pattern-matched the "Collaboration" requirement and assumed the necessary join table existed.

## Lesson
* **Architecture-First:** When building interconnected features, the data model *must* be fully defined and locked before any controller logic is generated. I should have made Task 2 "Create Team Membership Model" rather than "Create Team API."
