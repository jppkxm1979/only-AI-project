# CHECKLIST.md

## only-AI-project setup

### 1. Add Gemini secret

Repository: `only-AI-project`

1. `Settings`
2. `Secrets and variables`
3. `Actions`
4. `Secrets`
5. `New repository secret`
6. Name: `GEMINI_API_KEY`
7. Value: your Google AI Studio Gemini API key

### 2. Protect main

Repository: `only-AI-project`

1. `Settings`
2. `Branches`
3. `Add branch protection rule`
4. Branch name pattern: `main`
5. Enable:
   - `Require a pull request before merging`
   - `Require status checks to pass before merging`
6. In required checks, add:
   - `Autonomous Verify / verify`
7. Save

### 3. Allow Actions if needed

Repository: `only-AI-project`

1. `Settings`
2. `Actions`
3. `General`
4. Under workflow permissions, allow workflows to create pull requests if your current setting blocks them

### 4. Test

1. Open `Actions`
2. Run `Autonomous Propose`
3. Run `Autonomous Keepalive`
4. Confirm workflows can queue and finish
