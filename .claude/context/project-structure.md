---
created: 2026-03-29T14:39:41Z
last_updated: 2026-03-29T14:39:41Z
version: 1.0
author: Claude Code PM System
---

# Project Structure

```
spice-real-estate/
├── skill/                          # SOURCE OF TRUTH — edit here
│   ├── SKILL.md                    # Agent Skill entry point (cognitive loop)
│   ├── FORMULAS.md                 # Financial formulas + OPEX checklist
│   ├── BIASES.md                   # 12 cognitive biases + detection markers
│   ├── PERSONAS.md                 # 5 debate personas
│   ├── DECISION-CARD.md            # Vietnamese Decision Card template
│   ├── SOURCES-VN.md               # Vietnam market data sources
│   ├── EXAMPLES.md                 # 3 worked example scenarios
│   └── scripts/
│       ├── utils.py                # Shared JSON output + validation
│       ├── monte_carlo.py          # GBM price simulation (numpy)
│       ├── dcf_calculator.py       # NPV, IRR, cash-on-cash
│       ├── cashflow_proforma.py    # 10-year pro-forma + DSCR
│       ├── bayesian_updater.py     # Bayesian probability updating
│       └── test_all.py             # 14 automated tests
├── bin/
│   └── sync-skill.sh              # One-command sync: skill/ → .claude/skills/
├── docs/
│   └── PRD_SpiceRE.md             # Original detailed PRD (source material)
├── .claude/
│   ├── skills/spice-re/deciding-real-estate/  # RUNTIME copy (synced)
│   ├── prds/                       # CCPM PRD files
│   ├── epics/spice-re/             # CCPM epic + task files
│   ├── commands/                   # CCPM commands
│   ├── config/                     # CCPM config
│   └── context/                    # This directory
├── .spice_re/                      # Decision archive (gitignored)
│   └── decisions/
├── CLAUDE.md                       # Project instructions for Claude
├── .gitignore
└── README.md
```

## Key Conventions

- `skill/` = source of truth, `.claude/skills/` = runtime (synced via `bin/sync-skill.sh`)
- Python scripts use CLI args → JSON stdout pattern
- Reference files loaded on demand by SKILL.md (one per step max)
- `.spice_re/` is gitignored (user data)
