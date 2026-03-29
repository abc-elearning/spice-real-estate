"""Monte Carlo price projection using Geometric Brownian Motion.

Simulates future property prices and outputs percentile statistics as JSON.

Usage:
    python monte_carlo.py --price 1000000 --growth 0.05 --std 0.1 --years 5
"""

import argparse
import math
import sys

from utils import json_output, json_error, validate_positive, validate_range


def parse_args():
    parser = argparse.ArgumentParser(description="Monte Carlo GBM price simulation")
    parser.add_argument("--price", type=float, required=True, help="Initial price")
    parser.add_argument("--growth", type=float, required=True, help="Annual growth rate (mu)")
    parser.add_argument("--std", type=float, required=True, help="Annual volatility (sigma)")
    parser.add_argument("--years", type=int, required=True, help="Projection horizon in years")
    parser.add_argument("--sims", type=int, default=1000, help="Number of simulations")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    return parser.parse_args()


def simulate_numpy(price, growth, std, years, sims, seed):
    """Vectorized GBM simulation using numpy."""
    import numpy as np

    if seed is not None:
        np.random.seed(seed)

    # GBM: S(t) = S(0) * exp((mu - sigma^2/2)*t + sigma*W(t))
    # W(t) = normal(0, sqrt(t))
    t = float(years)
    drift = (growth - 0.5 * std ** 2) * t
    diffusion = std * np.sqrt(t) * np.random.standard_normal(sims)
    final_prices = price * np.exp(drift + diffusion)

    percentiles = {
        "p10": float(np.percentile(final_prices, 10)),
        "p25": float(np.percentile(final_prices, 25)),
        "p50": float(np.percentile(final_prices, 50)),
        "p75": float(np.percentile(final_prices, 75)),
        "p90": float(np.percentile(final_prices, 90)),
    }
    mean = float(np.mean(final_prices))
    prob_loss = float(np.sum(final_prices < price) / sims)

    return final_prices, percentiles, mean, prob_loss


def simulate_stdlib(price, growth, std, years, sims, seed):
    """Loop-based GBM simulation using stdlib random."""
    import random

    if seed is not None:
        random.seed(seed)

    t = float(years)
    drift = (growth - 0.5 * std ** 2) * t
    vol = std * math.sqrt(t)

    final_prices = []
    for _ in range(sims):
        z = random.gauss(0, 1)
        s_t = price * math.exp(drift + vol * z)
        final_prices.append(s_t)

    final_prices.sort()
    n = len(final_prices)

    def percentile(pct):
        k = (pct / 100.0) * (n - 1)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return final_prices[int(k)]
        return final_prices[f] * (c - k) + final_prices[c] * (k - f)

    percentiles = {
        "p10": percentile(10),
        "p25": percentile(25),
        "p50": percentile(50),
        "p75": percentile(75),
        "p90": percentile(90),
    }
    mean = sum(final_prices) / n
    prob_loss = sum(1 for p in final_prices if p < price) / n

    return final_prices, percentiles, mean, prob_loss


def main():
    args = parse_args()

    # Validate inputs
    validate_positive("price", args.price)
    validate_positive("std", args.std)
    validate_range("years", args.years, 1, 50)
    validate_range("sims", args.sims, 100, 100000)

    # Try numpy first, fallback to stdlib
    use_numpy = True
    try:
        import numpy  # noqa: F401
    except ImportError:
        use_numpy = False
        print("Warning: numpy not available, using stdlib random (slower)", file=sys.stderr)

    if use_numpy:
        _, percentiles, mean, prob_loss = simulate_numpy(
            args.price, args.growth, args.std, args.years, args.sims, args.seed
        )
    else:
        _, percentiles, mean, prob_loss = simulate_stdlib(
            args.price, args.growth, args.std, args.years, args.sims, args.seed
        )

    json_output(
        price=args.price,
        growth=args.growth,
        std=args.std,
        years=args.years,
        sims=args.sims,
        seed=args.seed,
        mean=round(mean, 2),
        p10=round(percentiles["p10"], 2),
        p25=round(percentiles["p25"], 2),
        p50=round(percentiles["p50"], 2),
        p75=round(percentiles["p75"], 2),
        p90=round(percentiles["p90"], 2),
        prob_loss=round(prob_loss, 4),
    )


if __name__ == "__main__":
    main()
