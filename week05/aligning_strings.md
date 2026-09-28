# Assignment: Tracing Back the Alignment

## What you already have

Two weeks ago, in class and in
[`string_alignment.ipynb`](../week03/string_alignment.ipynb), we derived the
recurrence for $P(i,j)$, the cost of optimally aligning the length-$i$
prefix of $X_m$ with the length $j$ prefix of $Y_n$:

$$
\begin{equation}
P(i,j) = \min \left ( P(i-1,j-1) + a_{x_{i-1}\,y_{j-1}},\quad
P(i-1,j)+a_{\text{gap}},\quad P(i,j-1)+a_{\text{gap}} \right )
\end{equation}
$$

and you wrote the code that fills in the entire table (assignment:
[`string_alignment_assignment.md`](../week03/string_alignment_assignment.md);
reference implementation: [`string_alignment.py`](../week03/string_alignment.py)).
At the time, that assignment explicitly stopped at the cost matrix and the
number in its bottom-right corner, $P(m,n)$ — figuring out *what the optimal
alignment looks like* was left for later.

It's later. This assignment is that "something to think about" from two
weeks ago, made concrete: you're going to trace back through the table you
already know how to build, and recover the alignment itself.

Our price list is still the one from class:

- match ($x = y$): **0**
- mismatch ($x \neq y$): **2**
- gap: **1**

## Read this first

Before you touch the alignment table, read how traceback works on a
problem we already solved end to end in class: the knapsack/subset-selection
problem in [`Museum_Heist.ipynb`](Museum_Heist.ipynb). Pay particular
attention to the section "How the traceback works?" and the
`museum_traceback` function. The idea there is:

- table $S(i,r)$ only remembers *how much* the optimal subset is worth, not
  *which* items are in it;
- every entry $S(i,r)$ was built from exactly one of a small number of
  smaller entries (there, exactly two: $S(i-1,r)$ or $S(i-1,r-w_i)+v_i$);
- traceback starts at the bottom-right corner (the answer to the whole
  problem) and, at each cell, re-asks which of those smaller entries
  actually produced the value sitting there — then moves to that smaller
  entry and repeats, until it runs out of table.

You should also (re-)read the relevant section of Jeff Erickson's dynamic
programming chapter,
[recurrences, memoization, and reconstructing solutions](https://jeffe.cs.illinois.edu/teaching/algorithms/book/03-dynprog.pdf),
which covers this same "recover the solution, not just its value" idea in
more generality.

Nothing about the museum heist is graded here. It's the worked example you
should have open in a second window while you do the assignment below.

## The assignment

Do for string alignment exactly what `museum_traceback` did for the
knapsack: write a function that starts at $P(m,n)$ and walks backward
through the table, recovering the actual aligned strings, not just the
cost.

The difference is that each cell $P(i,j)$ in the alignment table can come
from **three** possible neighbors instead of two:

- $P(i-1,j-1) + a_{x_{i-1}\,y_{j-1}}$ — the last column aligns $x_{i-1}$
  with $y_{j-1}$ (a match or a mismatch);
- $P(i-1,j) + a_{\text{gap}}$ — the last column aligns $x_{i-1}$ with a
  gap;
- $P(i,j-1) + a_{\text{gap}}$ — the last column aligns a gap with
  $y_{j-1}$.

At each cell, you have to figure out which of these three actually
produced the value stored at $P(i,j)$ — the same yes/no-style test
`museum_traceback` runs against its two candidates, just against three
here instead of two. (More than one candidate can tie; picking any one
that matches is fine.)

This means:

1. A function that takes the table $P$ (as built by your
   `compute_penalty`-style code from two weeks ago) along with $X$ and
   $Y$, and walks from $(m,n)$ back to $(0,0)$, recording, at each step,
   which of the three cases applied.
2. As you walk backward, build up the two aligned strings, $\overline X$
   and $\overline Y$, one column at a time — remember you're moving from
   the *end* of the alignment toward the beginning, so think about
   whether you're prepending or appending each character as you go.
3. A way to retrieve the full aligned pair ($\overline X$, $\overline Y$)
   from your function, alongside the cost $P(m,n)$ you already know how
   to compute.

## Questions to work through before you write code

- `museum_traceback` moves up a row unconditionally when it decides item
  $i$ wasn't taken, and up-and-left when it was. What are the three
  analogous moves here, and which cell coordinates do they land on?
- The knapsack traceback loop stops when `i` or `r` hits 0. What's the
  right stopping condition here, given that you have *two* indices, $i$
  and $j$, each of which can independently run out?
- Once $j$ reaches 0 but $i$ hasn't (or vice versa), there's no real
  choice left — every remaining column must be a gap on one side. Does
  your loop handle that automatically because it's built into the base
  case, or do you need to special-case it?
- `museum_traceback` only records *which items* were taken, not the order
  they appear in $\mathcal S$. Here, order matters — $\overline X$ and
  $\overline Y$ are strings, not sets. How does that change what you do
  inside the loop?

## Checking your work

Run your traceback against the same pairs you already validated the cost
matrix on. The costs should match what you got two weeks ago; now you can
also confirm the alignment itself is legitimate (same length for both
aligned strings, every column costs what your table says it should, and
summing the column costs reproduces $P(m,n)$).

| $X$ | $Y$ | $P(m,n)$ | One valid alignment |
|---|---|---|---|
| `CAT` | `CATS` | 1 | `CAT-` / `CATS` |
| `BICYCLE` | `CYCLE` | 2 | `BICYCLE` / `--CYCLE` |
| `CRANE` | `RAIN` | 3 | `CRANE` / `-RAIN` |
| `INTENTION` | `EXECUTION` | 8 | (several valid alignments exist — yours doesn't have to match anyone else's exactly, as long as its cost is 8) |

If your alignment's recomputed cost doesn't match $P(m,n)$, the bug is
almost always one of: picking a neighbor that doesn't actually satisfy the
recurrence at that cell, mixing up row/column direction, or getting the
stopping condition wrong at the edges of the table.

## A word on getting stuck

If your traceback runs but produces an alignment whose cost doesn't match
$P(m,n)$, print the sequence of cells it visits and compare that path
against the table by hand for a small example like `bicycle`/`cycle`. This
is the same debugging move you used two weeks ago on the forward pass —
find the one cell where the path takes a wrong turn, and ask why your test
at that cell chose the neighbor it did.
