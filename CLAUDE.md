# CLAUDE.md

> Think carefully and implement the most concise solution that changes as little code as possible.

## Communication
- Call user "Chef", respond in Vietnamese, suggest next steps after each response.
- 
## Python

- Always create and use `.venv` virtual environment
- Always run `python` and `pip` from `.venv`, never from global
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Skill Development

SpiceRE Agent Skill lives in two locations:

| Location | Purpose |
|---|---|
| `skill/` | **Source of truth.** Edit files here. |
| `.claude/skills/spice-re/deciding-real-estate/` | **Runtime copy.** Claude Code reads from here. Do not edit directly. |

### Workflow

1. Edit markdown or Python files in `skill/`
2. Sync to runtime: `bash bin/sync-skill.sh`
3. Test: `cd .claude/skills/spice-re/deciding-real-estate && .venv/bin/python3 scripts/test_all.py`

### First-time .venv setup (runtime location only)

```bash
cd .claude/skills/spice-re/deciding-real-estate
python3 -m venv .venv
.venv/bin/pip install numpy
```

### File inventory

**Markdown:** SKILL.md, FORMULAS.md, BIASES.md, PERSONAS.md, DECISION-CARD.md, SOURCES-VN.md, EXAMPLES.md

**Scripts:** scripts/utils.py, scripts/monte_carlo.py, scripts/dcf_calculator.py, scripts/cashflow_proforma.py, scripts/bayesian_updater.py, scripts/test_all.py
