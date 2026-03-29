"""Discounted Cash Flow calculator for rental property investment.

Computes NPV, IRR (bisection method), cash-on-cash return, and equity
multiple from rental income streams. Uses stdlib math only.
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import json_output, json_error, validate_positive, validate_range


def build_cash_flows(monthly_rent, growth, opex_ratio, years, annual_debt_service):
    """Build annual net cash flows array for years 1..years."""
    cash_flows = []
    for y in range(1, years + 1):
        gross = monthly_rent * 12 * (1 + growth) ** y
        net = gross * (1 - opex_ratio) - annual_debt_service
        cash_flows.append(net)
    return cash_flows


def compute_npv(cash_flows, discount, equity):
    """NPV = sum(cf_t / (1+discount)^t) - equity."""
    pv = sum(cf / (1 + discount) ** t for t, cf in enumerate(cash_flows, start=1))
    return pv - equity


def npv_at_rate(cash_flows, rate, equity):
    """NPV at a given rate, used for IRR bisection."""
    if rate <= -1:
        return float("inf")
    pv = sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows, start=1))
    return pv - equity


def compute_irr(cash_flows, equity, lo=-0.5, hi=2.0, max_iter=1000, tol=1e-6):
    """Find IRR via bisection method. Returns (irr, note) tuple."""
    npv_lo = npv_at_rate(cash_flows, lo, equity)
    npv_hi = npv_at_rate(cash_flows, hi, equity)

    # Need sign change for bisection
    if npv_lo * npv_hi > 0:
        return None, "IRR could not be determined"

    for _ in range(max_iter):
        mid = (lo + hi) / 2
        npv_mid = npv_at_rate(cash_flows, mid, equity)

        if abs(npv_mid) < tol:
            return mid, None

        if npv_lo * npv_mid < 0:
            hi = mid
            npv_hi = npv_mid
        else:
            lo = mid
            npv_lo = npv_mid

    return None, "IRR could not be determined"


def main():
    parser = argparse.ArgumentParser(description="DCF calculator for rental property")
    parser.add_argument("--monthly_rent", type=float, required=True)
    parser.add_argument("--growth", type=float, required=True)
    parser.add_argument("--opex_ratio", type=float, required=True)
    parser.add_argument("--discount", type=float, required=True)
    parser.add_argument("--years", type=int, required=True)
    parser.add_argument("--initial", type=float, required=True)
    parser.add_argument("--loan", type=float, default=0.0)
    parser.add_argument("--rate", type=float, default=0.0)
    args = parser.parse_args()

    # Validation
    if args.monthly_rent < 0:
        json_error("monthly_rent must be >= 0")
    validate_positive("discount", args.discount)
    validate_range("years", args.years, 1, 50)
    validate_positive("initial", args.initial)
    validate_range("opex_ratio", args.opex_ratio, 0, 1)

    # Derived values
    annual_debt_service = args.loan * args.rate
    equity = args.initial - args.loan

    if equity <= 0:
        json_error("equity (initial - loan) must be positive")

    # Build cash flows
    cash_flows = build_cash_flows(
        args.monthly_rent, args.growth, args.opex_ratio, args.years, annual_debt_service
    )

    # NPV
    npv = compute_npv(cash_flows, args.discount, equity)

    # IRR
    irr, irr_note = compute_irr(cash_flows, equity)

    # Cash-on-cash return (year 1 CF / equity)
    cash_on_cash = cash_flows[0] / equity

    # Terminal value = last year CF / discount (perpetuity approximation)
    terminal_value = cash_flows[-1] / args.discount
    sum_all_cf = sum(cash_flows)
    equity_multiple = (sum_all_cf + terminal_value) / equity

    # Build result
    result = {
        "npv": round(npv, 2),
        "irr": round(irr, 6) if irr is not None else None,
        "cash_on_cash": round(cash_on_cash, 4),
        "equity_multiple": round(equity_multiple, 4),
    }
    if irr_note:
        result["irr_note"] = irr_note

    json_output(**result)


if __name__ == "__main__":
    main()
