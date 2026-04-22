# OPERATIONS.md

## Required Repository Settings

Configure these in `jppkxm1979/only-AI-project`.

### Secrets

- `GEMINI_API_KEY`

### Branch protection for `main`

- require pull requests before merging
- require status checks to pass before merging
- require `Autonomous Verify / verify`
- restrict direct pushes to `main`

### Actions settings

- allow GitHub Actions to create pull requests if your repository settings currently block that
- keep scheduled workflows enabled

## Normal Autonomous Flow

1. `autonomous-propose.yml` creates a proposal PR
2. `autonomous-verify.yml` validates the result
3. `autonomous-merge.yml` merges green PRs after the waiting period
4. `autonomous-keepalive.yml` preserves repository activity if things go quiet

## External Guardian

`only-AI-project-manager` monitors this repository and can:

- re-enable key workflows
- close stale blocked autonomous PRs
- dispatch recovery workflows
