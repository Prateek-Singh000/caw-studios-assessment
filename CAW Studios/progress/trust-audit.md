# Trust Audit

## TRUST
* **Folder Structure & DB Tech:** I trust the folder list (`src/routes`, `src/models`) and the database tech (PostgreSQL/Prisma). This is highly factual, structural information that an AI can easily read from the file tree and `package.json`.

## VERIFY
* **Auth Enforcement:** The AI claims `requireAuth.js` enforces auth on requests. I need to verify *which* routes it is applied to. Is it applied globally, or per-route? If I build the Team Collaboration feature, I need to know exactly how to attach this middleware to the new `POST /teams` route.
* **Background Jobs:** The AI claims there is no background job system. I need to verify this because sending "Team Invitation Emails" asynchronously is a core requirement of our scenario. If there really is no job queue, I will have to architect one.

## SUSPICIOUS (Potential Hallucination)
* **User Roles:** The AI mentioned the User model has a `role` field with (Admin, User). Many starter kits do *not* have roles built-in. Because our Team Collaboration scenario requires strict role-based permissions, I am suspicious that the AI hallucinated this based on typical "SaaS starter kits." I must explicitly check the Prisma schema before writing any Role-Based Access Control (RBAC) code.

## VERIFICATION COMMANDS RUN
1. **Check for Express:**
   * Command: `cat package.json | grep express`
   * Result: `"express": "^4.18.2"` (VERIFIED: Project uses Express.js)

2. **Check for Auth Middleware:**
   * Command: `ls src/middlewares/requireAuth.js`
   * Result: File exists. (VERIFIED: Auth middleware is present)

3. **Check User Roles (The Suspicious Item):**
   * Command: `cat prisma/schema.prisma | grep role`
   * Result: No output. (BUSTED: The AI hallucinated the 'role' field. The User model only has id, email, password, and created_at. We will have to implement RBAC from scratch for the Team Collaboration scenario.)

## THE BREAK STEP: OVERCONFIDENT CLAIM BUSTED
* **The AI's Claim:** "The project uses PostgreSQL with Prisma ORM. Migrations are handled via Prisma CLI."
* **The Verification Command:** `cat package.json | grep -i -E '(prisma|sequelize)'`
* **The Actual Result:** The package.json contains `sequelize`, but absolutely no mention of `prisma`.
* **The Correction:** The codebase uses Sequelize ORM, not Prisma. The AI pattern-matched a trendy stack instead of reading the actual project dependencies. All future database prompts must explicitly instruct the AI to use Sequelize.

## THE FIX: CONSTRAINING THE AGENT
* **Why it failed:** Insufficient context. We asked a broad question, so the AI pattern-matched standard Node.js tutorials instead of reading our actual files.
* **The Corrected Prompt:** "Look strictly at `package.json` and the files in `src/models/`. Based ONLY on those files, what ORM is this project using? Do not guess."
* **Lesson Learned:** If the AI has to guess, it will. We must constrain it to specific files when asking factual architecture questions.
