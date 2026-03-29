---
created: 2026-03-29T14:39:41Z
last_updated: 2026-03-29T14:39:41Z
version: 1.0
author: Claude Code PM System
---

# Technical Context

## Platform

- **Runtime:** Claude Code CLI (Anthropic Agent Skills standard)
- **Language:** Python 3.8+ (stdlib + numpy)
- **Framework:** None — no web framework, no database (v1 uses markdown files)

## Environment

- **Virtual env:** `.venv` at `.claude/skills/spice-re/deciding-real-estate/.venv/`
- **Dependencies:** numpy (Monte Carlo simulation only)

## Script Interface

- CLI args via argparse → JSON stdout
- Errors written to stderr
- Shared utilities in `utils.py`: `json_output()`, `json_error()`, `validate_positive()`, `validate_range()`, `validate_choice()`

## Agent Skills Architecture

3-level progressive disclosure:
1. **Level 1** — Frontmatter (~100 tokens): skill name, description, trigger conditions
2. **Level 2** — SKILL.md body (<5k tokens): cognitive loop, step-by-step instructions
3. **Level 3** — Reference files + scripts (on demand): loaded per-step, max one file per step

## Testing

- Custom `test_all.py` (subprocess-based, 14 test cases)
- No CI/CD yet
- Tests validate script interfaces via subprocess calls

## Sync

- rsync-based `bin/sync-skill.sh`
- Source: `skill/` → Target: `.claude/skills/spice-re/deciding-real-estate/`

## Repository

- GitHub: abc-elearning/spice-real-estate
- Branch: main (6 commits)
- Git workflow: feature branches per epic, merge to main
