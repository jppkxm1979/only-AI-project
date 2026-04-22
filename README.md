# only-AI-project
this repository is made by only AI, see what AI can do, and see how they evolve repo

This repository is intentionally topicless. It may drift into experiments, small tools, strange docs, tiny apps, agent notes, or anything else that remains small and safe.

## Autonomous Setup

This repository is configured to evolve in a conservative, fail-closed way.

- `autonomous-propose.yml` runs on a daily schedule and then applies a `1 in 10` random gate.
- If an autonomous PR is already open, no new proposal is created.
- Gemini model selection is dynamic and falls back across multiple Flash-family candidates.
- The AI may only change a very small, approved subset of repository paths.
- The AI may not modify GitHub workflows, automation scripts, or hidden repository infrastructure.
- The AI may write and revise agent-facing files such as `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `MODELS.md`, and `IDEAS.md`.
- The preferred autonomous build zone is `development/`.
- Control-plane files stay frozen, while `development/` can grow broadly under rule-based scanning.
- Network access, secret-like strings, shell scripts, executable artifacts, destructive commands, and process-spawning patterns are blocked by safety scanning.
- Every proposal must pass repository verification before a PR is opened.
- Merge is delayed by at least 24 hours and only happens if GitHub checks are green.
- If a managed PR stays broken or unmergeable for too long, automation closes it so the system can recover and continue.
- If the repository stays inactive for too long, automation creates a keepalive PR to preserve activity.

## Required Secret

- `GEMINI_API_KEY`

Repository setup checklist: [OPERATIONS.md](C:/Users/Administrator/Documents/GitHub/only-AI-project/OPERATIONS.md)

## Recommended Repository Settings

- Protect `main`
- Require pull requests before merging
- Require status checks to pass before merging
- Require the `Autonomous Verify / verify` check
- Restrict direct pushes to `main`

## Safety Model

This setup is not "100% safe." It is designed to fail closed:

- model lookup failure: skip safely
- model deprecation or 404: try fallback models, otherwise skip safely
- generation failure: skip safely
- invalid patch: skip safely
- blocked path touched: stop without PR
- verification failure: stop without PR
- open autonomous PR already exists: stop without new proposal
- PR too new or not green: stop without merge
- stale broken autonomous PR: close and recover
- long inactivity: create keepalive PR
