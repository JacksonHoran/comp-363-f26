# Week 04 Reference Solution: Classic vs. Karatsuba Timing Study

Code: [`week04_solution.py`](week04_solution.py) (standard library only).
Raw table: [`timings.csv`](timings.csv). Timings below are the **minimum of 7
runs** on one laptop with seed 363; yours will differ in absolute value but
not in shape.

## Part 1: Correctness

Trace of `multiply_classic([1, 2], [3, 4])`: $A=1, B=2, C=3, D=4$, so
$AC=3$, $BC=6$, $AD=4$, $BD=8$, and
$xy = 3\cdot 10^2 + (6+4)\cdot 10 + 8 = 408 = 12\times 34$.

Karatsuba computes only $AC=3$, $BD=8$, and $(A+B)(C+D)=3\cdot 7=21$, so the
middle term is $21-3-8=10$ and the result is again $300+100+8=408$.
(Here $A+B$ and $C+D$ do not carry; for $[9,9]$ they do, and the code sets the
carry aside so the recursive call still sees $n/2$ digits.)

`test_against_builtin` compares both routines with `*` on 260 cases
(lengths 1 to 16, random, all-9s, and zero), all passing.

## Part 2 and 3: Measurements

| n | classic ms | Karatsuba ms | classic ÷ Karatsuba | classic mults | Karatsuba mults | classic ×2 | Karatsuba ×2 |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 2 | 0.005 | 0.011 | 0.43 | 4 | 3 | – | – |
| 4 | 0.025 | 0.046 | 0.53 | 16 | 9 | 5.07 | 4.10 |
| 8 | 0.107 | 0.155 | 0.69 | 64 | 27 | 4.34 | 3.34 |
| 16 | 0.438 | 0.494 | 0.89 | 256 | 81 | 4.08 | 3.19 |
| 32 | 1.776 | 1.517 | 1.17 | 1024 | 243 | 4.06 | 3.07 |
| 64 | 7.089 | 4.622 | 1.53 | 4096 | 729 | 3.99 | 3.05 |
| 128 | 28.627 | 13.969 | 2.05 | 16384 | 2187 | 4.04 | 3.02 |
| 256 | 115.023 | 42.251 | 2.72 | 65536 | 6561 | 4.02 | 3.02 |
| 512 | 461.260 | 127.399 | 3.62 | 262144 | 19683 | 4.01 | 3.02 |

## Part 4: Report

**1. Master Theorem.** For $T(n)=r\,T(n/c)+n^d$:

- Classic: $r=4$ (`AC`, `BC`, `AD`, `BD`), $c=2$ (halves), $d=1$. The
  non-recursive work is splitting, three `add_digits` calls, and `shift`s, each
  a single pass over $O(n)$ digits. Since $r=4>c^d=2$, this is the
  leaf-dominated case: $T(n)=\Theta(n^{\log_2 4})=\Theta(n^2)$.
- Karatsuba: $r=3$ (`AC`, `BD`, `(A+B)(C+D)`), $c=2$, $d=1$. The two
  additions of halves, two subtractions, and the shifts and final additions
  are still $O(n)$ (just more of them, which changes the constant, not $d$).
  Again $r=3>2$, so $T(n)=\Theta(n^{\log_2 3})\approx\Theta(n^{1.585})$.

**2. Multiplication counts.** Only multiplications count, so $f(n)=0$ and
$M(1)=1$. Classic: $M(n)=4M(n/2)$, so $M(n)=4^{\log_2 n}=n^2$. Karatsuba:
$M(n)=3M(n/2)$, so $M(n)=3^{\log_2 n}=n^{\log_2 3}$. The table matches
**exactly**, not just asymptotically: 262,144 $=512^2$ and
19,683 $=3^9=512^{\log_2 3}$. At $n=512$ Karatsuba does 13.3 times fewer
multiplications.

**3. Running times.** Classic wins for $n\le 16$ (Karatsuba is 2.3 times slower at $n=2$);
the crossover is between $n=16$ and $n=32$ on this machine. From there
Karatsuba's lead widens at every doubling, to 3.6 times at $n=512$. Karatsuba
loses at small $n$ because each level pays for extra additions, subtractions,
carries, and list slicing that a single-digit multiplication doesn't repay.
A production implementation stops recursing at a cutoff and finishes with
the classic method.

**4. Growth rate.** Classic time grows about $4.0\times$ per doubling ($2^2$),
Karatsuba about $3.02\times$ ($2^{\log_2 3}=3$). Both match $\Theta(n^2)$ and
$\Theta(n^{\log_2 3})$. The larger ratios at small $n$ (5.07, 4.10) are
fixed overhead (function calls, timer resolution) that hasn't yet been
swamped by the $n$-dependent work.

**5. Counts vs. clock.** They do not match. The count ratio at $n=512$ is 13.3,
the time ratio only 3.6. Karatsuba's non-multiplication work (two half-length
additions, two subtractions, carry handling, shifts, and list copies at every
node of the recursion) is real cost that the multiplication count ignores.
The *exponents* agree; the *constant* is what differs, and it moves the
crossover from $n=1$ to about $n=20$–$30$. The gap keeps closing in Karatsuba's
favor as $n$ grows, since $n^{0.415}$ eventually outgrows any constant.

**6. Reproducibility.** Rerun the script and compare: relative variation is
largest at small $n$, where microsecond timings sit near the OS-scheduling and
timer noise floor, and shrinks as $n$ grows. (Measure it yourself, e.g. print
the min and max of the 7 trials.) Noise is one-sided: interference only ever
adds time, so the minimum estimates the undisturbed cost, while the median
would still absorb some interference.

## Something to think about

Padding 513 digits to 1024 makes classic do $\approx 4\times$ and Karatsuba
$\approx 3\times$ the work of a 512-digit input, for a 1-digit larger problem.
Fix: recurse on unequal halves (split at $\lceil n/2\rceil$ and pad only the
shorter piece by one digit at each level), or stop at a small cutoff that
needn't be a power of 2 and finish with classic multiplication.
