#!/usr/bin/env python3
"""Automated test runner for SpiceRE decision scripts.

Runs ~15 test cases across 4 scripts via subprocess. Uses .venv/bin/python3.
Run from the skill directory:
    .venv/bin/python3 scripts/test_all.py
"""

import json
import os
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PYTHON = os.path.join(SKILL_DIR, ".venv", "bin", "python3")
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")

passed = 0
failed = 0
results = []


def run_script(script_name, args):
    """Run a script via subprocess and return (returncode, stdout, stderr)."""
    cmd = [VENV_PYTHON, os.path.join(SCRIPTS_DIR, script_name)] + args
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def parse_json(stdout):
    """Parse JSON from stdout. Returns dict or None."""
    try:
        return json.loads(stdout)
    except (json.JSONDecodeError, ValueError):
        return None


def test(description, script, args, check_fn):
    """Run a single test case and report result."""
    global passed, failed
    try:
        rc, stdout, stderr = run_script(script, args)
        data = parse_json(stdout)
        ok, detail = check_fn(rc, data, stdout, stderr)
    except subprocess.TimeoutExpired:
        ok, detail = False, "TIMEOUT after 30s"
    except Exception as e:
        ok, detail = False, f"Exception: {e}"

    if ok:
        passed += 1
        status = "PASS"
    else:
        failed += 1
        status = "FAIL"

    results.append((status, description, detail))
    icon = "✅" if ok else "❌"
    print(f"  {icon} {description}")
    if not ok and detail:
        print(f"     → {detail}")


# ─────────────────────────────────────────────
# monte_carlo.py tests
# ─────────────────────────────────────────────
print("\n── monte_carlo.py ──")

test(
    "Happy path: seed 42, 1000 sims",
    "monte_carlo.py",
    ["--price", "1000000", "--growth", "0.05", "--std", "0.1",
     "--years", "5", "--sims", "1000", "--seed", "42"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success" and "p50" in data),
        f"status={data.get('status') if data else 'NO JSON'}, p50={'present' if data and 'p50' in data else 'missing'}"
    )
)

test(
    "Boundary: minimum sims=100",
    "monte_carlo.py",
    ["--price", "1000000", "--growth", "0.05", "--std", "0.1",
     "--years", "5", "--sims", "100", "--seed", "42"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success"),
        f"status={data.get('status') if data else 'NO JSON'}"
    )
)

test(
    "Invalid: negative price",
    "monte_carlo.py",
    ["--price", "-100", "--growth", "0.05", "--std", "0.1",
     "--years", "5", "--sims", "1000"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "error"),
        f"status={data.get('status') if data else 'NO JSON'}"
    )
)

# ─────────────────────────────────────────────
# dcf_calculator.py tests
# ─────────────────────────────────────────────
print("\n── dcf_calculator.py ──")

test(
    "Happy path: standard rental DCF",
    "dcf_calculator.py",
    ["--monthly_rent", "12000000", "--growth", "0.03", "--opex_ratio", "0.4",
     "--discount", "0.1", "--years", "10", "--initial", "3200000000"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success" and "npv" in data),
        f"status={data.get('status') if data else 'NO JSON'}, npv={data.get('npv') if data else 'N/A'}"
    )
)

test(
    "Boundary: very small discount rate 0.001",
    "dcf_calculator.py",
    ["--monthly_rent", "12000000", "--growth", "0.03", "--opex_ratio", "0.4",
     "--discount", "0.001", "--years", "10", "--initial", "3200000000"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success"),
        f"status={data.get('status') if data else 'NO JSON'}"
    )
)

test(
    "Invalid: discount=0",
    "dcf_calculator.py",
    ["--monthly_rent", "12000000", "--growth", "0.03", "--opex_ratio", "0.4",
     "--discount", "0", "--years", "10", "--initial", "3200000000"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "error"),
        f"status={data.get('status') if data else 'NO JSON'}"
    )
)

# ─────────────────────────────────────────────
# cashflow_proforma.py tests
# ─────────────────────────────────────────────
print("\n── cashflow_proforma.py ──")

test(
    "Happy path: positive cash flow",
    "cashflow_proforma.py",
    ["--price", "2800000000", "--rent", "15000000", "--area", "70",
     "--loan", "1120000000", "--interest", "0.09"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success"
         and "summary" in data),
        f"status={data.get('status') if data else 'NO JSON'}"
    )
)

test(
    "Happy path: negative cash flow, DSCR red flag",
    "cashflow_proforma.py",
    ["--price", "3200000000", "--rent", "13000000", "--area", "70",
     "--loan", "1600000000", "--interest", "0.09"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success"
         and data.get("summary", {}).get("dscr_flag") == "red"),
        f"dscr_flag={data.get('summary', {}).get('dscr_flag') if data else 'NO JSON'}"
    )
)

test(
    "Invalid: price=0",
    "cashflow_proforma.py",
    ["--price", "0", "--rent", "15000000", "--area", "70",
     "--loan", "0", "--interest", "0.09"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "error"),
        f"status={data.get('status') if data else 'NO JSON'}"
    )
)

test(
    "Edge: rent=0 with loan → DSCR=0, flag red",
    "cashflow_proforma.py",
    ["--price", "3000000000", "--rent", "0", "--area", "70",
     "--loan", "1500000000", "--interest", "0.09"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success"
         and data.get("summary", {}).get("dscr") == 0.0
         and data.get("summary", {}).get("dscr_flag") == "red"),
        f"dscr={data.get('summary', {}).get('dscr') if data else 'N/A'}, flag={data.get('summary', {}).get('dscr_flag') if data else 'N/A'}"
    )
)

# ─────────────────────────────────────────────
# bayesian_updater.py tests
# ─────────────────────────────────────────────
print("\n── bayesian_updater.py ──")

test(
    "Happy path: prior=0.5, strong positive → posterior ~0.857",
    "bayesian_updater.py",
    ["--prior", "0.5", "--evidence_strength", "strong",
     "--evidence_direction", "positive"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success"
         and abs(data.get("posterior", 0) - 0.857143) < 0.01),
        f"posterior={data.get('posterior') if data else 'NO JSON'}"
    )
)

test(
    "Invalid: prior=0 (must be strictly between 0 and 1)",
    "bayesian_updater.py",
    ["--prior", "0", "--evidence_strength", "strong",
     "--evidence_direction", "positive"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "error"),
        f"status={data.get('status') if data else 'NO JSON'}"
    )
)

test(
    "Overconfidence: prior=0.8 far from base_rate=0.5",
    "bayesian_updater.py",
    ["--prior", "0.8", "--evidence_strength", "weak",
     "--evidence_direction", "positive", "--base_rate", "0.5"],
    lambda rc, data, out, err: (
        (data is not None and data.get("status") == "success"
         and "overconfidence_warning" in data),
        f"warning={'present' if data and 'overconfidence_warning' in data else 'missing'}"
    )
)

# ─────────────────────────────────────────────
# Determinism test
# ─────────────────────────────────────────────
print("\n── Determinism ──")

det_args = ["--price", "1000000", "--growth", "0.05", "--std", "0.1",
            "--years", "5", "--sims", "1000", "--seed", "42"]
try:
    _, out1, _ = run_script("monte_carlo.py", det_args)
    _, out2, _ = run_script("monte_carlo.py", det_args)
    det_ok = out1 == out2 and out1 != ""
    det_detail = "identical" if det_ok else f"MISMATCH:\n  run1={out1[:80]}\n  run2={out2[:80]}"
except Exception as e:
    det_ok = False
    det_detail = f"Exception: {e}"

if det_ok:
    passed += 1
    icon = "✅"
else:
    failed += 1
    icon = "❌"
results.append(("PASS" if det_ok else "FAIL", "Determinism: seed=42 two runs identical", det_detail))
print(f"  {icon} Determinism: seed=42 two runs identical")
if not det_ok:
    print(f"     → {det_detail}")

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
total = passed + failed
print(f"\n{'='*40}")
print(f"Results: {passed}/{total} passed")
if failed > 0:
    print("\nFailed tests:")
    for status, desc, detail in results:
        if status == "FAIL":
            print(f"  ❌ {desc}: {detail}")

sys.exit(0 if failed == 0 else 1)
