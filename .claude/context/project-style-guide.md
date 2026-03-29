---
created: 2026-03-29T14:39:41Z
last_updated: 2026-03-29T14:39:41Z
version: 1.0
author: Claude Code PM System
---

### Python Style
- PEP 8 compliance
- snake_case for functions and variables
- argparse for CLI interface
- All scripts share common pattern: argparse → validate → compute → json_output()
- Import utils via `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` then `from utils import ...`
- Dependencies: stdlib + numpy only (no pandas, no external packages)
- Error handling: json_error() for validation failures, try/except for computation errors

### Markdown Style
- Reference files use clear section headers for Claude to navigate
- Vietnamese for user-facing content (Decision Card, examples, bias reframes)
- English for technical content (SKILL.md instructions, frontmatter fields, code comments)
- Tables for structured data (formulas, biases, sources, indicators)

### Script Interface Contract
- Input: `--param value` CLI arguments via argparse
- Output: JSON to stdout with `"status": "success"` or `"status": "error"` + `"message"`
- Errors: stderr for warnings, non-zero exit code on failure
- Validation: every input validated before computation, invalid → json_error()

### SKILL.md Style
- Directive-style instructions (imperative: "Parse", "Run", "Load")
- Max ONE reference file loaded per step
- Script paths relative to skill directory
- Token budget: aim for <4k tokens body (5k limit)

### Naming Conventions
- Skill directory: kebab-case (`deciding-real-estate`)
- Python files: snake_case (`monte_carlo.py`)
- Reference files: UPPER-CASE with hyphens (`DECISION-CARD.md`)
- Git branches: `epic/{name}` for feature work

### Communication
- Call user "Chef"
- Respond in Vietnamese
- Suggest next steps after each response
