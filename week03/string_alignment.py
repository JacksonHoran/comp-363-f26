from __future__ import annotations

# Price list from class: match 0, mismatch 2, gap 1. compute_penalty() takes
# a and a_gap as callables (rather than hardcoding these values into the
# recurrence) so the same function works with any price list a caller wants.
# This is the same design choice museum_partial() makes with w and v in the
# knapsack problem: the recurrence's *shape* doesn't depend on the specific
# numbers, so we keep the numbers out of the function that encodes the shape.
GAP_PENALTY = 1  # Penalty for introducing a gap
MISMATCH_PENALTY = 2  # Penalty for a mismatch
MATCH_PENALTY = 0  # No penalty for a match


def a(x: str, y: str) -> int:
    """
    Computes the penalty for aligning two characters.

    Parameters:
    x (str): The first character.
    y (str): The second character.

    Returns:
    int: The penalty for aligning the two characters.
    """
    # This is a_xy from the recurrence: 0 when the two symbols in an
    # alignment column agree, MISMATCH_PENALTY when they don't. Two
    # characters, always compared in isolation from the rest of the
    # strings -- this function has no idea it's being called from inside
    # a table fill, which is exactly why compute_penalty() can be handed
    # any similarly-shaped a() and still work.
    penalty = MISMATCH_PENALTY
    if x == y:
        penalty = MATCH_PENALTY
    return penalty


def a_gap() -> int:
    """
    Returns the penalty for introducing a gap. For now, this is a trivial
    function that returns a constant value, but it can be modified to compute
    the penalty based on the context of the alignment.

    Returns:
    int: The penalty for introducing a gap.
    """
    # Constant for now, but written as a function (not just a module-level
    # constant used directly) because a_gap in the general problem is
    # allowed to depend on context -- e.g., a real bioinformatics scoring
    # scheme might charge more for *opening* a gap than for extending one
    # already in progress. Keeping it a callable means compute_penalty()
    # doesn't have to change if a_gap() ever grows that kind of logic.
    return GAP_PENALTY


def compute_penalty(X: str, Y: str, a: callable, a_gap: callable) -> list[list[int]]:
    """
    Computes the penalty for aligning two sequences with gaps.

    Parameters:
    X (str): The first sequence.
    Y (str): The second sequence.
    a (function): A function that computes the penalty for a mismatch.
    a_gap (function): A function that computes the penalty for introducing a gap.

    Returns:
    list[list[int]]: The penalty matrix for aligning the two sequences.
    """
    # P[i][j] is P(i,j) from the recurrence: the cost of optimally aligning
    # the length-i PREFIX of X with the length-j PREFIX of Y. The table has
    # one extra row and column (m+1 by n+1, not m by n) to make room for the
    # empty-prefix case, P(0, anything) and P(anything, 0) -- there's no
    # valid array index for "zero characters" otherwise.
    m: int = len(X)
    n: int = len(Y)
    P: list[list[int]] = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    # Base cases: aligning a non-empty prefix against an empty one has only
    # one possible "alignment" -- every character in the non-empty prefix
    # lines up with a gap. That's i (or j) gap penalties, no choice
    # involved, which is why these two loops don't need min() at all.
    # Ok, I am a bit dramatic with setting i,j to int here, but I want to
    # make sure that the type hints are clear and explicit.
    i: int
    j: int
    for i in range(1, m + 1):
        P[i][0] = i * a_gap()
    for j in range(1, n + 1):
        P[0][j] = j * a_gap()
    # Fill the rest of the penalty matrix. Row i and column j must already
    # be filled in row-major, top-to-bottom / left-to-right order for this
    # to work, because P[i][j] depends on P[i-1][j-1], P[i-1][j], and
    # P[i][j-1] -- all three are "earlier" cells under that ordering, which
    # is exactly why the base cases above had to come first.
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # The three options below are the three possible last columns
            # of an optimal alignment of the length-i prefix of X and the
            # length-j prefix of Y (see the class derivation / the
            # accompanying notebook): X[i-1] paired with a gap, a gap
            # paired with Y[j-1], or X[i-1] paired with Y[j-1]. We don't
            # know which of the three is actually optimal ahead of time,
            # so we compute the cost of all three and let min() decide --
            # this is the recurrence, verbatim. Note X[i-1] and Y[j-1],
            # not X[i] and Y[j]: X and Y are 0-indexed strings, but i and j
            # count *how many* characters we've consumed, so the last
            # character consumed so far is always one index behind.
            P[i][j] = min(
                P[i - 1][j] + a_gap(),
                P[i][j - 1] + a_gap(),
                P[i - 1][j - 1] + a(X[i - 1], Y[j - 1]),
            )
    return P