"""Bayesian probability updater for real estate investment decisions.

Updates prior probability estimates using new evidence via Bayes' theorem.
Includes overconfidence detection when base rates are available.

Usage:
    python bayesian_updater.py --prior 0.4 --evidence_strength strong --evidence_direction positive
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import json_output, json_error, validate_choice


LIKELIHOOD_RATIOS = {
    "weak": 1.5,
    "moderate": 3.0,
    "strong": 6.0,
    "very_strong": 12.0,
}

VALID_STRENGTHS = list(LIKELIHOOD_RATIOS.keys())
VALID_DIRECTIONS = ["positive", "negative"]


def parse_args():
    parser = argparse.ArgumentParser(description="Bayesian probability updater")
    parser.add_argument("--prior", type=float, required=True,
                        help="Prior probability (strictly between 0 and 1)")
    parser.add_argument("--evidence_strength", type=str, required=True,
                        help="Evidence strength: weak|moderate|strong|very_strong")
    parser.add_argument("--evidence_direction", type=str, required=True,
                        help="Evidence direction: positive|negative")
    parser.add_argument("--base_rate", type=float, default=None,
                        help="Population base rate for overconfidence check")
    return parser.parse_args()


def validate_prior(prior):
    """Prior must be strictly between 0 and 1 (exclusive)."""
    if prior <= 0 or prior >= 1:
        json_error("prior must be strictly between 0 and 1 (exclusive)")


def validate_base_rate(base_rate):
    """Base rate must be strictly between 0 and 1 (exclusive)."""
    if base_rate <= 0 or base_rate >= 1:
        json_error("base_rate must be strictly between 0 and 1 (exclusive)")


def compute_posterior(prior, lr):
    """Bayes' theorem: posterior = (prior * lr) / (prior * lr + (1 - prior))."""
    return (prior * lr) / (prior * lr + (1 - prior))


def main():
    args = parse_args()

    # Validate inputs
    validate_prior(args.prior)
    validate_choice("evidence_strength", args.evidence_strength, VALID_STRENGTHS)
    validate_choice("evidence_direction", args.evidence_direction, VALID_DIRECTIONS)

    if args.base_rate is not None:
        validate_base_rate(args.base_rate)

    # Get likelihood ratio
    lr = LIKELIHOOD_RATIOS[args.evidence_strength]

    # If negative direction, use reciprocal
    if args.evidence_direction == "negative":
        lr = 1.0 / lr

    # Compute posterior
    posterior = compute_posterior(args.prior, lr)
    shift = posterior - args.prior

    # Interpretation text (Vietnamese)
    prior_pct = round(args.prior * 100, 1)
    posterior_pct = round(posterior * 100, 1)
    direction_vi = "tich cuc" if args.evidence_direction == "positive" else "tieu cuc"

    if shift >= 0:
        interpretation = (
            f"Xac suat tang tu {prior_pct}% len {posterior_pct}% "
            f"sau khi cap nhat bang chung {args.evidence_strength} {direction_vi}"
        )
    else:
        interpretation = (
            f"Xac suat giam tu {prior_pct}% xuong {posterior_pct}% "
            f"sau khi cap nhat bang chung {args.evidence_strength} {direction_vi}"
        )

    # Build result
    result = {
        "prior": round(args.prior, 6),
        "posterior": round(posterior, 6),
        "shift": round(shift, 6),
        "likelihood_ratio": round(lr, 6),
        "interpretation": interpretation,
    }

    # Overconfidence check
    if args.base_rate is not None and abs(args.prior - args.base_rate) > 0.2:
        result["overconfidence_warning"] = (
            f"Canh bao: Prior ({prior_pct}%) chenh lech lon voi ty le co so "
            f"({round(args.base_rate * 100, 1)}%). "
            f"Kiem tra xem ban co dang qua tu tin hoac qua bi quan khong."
        )

    json_output(**result)


if __name__ == "__main__":
    main()
