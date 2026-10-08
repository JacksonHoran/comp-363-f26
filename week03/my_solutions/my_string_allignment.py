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
        matrix, cost = string_allign(x, y, GAP, MATCH, MISMATCH)
        ok = (cost == expected)
        print(f"[{'PASS' if ok else 'FAIL'}] {x!r} vs {y!r}: got {cost}, expected {expected}")