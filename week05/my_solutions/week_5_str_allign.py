GAP = 1
MATCH = 0
MISMATCH = 2

def string_allign(
    x: str, 
    y: str, 
    gap: int,
    match: int,
    mismatch: int,
    ):
    m = len(x)
    n = len(y)
    matrix = [[None] * (n + 1) for _ in range(m + 1)]

    matrix[0][0] = 0
    for j in range(1, n + 1):
        matrix[0][j] = j * gap
    for i in range(1, m + 1):
        matrix[i][0] = i * gap

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                diaganol_cost = match
            else:
                diaganol_cost = mismatch

            matrix[i][j] = min(
                matrix[i - 1][j - 1] + diaganol_cost,
                matrix[i - 1][j] + gap,
                matrix[i][j - 1] + gap
            )
    return matrix, matrix[m][n]

def traceback(
    matrix: list[list[int]],
    x: str,
    y: str,
    gap: int,
    match: int,
    mismatch: int,
    ):
    i = len(x)
    j = len(y)
    x_cols = []
    y_cols = []

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            if x[i - 1] == y[j - 1]:
                diaganol_cost = match
            else:
                diaganol_cost = mismatch

            if matrix[i][j] == matrix[i - 1][j - 1] + diaganol_cost:
                x_cols.append(x[i - 1])
                y_cols.append(y[j - 1])
                i -= 1
                j -= 1
                continue

        if i > 0 and matrix[i][j] == matrix[i - 1][j] + gap:
            x_cols.append(x[i - 1])
            y_cols.append("-")
            i -= 1
        else:
            x_cols.append("-")
            y_cols.append(y[j - 1])
            j -= 1

    return "".join(reversed(x_cols)), "".join(reversed(y_cols))

def alignment_cost(
    x_aligned: str,
    y_aligned: str,
    gap: int,
    match: int,
    mismatch: int,
    ):
    total = 0
    for a, b in zip(x_aligned, y_aligned):
        if a == "-" or b == "-":
            total += gap
        elif a == b:
            total += match
        else:
            total += mismatch
    return total

def align(x: str, y: str, gap: int, match: int, mismatch: int):
    matrix, cost = string_allign(x, y, gap, match, mismatch)
    x_aligned, y_aligned = traceback(matrix, x, y, gap, match, mismatch)
    return cost, x_aligned, y_aligned

if __name__ == "__main__":
    test_cases = [
        ("CAT", "CATS", 1),
        ("CATS", "DOGS", 6),
        ("BICYCLE", "CYCLE", 2),
        ("CRANE", "RAIN", 3),
        ("ASTRONOMY", "GASTRONOMY", 1),
        ("DELICIOUS", "RELIGIOUS", 4),
        ("INTENTION", "EXECUTION", 8),
    ]

    for x, y, expected in test_cases:
        cost, x_aligned, y_aligned = align(x, y, GAP, MATCH, MISMATCH)
        recomputed = alignment_cost(x_aligned, y_aligned, GAP, MATCH, MISMATCH)
        ok = (
            cost == expected
            and len(x_aligned) == len(y_aligned)
            and x_aligned.replace("-", "") == x
            and y_aligned.replace("-", "") == y
            and recomputed == cost
        )
        print(f"[{'PASS' if ok else 'FAIL'}] {x!r} vs {y!r}: got {cost}, expected {expected}, recomputed {recomputed}")
        print(f"    {x_aligned}")
        print(f"    {y_aligned}")