# CI/CD Break Diagnosis

1. **Secret Leak:** A debug step (like `printenv` or `echo`) was added that dumped unmasked credentials into the plaintext logs.
2. **Pipeline Slowdown:** The cache path or key is misconfigured, causing a 100% cache miss rate and forcing a full dependency download on every run.
3. **Unintended Deployments:** The Docker build/push step is missing an `if: github.ref == 'refs/heads/main'` condition, causing feature branches to pollute the registry.
