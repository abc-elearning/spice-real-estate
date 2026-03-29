---
created: 2026-03-29T14:39:41Z
last_updated: 2026-03-29T14:39:41Z
version: 1.0
author: Claude Code PM System
---

# System Patterns

### Cognitive Loop Pattern

6-step sequential processing: Perception → State Modeling → Analysis → Simulation → Decision → Reflection. Each step has specific inputs/outputs and reference file dependencies.

### Script Interface Pattern

All Python scripts follow: argparse CLI → validate inputs → compute → `json_output()`. Shared `utils.py` provides `json_output()`, `json_error()`, `validate_positive()`, `validate_range()`, `validate_choice()`.

### Reference File Loading Pattern

SKILL.md uses `cat` commands to load reference files on demand. HARD RULE: max one reference file per step to prevent context window crowding.

### Adversarial Debate Pattern

5 personas with conflicting viewpoints debate each decision. Tensions between personas reveal hidden risks and assumptions.

### Decision Card Pattern

Structured output template (Vietnamese) with: situation, framework, bias alerts, scenarios (P10/P50/P90), debate summary, recommendation + confidence %, next steps, disclaimer.

### Source of Truth Pattern

`skill/` (root) → `bin/sync-skill.sh` → `.claude/skills/` (runtime). Development edits at root, sync to runtime location.
