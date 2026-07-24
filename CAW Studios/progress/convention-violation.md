# Convention Violation: Middleware Error Format

## The Issue
* **Target:** `middlewares/requireRole.js`
* **Violation:** The middleware returns `{ "message": "Insufficient permissions" }` instead of the mandated `{ "error": { "code": "FORBIDDEN", "message": "..." } }` format.
* **Impact:** Downstream clients expecting the `error` object wrapper will break or fail to parse the response correctly.

## Why it Happened
* **Incomplete Context:** While `system-context.md` defined the error format, the Task 3 bundle didn't explicitly include a file that *used* the `error` wrapper to serve as a concrete "copy-paste" reference for the agent. The agent had the rules, but not the concrete example to clone.

## Fix
* Add `middlewares/requireAuth.js` to the "Files to read" list for Task 3, as it contains the correct error format implementation.
