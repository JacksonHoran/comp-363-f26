'''
beautiful dock blocks via https://github.com/NilsJPWerner/autoDocstring
'''

import os #used only for file paths
import sys
import random
import statistics
import time
from collections.abc import Callable
import matplotlib.pyplot as plt
import pandas as pd
# multiplication.py is the instructor's starter code one folder up (week04/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from multiplication import *

# constants
RAND_SEED = 363
MAX_DIGIT = 9
TEST_MAX_POWER = 4
TEST_PAIRS_PER_LENGTH = 200
TIMING_MIN_POWER = 1
TIMING_MAX_POWER = 9
TRIALS = 7
NS_PER_MS = 1e6
LOG_BASE = 2
DPI = 150
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(THIS_DIR, "timings.csv")
LINEAR_PLOT_PATH = os.path.join(THIS_DIR, "timing.png")
LOGLOG_PLOT_PATH = os.path.join(THIS_DIR, "timing_loglog.png")
COLUMNS = ["n", "classic_ns", "karatsuba_ns", "classic_mults", "karatsuba_mults",
           "classic_median_ns", "karatsuba_median_ns",
           "classic_max_ns", "karatsuba_max_ns"]

# type aliases
Digits = list[int]
Multiplier = Callable[[Digits, Digits], Digits] # a function tha takes two int lists and returns an int list


# Part 1 -- check the code

def check_pair(func: Multiplier, x: Digits, y: Digits) -> bool:
    """ Return True if func(x, y) equals the true product and has exactly
    2n digits. Print the details and return False otherwise

    Args:
        func (function): multiply_classic or multiply_karatsuba
        x Digits: first factor, n digits, most significant first
        y Digits: second factor, same length n as x

    Returns:
        bool: True if the product is correct and 2n digits long
    """
    expected = to_int(x) * to_int(y)
    product = func(x, y)
    ok = to_int(product) == expected and len(product) == 2 * len(x)

    if not ok:
        print(f"FAIL {func.__name__}({x}, {y}) -> {product}, expected {expected}")

    return ok


def random_pair(n: int, rng: random.Random) -> tuple[Digits, Digits]:
    """ Return two random n-digit lists

    Args:
        n (int): number of digits in each list
        rng (random.Random): seeded generator

    Returns:
        tuple[Digits, Digits]: the pair (x, y).
    """
    x = [rng.randint(0, MAX_DIGIT) for _ in range(n)]
    y = [rng.randint(0, MAX_DIGIT) for _ in range(n)]
    result = (x, y)
    return result


def run_tests() -> tuple[int, int]:
    """ Check both algorithms against native `*` on TEST_PAIRS_PER_LENGTH
    random pairs of each length 1, 2, 4, etc, 2**TEST_MAX_POWER, plus the
    all-9s pair

    Returns:
        tuple[int, int]: (number of checks passed, number of checks run).
    """
    rng = random.Random(RAND_SEED)
    passed = 0
    total = 0

    for p in range(TEST_MAX_POWER + 1):
        n = 2**p
        cases = [random_pair(n, rng) for _ in range(TEST_PAIRS_PER_LENGTH)]
        cases.append(([MAX_DIGIT] * n, [MAX_DIGIT] * n))
        cases.append(([0] * n, [0] * n))
        for x, y in cases:
            for func in [multiply_classic, multiply_karatsuba]:
                if check_pair(func, x, y):
                    passed += 1
                total += 1

    result = (passed, total)
    return result


# Part 2 -- timing with perf_counter_ns()

def time_trials(func: Multiplier, x: Digits, y: Digits, trials: int) -> Digits:
    """ Time func(x, y) with perf_counter_ns(), `trials` times over

    Args:
        func (function): multiply_classic or multiply_karatsuba
        x Digits: first factor
        y Digits: second factor
        trials (int): how many times to repeat the measurement

    Returns:
        Digits: one elapsed time per trial, in nanoseconds
    """
    timings = []
    for _ in range(trials):
        start = time.perf_counter_ns()
        func(x, y)
        elapsed = time.perf_counter_ns() - start
        timings.append(elapsed)
    return timings


def count_mults(func: Multiplier, x: Digits, y: Digits) -> int:
    """ Count the single-digit multiplications func(x, y) performs, using
    the counter in multiplication.py

    Args:
        func (function): multiply_classic or multiply_karatsuba
        x Digits: first factor
        y Digits: second factor, same length as x

    Returns:
        int: number of calls to multiply_digits during func(x, y)
    """
    reset_digit_mult_count()
    func(x, y)
    result = get_digit_mult_count()
    return result


def run_experiment() -> list[tuple[int, ...]]:
    """ Time and count both algorithms on the same random inputs at each
    length 2^TIMING_MIN_POWER, ..., 2^TIMING_MAX_POWER.

    Returns:
        list[tuple]: one row per length, in the order of COLUMNS.
            classic_ns and karatsuba_ns are the minimum over TRIALS runs
    """
    rng = random.Random(RAND_SEED)
    rows = []
    for p in range(TIMING_MIN_POWER, TIMING_MAX_POWER + 1):
        n = 2**p
        x = random_digits(n, rng)
        y = random_digits(n, rng)

        classic_times = time_trials(multiply_classic, x, y, TRIALS)
        karatsuba_times = time_trials(multiply_karatsuba, x, y, TRIALS)

        m_classic = count_mults(multiply_classic, x, y)
        m_karatsuba = count_mults(multiply_karatsuba, x, y)

        rows.append((n,
                     min(classic_times), min(karatsuba_times),
                     m_classic, m_karatsuba,
                     statistics.median(classic_times), statistics.median(karatsuba_times),
                     max(classic_times), max(karatsuba_times)))
    return rows


# Part 3 -- getting the numbers out

def growth_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """ Compute how much each quantity grew since the previous length, as pct_change()
        + 1.

    Args:
        df (pandas.DataFrame): the timing table

    Returns:
        pandas.DataFrame: n and the growth ratio of each time and count.
    """
    result = pd.DataFrame({
        "n": df["n"],
        "classic_time_ratio": df["classic_ns"].pct_change() + 1,
        "karatsuba_time_ratio": df["karatsuba_ns"].pct_change() + 1,
        "classic_mults_ratio": df["classic_mults"].pct_change() + 1,
        "karatsuba_mults_ratio": df["karatsuba_mults"].pct_change() + 1,
    })
    return result


def plot_times(df: pd.DataFrame, path: str, loglog: bool) -> None:
    """ Draw classic vs. Karatsuba time against n and save the
    figure as a PNG

    Args:
        df (pandas.DataFrame): the timing table
        path (str): dir to save the image
        loglog (bool): True for log-log axes, False for linear axes.
    """
    fig, ax = plt.subplots()
    ax.plot(df["n"], df["classic_ns"] / NS_PER_MS, marker="o", label="classic")
    ax.plot(df["n"], df["karatsuba_ns"] / NS_PER_MS, marker="s", label="Karatsuba")
    ax.set_xlabel("number of digits, n")
    ax.set_ylabel(f"time (ms), best of {TRIALS}")
    title = "Classic vs. Karatsuba multiplication"

    if loglog:
        ax.set_xscale("log", base=LOG_BASE)
        ax.set_yscale("log")
        title = title + " (log-log)"

    ax.set_title(title)
    ax.legend()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)

if __name__ == "__main__":
    print("\n------------Part 1: correctness------------")
    passed, total = run_tests()
    print(f"{passed}/{total} checks passed")

    if passed == total:
        print("\n------------Part 2: timing------------")
        df = pd.DataFrame(run_experiment(), columns=COLUMNS)
        print(df.to_string(index=False))

        print("\n------------Part 3: output------------")
        df.to_csv(CSV_PATH, index=False)
        print(f"csv saved to {CSV_PATH}")

        print("\ngrowth when n doubles:")
        print(growth_ratios(df).to_string(index=False, float_format="%.2f"))

        plot_times(df, LINEAR_PLOT_PATH, loglog=False)
        plot_times(df, LOGLOG_PLOT_PATH, loglog=True)
        print(f"\ncharts saved to:\n{LINEAR_PLOT_PATH}\n{LOGLOG_PLOT_PATH}")
    else:
        print("skipped timing study, fix failing checks first")
