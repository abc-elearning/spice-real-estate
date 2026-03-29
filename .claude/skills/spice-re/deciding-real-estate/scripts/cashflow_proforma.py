"""10-Year Cash Flow Pro-forma for Vietnamese Real Estate.

Computes realistic net cash flow with all OPEX items that Vietnamese investors
typically underestimate. DSCR < 1.0 detection is a critical safety feature.

Usage:
    python cashflow_proforma.py --price 3200000000 --rent 13000000 --area 70 \
        --loan 1600000000 --interest 0.09
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import json_output, json_error, validate_positive, validate_range


def parse_args():
    parser = argparse.ArgumentParser(
        description="10-Year Cash Flow Pro-forma for Vietnamese Real Estate"
    )
    parser.add_argument("--price", type=float, required=True,
                        help="Purchase price (VND)")
    parser.add_argument("--rent", type=float, required=True,
                        help="Monthly gross rent (VND)")
    parser.add_argument("--area", type=float, default=None,
                        help="Area in sqm (for mgmt fee calculation)")
    parser.add_argument("--vacancy", type=float, default=0.125,
                        help="Vacancy rate (default 0.125 = 1.5 months/year)")
    parser.add_argument("--mgmt_fee", type=float, default=10000,
                        help="Management fee VND/sqm/month (default 10000)")
    parser.add_argument("--tax_rate", type=float, default=0.10,
                        help="Tax rate on effective gross income (default 0.10)")
    parser.add_argument("--maintenance", type=float, default=0.015,
                        help="Annual maintenance as fraction of price (default 0.015)")
    parser.add_argument("--loan", type=float, default=0,
                        help="Loan amount (VND, default 0)")
    parser.add_argument("--interest", type=float, default=0.09,
                        help="Annual interest rate (default 0.09)")
    parser.add_argument("--years", type=int, default=10,
                        help="Projection horizon in years (default 10)")
    parser.add_argument("--rent_growth", type=float, default=0.03,
                        help="Annual rent growth rate (default 0.03)")
    parser.add_argument("--furniture", type=float, default=0,
                        help="Total furniture cost, depreciated over 5 years (default 0)")
    return parser.parse_args()


def validate_inputs(args):
    validate_positive("price", args.price)
    if args.rent < 0:
        json_error("rent must be >= 0")
    validate_range("vacancy", args.vacancy, 0, 1)
    validate_range("tax_rate", args.tax_rate, 0, 1)
    validate_range("maintenance", args.maintenance, 0, 1)
    validate_range("interest", args.interest, 0, 1)
    validate_range("rent_growth", args.rent_growth, 0, 1)
    validate_range("years", args.years, 1, 30)
    if args.loan < 0:
        json_error("loan must be >= 0")
    if args.furniture < 0:
        json_error("furniture must be >= 0")
    if args.loan > args.price:
        json_error("loan cannot exceed price")


def compute_proforma(args):
    year_by_year = []
    debt_service = args.loan * args.interest

    for year in range(1, args.years + 1):
        gross_rent = args.rent * 12 * (1 + args.rent_growth) ** (year - 1)
        vacancy_loss = gross_rent * args.vacancy
        effective_gross = gross_rent - vacancy_loss

        mgmt_cost = args.mgmt_fee * args.area * 12 if args.area else 0
        tax = effective_gross * args.tax_rate
        maintenance_cost = args.price * args.maintenance
        furniture_dep = (args.furniture / 60 * 12
                         if args.furniture > 0 and year <= 5 else 0)
        total_opex = mgmt_cost + tax + maintenance_cost + furniture_dep

        noi = effective_gross - total_opex
        net_cf = noi - debt_service

        year_by_year.append({
            "year": year,
            "gross_rent": round(gross_rent, 0),
            "vacancy_loss": round(vacancy_loss, 0),
            "effective_gross": round(effective_gross, 0),
            "mgmt_cost": round(mgmt_cost, 0),
            "tax": round(tax, 0),
            "maintenance_cost": round(maintenance_cost, 0),
            "furniture_dep": round(furniture_dep, 0),
            "total_opex": round(total_opex, 0),
            "noi": round(noi, 0),
            "debt_service": round(debt_service, 0),
            "net_cf": round(net_cf, 0),
        })

    # Summary from year 1
    y1 = year_by_year[0]
    equity = args.price - args.loan
    monthly_cf = y1["net_cf"] / 12

    if equity <= 0:
        json_error("equity (price - loan) must be positive")

    annual_coc = y1["net_cf"] / equity

    # DSCR calculation
    if debt_service > 0:
        if args.rent == 0:
            dscr = 0.0
        else:
            dscr = y1["noi"] / debt_service

        if dscr < 1.0:
            dscr_flag = "red"
        elif dscr < 1.3:
            dscr_flag = "yellow"
        else:
            dscr_flag = "green"
    else:
        dscr = None
        dscr_flag = None

    summary = {
        "monthly_cf": round(monthly_cf, 0),
        "annual_coc": round(annual_coc, 4),
        "equity": round(equity, 0),
        "debt_service_annual": round(debt_service, 0),
        "dscr": round(dscr, 4) if dscr is not None else None,
        "dscr_flag": dscr_flag,
    }

    if dscr is not None and dscr < 1.0:
        shortfall = abs(monthly_cf)
        summary["warning"] = (
            f"DSCR < 1.0 -- negative cash flow. "
            f"Monthly shortfall: {round(shortfall, 0):.0f} VND"
        )

    return summary, year_by_year


def main():
    args = parse_args()
    validate_inputs(args)
    summary, year_by_year = compute_proforma(args)
    json_output(summary=summary, year_by_year=year_by_year)


if __name__ == "__main__":
    main()
