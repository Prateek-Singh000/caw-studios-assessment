# Docker Break Diagnosis

1. **Slow Builds:** Caused by cache invalidation. Putting `COPY . .` before `RUN npm install` means any source code change busts the dependency cache.
2. **Sensitive Data Leaks:** Caused by a missing `.dockerignore` file. `COPY . .` blindly copies local secrets, `.git` history, and local `node_modules` into the container.
