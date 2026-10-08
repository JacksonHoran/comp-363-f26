import math

EPSILON = 0.0001
LIMIT = 1_000

def checkCases(num: float, stopCounter: int, LIMIT=LIMIT):
    if num < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    if num == 0:
        return 0
    if stopCounter > LIMIT:
        raise RecursionError("Maximum limit exceeded")
    return None

def lessThanEpsilon(num: float, guess: float, EPSILON=EPSILON):
    return not (abs(guess * guess - num) > EPSILON)

def update(num: float, guess: float, stopCounter: int):
    if stopCounter == 0:
        return num / 2.0
    else:
        return (guess + num / guess) / 2.0

def sqrt(num: float, guess=0.0, stopCounter=0):
    error = checkCases(num, stopCounter)
    if error is not None:
        return error
    
    guess = update(num, guess, stopCounter)

    if lessThanEpsilon(num, guess):
        return guess
    else: 
        return sqrt(num, guess, stopCounter + 1)

    
if __name__ == "__main__":
    # perfect squares
    for n, expected in [(1, 1), (4, 2), (25, 5), (144, 12)]:
        result = sqrt(n)
        assert math.isclose(result, expected, abs_tol=EPSILON), \
            f"sqrt({n}) = {result}, expected ~{expected}"
        print(f"sqrt({n:>4}) = {result:<22}  (expected {expected})")

    # non-perfect squares
    for n in [2, 10, 24, 99, 1000]:
        result = sqrt(n)
        reference = math.sqrt(n)
        assert math.isclose(result, reference, abs_tol=EPSILON), \
            f"sqrt({n}) = {result}, but math.sqrt says {reference}"
        print(f"sqrt({n:>4}) = {result:<22}  (math.sqrt = {reference})")

    # edge case: input is 0
    assert sqrt(0) == 0, "sqrt(0) should return 0"
    print("sqrt(0) correctly returned 0")

    # edge case: negatives must raise
    try:
        sqrt(-4)
    except ValueError as e:
        print(f"sqrt(-4) correctly raised ValueError: {e}")
    else:
        raise AssertionError("BUG: sqrt(-4) returned instead of raising!")

    # edge case: exceeding the iteration cap must raise
    try:
        checkCases(25, stopCounter=LIMIT + 1)
    except RecursionError as e:
        print(f"limit exceeded correctly raised RecursionError: {e}")
    else:
        raise AssertionError("BUG: exceeding LIMIT did not raise!")

    print("\nAll assertions passed.")