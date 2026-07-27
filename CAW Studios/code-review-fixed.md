# Code Review: Add user summary generation

Hi! Thanks for putting this together. The function is beautifully self-contained—it takes inputs, processes data, and returns a result without any unexpected side effects, which makes it very easy to test.

I have one blocking bug that we need to fix before merging, alongside a few suggestions that will make the code much easier to read and maintain long-term.

### 🛑 Blocking Bug
*   **Division by Zero Risk:** On the line `d["average_account_age"] = total_age / cnt`, the program will crash with a `ZeroDivisionError` if the `users` list contains zero active users (`cnt` remains 0). 
    *   *Suggestion:* We should handle this edge case. Could we add a safeguard, like `d["average_account_age"] = total_age / cnt if cnt > 0 else 0`?

### 💡 Readability Suggestions (Non-blocking)
*   **Variable Naming:** Variables like `d`, `cnt`, and `cnt2` can be a bit tricky to decode months later. 
    *   *Suggestion:* Consider renaming `d` to `summary`, `cnt` to `active_count`, and `cnt2` to `inactive_count`. This makes the code instantly self-documenting.
*   **Iteration Pattern:** Python allows us to iterate directly over lists rather than using indices. 
    *   *Suggestion:* Changing `for i in range(len(users)): user = users[i]` to simply `for user in users:` is a bit cleaner and saves you a step!
*   **Nesting & Data Structures:** The nested `if/else` block for the health logic is doing a lot of heavy lifting. Also, using a dictionary is totally fine here, but a `dataclass` might provide better type hinting for other developers calling this function.
    *   *Suggestion:* If you have time, you might consider extracting the health logic into a small helper function or using early returns to flatten the nesting. Totally up to you!

Let me know once the division-by-zero is patched, and I will gladly approve!
