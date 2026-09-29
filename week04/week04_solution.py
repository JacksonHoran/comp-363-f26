"""
COMP 363 -- Week 04 reference solution: Classic vs. Karatsuba multiplication.

Run from this folder:

    python3 week04_solution.py

It (1) tests both routines against Python's built-in `*`, (2) times them with
time.perf_counter_ns() and counts single-digit multiplications for
n = 2, 4, ..., 512, (3) writes timings.csv, (4) prints the growth ratios that
the written solution (week04_solution.md) discusses, and (5) draws
timing.png if matplotlib happens to be installed.

Only the standard library is required.
"""

import math
import random
import time

from multiplication import *


def test_against_builtin(rng, trials_per_length=50):
    """Compare both routines with Python's `*`; raise AssertionError on a mismatch."""
    checked = 0
    for p in range(0, 5):                       # lengths 1, 2, 4, 8, 16
        n = 2**p
        cases = [(random_digits(n, rng), random_digits(n, rng))
                 for _ in range(trials_per_length)]
        cases.append(([9] * n, [9] * n))        # all 9s: every carry fires
        cases.append(([0] * n, random_digits(n, rng)))
        for x, y in cases:
            expected = to_int(x) * to_int(y)
            assert to_int(multiply_classic(x, y)) == expected, (x, y)
            assert to_int(multiply_karatsuba(x, y)) == expected, (x, y)
            assert len(multiply_classic(x, y)) == 2 * n
            assert len(multiply_karatsuba(x, y)) == 2 * n
            checked += 1
    return checked


def time_one(func, x, y, trials):
    """Return the best (smallest) of `trials` timings of func(x, y), in ns."""
    best = None
    for _ in range(trials):
        start = time.perf_counter_ns()
        func(x, y)
        elapsed = time.perf_counter_ns() - start
        if best is None or elapsed < best:
            best = elapsed
    return best


def count_mults(func, x, y):
    """Return the number of single-digit multiplications func(x, y) performs."""
    reset_digit_mult_count()
    func(x, y)
    return get_digit_mult_count()


def run_experiment(max_power=9, trials=7, seed=363):
    """Return one row (n, classic_ns, karatsuba_ns, classic_mults, karatsuba_mults) per length."""
    rng = random.Random(seed)
    rows = []
    for p in range(1, max_power + 1):
        n = 2**p
        x = random_digits(n, rng)               # same inputs for both algorithms
        y = random_digits(n, rng)
        rows.append((n,
                     time_one(multiply_classic, x, y, trials),
                     time_one(multiply_karatsuba, x, y, trials),
                     count_mults(multiply_classic, x, y),
                     count_mults(multiply_karatsuba, x, y)))
    return rows


def write_csv(rows, path="timings.csv"):
    with open(path, "w") as f:
        f.write("n,classic_ns,karatsuba_ns,classic_mults,karatsuba_mults\n")
        for n, tc, tk, mc, mk in rows:
            f.write(f"{n},{tc},{tk},{mc},{mk}\n")


def print_report(rows):
    log3 = math.log2(3)
    print(f"{'n':>5} {'classic ms':>11} {'karat ms':>10} {'t ratio':>8} "
          f"{'classic mults':>14} {'n^2':>9} {'karat mults':>12} {'n^1.585':>9} "
          f"{'c x2':>6} {'k x2':>6}")
    previous = None
    for n, tc, tk, mc, mk in rows:
        growth_c = f"{tc / previous[1]:.2f}" if previous else "-"
        growth_k = f"{tk / previous[2]:.2f}" if previous else "-"
        print(f"{n:>5} {tc / 1e6:>11.3f} {tk / 1e6:>10.3f} {tc / tk:>8.2f} "
              f"{mc:>14} {n**2:>9} {mk:>12} {n**log3:>9.0f} {growth_c:>6} {growth_k:>6}")
        previous = (n, tc, tk)


def plot(rows, path="timing.png"):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        plt = None
    if plt is not None:
        ns = [r[0] for r in rows]
        fig, ax = plt.subplots()
        ax.plot(ns, [r[1] / 1e6 for r in rows], marker="o", label="classic")
        ax.plot(ns, [r[2] / 1e6 for r in rows], marker="s", label="Karatsuba")
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_xlabel("number of digits, n")
        ax.set_ylabel("time (ms)")
        ax.set_title("Classic vs. Karatsuba multiplication")
        ax.legend()
        fig.savefig(path, dpi=150)
    return plt is not None


def main():
    checked = test_against_builtin(random.Random(363))
    print(f"Part 1: {checked} random and edge-case products match Python's `*`.\n")
    rows = run_experiment()
    write_csv(rows)
    print_report(rows)
    print("\nplot written" if plot(rows) else "\nmatplotlib not installed; skipped timing.png")


if __name__ == "__main__":
    main()
