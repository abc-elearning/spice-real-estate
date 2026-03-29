---
epic: spice-re
prd: .claude/prds/spice-re.md
mode: full
reviewer: claude
created: 2026-03-29T14:02:54Z
verdict: ready-with-warnings
critical_gaps: 0
warnings: 6
---

# Plan Review: spice-re

## Phase 0: Scope Challenge

### 0A. Existing Code Audit

| Sub-problem | Existing code | Reuse? | Gap |
|-------------|--------------|--------|-----|
| Agent Skill structure | `.claude/skills/` dir convention | ✅ Pattern | No existing RE skills — greenfield |
| Financial calculations | None in project | ❌ New | All 4 scripts from scratch |
| Bias detection | None in project | ❌ New | Prompt engineering + reference file |
| Debate engine | None in project | ❌ New | Prompt engineering + PERSONAS.md |
| Decision archiving | None in project | ❌ New | Simple markdown I/O |

No rebuild risk. 100% greenfield.

### 0B. Complexity Assessment

```
📐 COMPLEXITY CHECK
Files touched: 12 (all new)  |  New components: 4 (SKILL.md + 6 reference MDs + 4 scripts + archive)
Task count: 8 / parallel: 5/8  |  Effort: 10d (5d critical path)
Cross-epic conflicts: none
```

### 0C. PRD Alignment Quick Check

```
📋 PRD ALIGNMENT
MUST requirements: 8/8 mapped (100%)
Unmapped: none
NTH deferred: NTH-3 (Sensitivity), NTH-4 (User Profile)
NTH included: NTH-1 (Web Research), NTH-2 (Archive, partial)
```

### 0F. Completeness Check (Lake Score)

| Decision | Planned | Full option | Effort diff | Choice |
|----------|---------|------------|------------|--------|
| Script error handling | Basic argparse | Full input validation + ranges | <1.5x | Full ✅ |
| Test strategy | test_all.py in Phase 3 | Test per script + integration | <1.5x | Full ✅ |
| OPEX defaults | Hardcoded | Config-driven with override | ~2x | Planned ⬜ |
| Archive format | Plain markdown | Markdown + frontmatter index | <1.5x | Full ✅ |
| numpy fallback | Warning only | stdlib fallback in monte_carlo | <1.5x | Full ✅ |
| .venv setup | Not planned | Setup task with requirements | <1.5x | Full ✅ |

Lake Score: 5/6 (83%) decisions should choose complete option.

---

## Section 1: Architecture Review

### Architecture Diagram

```
User Query ("Should I buy this apartment?")
         │
         ▼
┌─────────────────────────────────────────────────────┐
│  ★ SKILL.md — Cognitive Loop Orchestrator (<5k tok) │
│                                                     │
│  Step 1: Perception ─── parse intent, extract attrs │
│  Step 2: State ──────── build models (markdown)     │
│  Step 3: Analysis ──┬── cat BIASES.md → scan        │
│                     ├── cat FORMULAS.md → reference  │
│                     └── cat SOURCES-VN.md → search   │
│  Step 4: Simulation ┬── python3 monte_carlo.py      │
│                     ├── python3 dcf_calculator.py    │
│                     └── python3 cashflow_proforma.py │
│  Step 5: Decision ──┬── cat PERSONAS.md → debate     │
│                     └── cat DECISION-CARD.md → gen   │
│  Step 6: Reflection ─── save to .spice_re/decisions/ │
└─────────────────────────────────────────────────────┘
         │
         ▼
   Decision Card (Vietnamese)
```

### ARCH-1: Context Window Pressure from Reference File Loading

```
🏗️ ARCH-1: Reference file loading may consume excessive context
Problem: SKILL.md Step 3-5 loads 4-5 reference files + parses 3-4 script JSON outputs.
  BIASES.md (~2k tokens) + FORMULAS.md (~1.5k) + SOURCES-VN.md (~1k) +
  PERSONAS.md (~2k) + DECISION-CARD.md (~1k) + 3-4 script outputs (~1k total)
  = ~9-10k tokens from skill resources alone.
  Add SKILL.md body (~4k) + user conversation context → could hit 20k+ tokens
  just from the skill machinery.
Impact: Crowds out conversation context. Claude may truncate earlier messages
  or produce compressed outputs. Especially problematic in multi-turn sessions.
Options:
  A) [Recommended] Selective loading — SKILL.md instructions should NOT load all
     reference files every time. Load BIASES.md only in Step 3, PERSONAS.md only
     in Step 5, etc. Never load all at once. — Effort: S, Risk: L
  B) Compress reference files — Cut each to <1k tokens. — Effort: M, Risk: M
     (may lose detection quality)
  C) Do nothing — Risk: degraded output quality in longer conversations
Recommend A because: minimal diff to plan, preserves reference quality, explicit
  loading is already the stated intent but should be emphasized as a HARD RULE
  in SKILL.md ("NEVER load more than one reference file per step").
```

### ARCH-2: Python .venv Requirement Missing from Plan

```
🏗️ ARCH-2: CLAUDE.md requires .venv but epic doesn't address it
Problem: CLAUDE.md specifies "Always create and use .venv virtual environment"
  and "Always run python and pip from .venv, never from global." Epic's 4 Python
  scripts (T4-T7) need numpy. No task creates .venv or installs numpy.
Impact: Scripts will fail on first invocation if run without .venv active.
  SKILL.md's bash invocations (`python3 scripts/monte_carlo.py`) may use system
  Python without numpy.
Options:
  A) [Recommended] Add .venv setup to T1 (SKILL.md task) or create T0. Include:
     - `python3 -m venv .claude/skills/spice-re/deciding-real-estate/.venv`
     - `.venv/bin/pip install numpy`
     - SKILL.md uses `.venv/bin/python3` in script invocations instead of bare `python3`
     — Effort: S, Risk: L
  B) Use shebang + runtime detection in scripts — each script checks for numpy
     and prints install instructions. — Effort: S, Risk: M (user friction)
  C) Do nothing — Risk: scripts fail at runtime
Recommend A because: explicit is better than clever. Hardcoding .venv/bin/python3
  in SKILL.md script invocations guarantees correct environment.
```

---

## Section 2: Failure Mode Analysis

### Failure Mode Registry

| Codepath/Script | What can fail | Handled? | Test? | User sees | Severity |
|----------------|---------------|----------|-------|-----------|----------|
| monte_carlo.py: numpy import | ImportError if numpy missing | Mentioned (fallback) | N | Script error in Claude output | Medium |
| monte_carlo.py: negative price | ValueError / nonsensical output | N | N | Silent wrong output | 🔴 Medium |
| dcf_calculator.py: IRR no convergence | Infinite loop or wrong value | Y (max iterations mentioned) | N | "IRR not calculable" | Low |
| dcf_calculator.py: zero discount rate | Division by zero in NPV | N | N | Script crash | 🔴 Medium |
| cashflow_proforma.py: zero rent | DSCR division by zero | N | N | Script crash | 🔴 Medium |
| cashflow_proforma.py: missing args | argparse error | Y (argparse default) | N | argparse help text | Low |
| bayesian_updater.py: prior=0 or prior=1 | Bayes theorem breaks (0 or undefined) | N | N | Wrong posterior | 🔴 Medium |
| SKILL.md: skill doesn't trigger | User RE query doesn't match | N | N | Skill not activated | Medium |
| SKILL.md: cat reference file fails | File not found (wrong path) | N | N | Error in Claude output | Medium |
| Web search: no results | batdongsan.com.vn blocked | N | N | Missing market context | Low |
| Archive: .spice_re/ doesn't exist | mkdir not run | Mentioned (lazy) | N | File write fails | Low |

**Critical gaps:** 4 input validation issues (negative price, zero discount, zero rent, prior boundaries) — all in scripts where wrong output is SILENT (no crash, just wrong numbers). This is worse than a crash because user trusts the output.

### FAIL-1: Script Input Validation

```
🏗️ FAIL-1: Scripts lack input validation for boundary/invalid inputs
Problem: monte_carlo.py, dcf_calculator.py, cashflow_proforma.py, bayesian_updater.py
  have no input validation beyond argparse type checking. Edge cases (price<=0,
  discount_rate=0, rent=0 with DSCR calc, prior=0|1) produce silent wrong output.
Impact: User receives mathematically incorrect results and makes decisions based
  on them. This is the highest-severity failure for a financial tool.
Options:
  A) [Recommended] Add validation block to each script: check value ranges, emit
     {"status":"error", "message":"..."} JSON for invalid inputs. Define ranges:
     price>0, rate∈[0,1], years∈[1,50], sims∈[100,100000], prior∈(0,1).
     — Effort: S, Risk: L
  B) Validate in SKILL.md instructions (tell Claude to check before invoking)
     — Effort: S, Risk: M (Claude may skip)
  C) Do nothing — Risk: silent wrong financial calculations
Recommend A because: defense in depth. Scripts are the last line of defense.
  Validation at the script level is more reliable than relying on prompt behavior.
```

---

## Section 3: Code Quality & DRY Review

### QUAL-1: Shared Script Utilities

```
🏗️ QUAL-1: 4 scripts will duplicate argparse boilerplate + JSON output pattern
Problem: All 4 scripts need: argparse setup, JSON output formatting, error
  handling pattern (try/except → status:error JSON), input validation. Each
  will implement this independently.
Impact: Inconsistent error formats between scripts. Bug fixes need 4x changes.
Options:
  A) [Recommended] Create scripts/utils.py with: parse_args() helper, json_output()
     helper, validate_range() helper. Each script imports from utils.
     — Effort: S, Risk: L
  B) Accept duplication — only 4 scripts, manageable.
     — Effort: 0, Risk: L
  C) Template generator — overkill for 4 files.
Recommend A because: DRY. 4 scripts × 3 patterns = 12 duplication points.
  utils.py is ~50 lines and eliminates all of them. Also makes adding new
  scripts in v2 trivial.
```

No other DRY violations (greenfield project). Naming conventions follow Python standard (snake_case files, PEP 8). Module structure is flat and appropriate for 4 scripts.

---

## Section 4: Test Strategy Review

### Test Coverage Map

| What's new | Happy path test? | Failure path test? | Edge case? | Test type |
|-----------|-----------------|-------------------|-----------|-----------|
| monte_carlo.py | T8 (test_all.py) | Not planned | Not planned | Automated |
| dcf_calculator.py | T8 | Not planned | Not planned | Automated |
| cashflow_proforma.py | T8 | Not planned | Not planned | Automated |
| bayesian_updater.py | T8 | Not planned | Not planned | Automated |
| SKILL.md trigger | T8 (3 queries manual) | Not planned | Not planned | Manual |
| Bias detection | Manual (5 scenarios) | Not planned | Not planned | Manual |
| Debate quality | Manual (5 outputs) | Not planned | Not planned | Manual |
| Decision Card completeness | T8 (parse check) | Not planned | Not planned | Manual |

### TEST-1: Test Strategy Needs Edge Cases

```
🏗️ TEST-1: test_all.py only covers happy paths
Problem: T8 spec says "verify JSON validity" and "test inputs." No mention of
  edge cases: zero values, negative inputs, extreme ranges (100 year projection,
  prior=0.001), missing optional args. For a financial tool, edge case testing
  is essential.
Impact: Silent bugs in boundary conditions → wrong financial advice.
Options:
  A) [Recommended] Expand test_all.py scope: 3 test cases per script —
     happy path, boundary inputs, invalid inputs. Verify both success JSON
     and error JSON. ~15 test cases total. — Effort: S, Risk: L
  B) Separate test file per script (test_monte_carlo.py etc.)
     — Effort: M, Risk: L (more files but better isolation)
  C) Happy paths only — Risk: silent boundary bugs
Recommend A because: single test_all.py with 15 cases is fast to run,
  easy to maintain, catches the critical boundary issues.
```

---

## Section 5: Performance & Resource Review

| Concern | Assessment | Action |
|---------|-----------|--------|
| Shell spawning for 4 scripts | 4 × ~100ms = ~400ms total | Acceptable |
| Monte Carlo 1000 × numpy | <1 second | Acceptable |
| Context window from reference files | ~9-10k tokens from skill resources (see ARCH-1) | ⚠️ Addressed in ARCH-1 |
| Parallel safety | Phase 2 scripts share no state | ✅ Safe |
| File I/O | Markdown read/write only, no loops | ✅ Fine |

No performance blockers. ARCH-1 (context pressure) is the only resource concern.

---

## Section 6: PRD Traceability Audit

| PRD Req | Epic maps to | Task(s) | Verification | Status |
|---------|-------------|---------|-------------|--------|
| FR-1: Cognitive Loop | §SKILL.md Cognitive Loop | T1 | Manual: 3 queries → 6 steps | ✅ |
| FR-2: Bias Detection | §BIASES.md + SKILL.md step 3 | T1, T2 | Manual: 5 biased inputs | ✅ |
| FR-3: Cash Flow Pro-forma | §cashflow_proforma.py | T6, T2 | Automated: known inputs | ✅ |
| FR-4: Monte Carlo | §monte_carlo.py | T4 | Automated: fixed seed | ✅ |
| FR-5: DCF Calculator | §dcf_calculator.py | T5 | Automated: Excel cross-val | ✅ |
| FR-6: Bayesian Updater | §bayesian_updater.py | T7 | Automated: known prior | ✅ |
| FR-7: Multi-Persona Debate | §PERSONAS.md + SKILL.md step 5 | T1, T3 | Manual: 5 debates | ✅ |
| FR-8: Decision Card | §DECISION-CARD.md + SKILL.md step 5 | T1, T3 | Manual: all sections | ✅ |
| NFR-1: Token Budget | §SKILL.md token budget | T1 | Automated: wc -w | ✅ |
| NFR-2: CLI + JSON | §Script Interface Contracts | T4-T7 | Automated: json.tool | ✅ |
| NFR-3: Reliability | §monte_carlo.py --seed | T4 | Automated: seed test | ✅ |
| NFR-4: Card Completeness | §DECISION-CARD.md template | T3, T8 | Manual: parse card | ✅ |
| NFR-5: Platform | All tasks: stdlib + numpy | All | Automated: import check | ✅ |
| NTH-1: Web Research | §SOURCES-VN.md + SKILL.md | T1, T3 | Manual: web search triggered | ✅ |
| NTH-2: Archive | §Data Storage + SKILL.md step 6 | T8 | Manual: card saved | ✅ |
| NTH-3: Sensitivity | Deferred | — | — | ⏭️ |
| NTH-4: User Profile | Deferred | — | — | ⏭️ |

**Coverage: 8/8 MUST (100%), 5/5 NFR (100%), 2/4 NTH included. 0 unmapped.**

---

## Required Outputs

### Existing Code Reuse

| Functionality | Existing code | Reused? | Recommendation |
|--------------|--------------|---------|----------------|
| Agent Skills structure | Anthropic convention | ✅ Pattern | Follow .claude/skills/ standard |
| Python venv | CLAUDE.md directive | ⚠️ Not addressed | Add to T1 or T0 (ARCH-2) |
| Financial formulas | docs/PRD_SpiceRE.md has formulas | ✅ Reference | Port formulas from original PRD |
| Bias catalog | docs/PRD_SpiceRE.md has 12 biases | ✅ Reference | Port bias table from original PRD |
| Persona definitions | docs/PRD_SpiceRE.md has 5 personas | ✅ Reference | Port personas from original PRD |
| Vietnam data sources | docs/PRD_SpiceRE.md has source table | ✅ Reference | Port source table from original PRD |

**Key insight:** docs/PRD_SpiceRE.md contains rich detail (formulas, biases, personas, sources, examples) that should be directly ported into reference files. T2 and T3 should explicitly reference this document as source material.

### NOT in Scope

| Deferred item | Reason |
|--------------|--------|
| NTH-3: Sensitivity analysis script | Claude handles prompt-based in v1 |
| NTH-4: User profile persistence | Full profile management deferred |
| SQLite decision database | Markdown archive sufficient for v1 |
| Location Intelligence toolkit | General web search guidance only |
| Reflection loop + prediction tracking | v2 feature |
| Additional scripts (sensitivity, scenario_builder, ev_calculator, risk_classifier) | Prompt-based in v1 |

### Failure Modes Registry (consolidated)

| # | Codepath | Failure | Severity | Status |
|---|---------|---------|----------|--------|
| 1 | monte_carlo.py: negative price | Silent wrong output | 🔴 Medium | Unhandled → FAIL-1 |
| 2 | dcf_calculator.py: discount=0 | Division by zero | 🔴 Medium | Unhandled → FAIL-1 |
| 3 | cashflow_proforma.py: rent=0 | DSCR division by zero | 🔴 Medium | Unhandled → FAIL-1 |
| 4 | bayesian_updater.py: prior=0|1 | Bayes undefined | 🔴 Medium | Unhandled → FAIL-1 |
| 5 | All scripts: numpy missing | ImportError | Medium | Partially handled (monte_carlo only) |
| 6 | SKILL.md: wrong file paths | cat fails | Medium | Unhandled |
| 7 | .spice_re/ missing | Write fails | Low | Mentioned, lazy mkdir |

**CRITICAL GAPS: 0** (no HIGH severity unhandled)
**WARNINGS: 4** (medium severity input validation, see FAIL-1)

### Unresolved Decisions

| Issue | Section | Recommended | Risk if unresolved |
|-------|---------|-------------|-------------------|
| ARCH-2: .venv setup for scripts | Architecture | Add venv setup to T1, use .venv/bin/python3 in SKILL.md | Scripts fail at runtime |
| FAIL-1: Input validation in scripts | Failure Modes | Validation block in each script | Silent wrong financial results |
| QUAL-1: Shared script utilities | Code Quality | Create scripts/utils.py | Inconsistent error handling across 4 scripts |
| TEST-1: Edge case testing | Test Strategy | Expand test_all.py to 15 cases | Boundary bugs undetected |
| ARCH-1: Reference file loading strategy | Architecture | Selective loading rule in SKILL.md | Context window crowding |
| Source material reuse | Existing Code | T2/T3 reference docs/PRD_SpiceRE.md | Reinventing content that already exists |

### Completion Summary

```
╔════════════════════════════════════════════════════════════╗
║              PLAN REVIEW — COMPLETION SUMMARY             ║
╠════════════════════════════════════════════════════════════╣
║ Epic:              spice-re                               ║
║ Mode:              FULL                                   ║
║ PRD coverage:      8/8 MUST requirements mapped (100%)    ║
╠════════════════════════════════════════════════════════════╣
║ Arch issues: 2    |  Failure modes: 7 (0 critical)        ║
║ Quality: 1        |  Test gaps: 1                         ║
║ Perf: 0           |  PRD trace: 0 unmapped                ║
╠════════════════════════════════════════════════════════════╣
║ Code reuse: 5     |  Deferred: 6   |  Unresolved: 6      ║
║ Lake Score: 5/6 (83%) decisions chose complete option     ║
╠════════════════════════════════════════════════════════════╣
║ VERDICT:  ⚠️ READY WITH WARNINGS                          ║
║ Reason:   0 critical gaps, 0 unmapped MUST, but 6         ║
║           warnings need addressing in epic update         ║
╚════════════════════════════════════════════════════════════╝
```
