# Part 1 — Hand traces of 12 × 34

x = `[1, 2]`, y = `[3, 4]`, so n = 2 and half = 1.
Expected answer (2n = 4 digits): `[_, _, _, _]`

## multiply_classic([1, 2], [3, 4])

Split (`split_in_half`):

| | value |
|---|---|
| A | |
| B | |
| C | |
| D | |

Four recursive products (each is an n = 1 base case → `multiply_digits`, returns 2 digits):

| product | digits | value |
|---|---|---|
| AC | | |
| BC | | |
| AD | | |
| BD | | |

Combine:

- `middle = add_digits(BC, AD)` →
- `shift(AC, n)` →
- `shift(middle, half)` →
- `total = add_digits(shift(AC, n), shift(middle, half))` →
- `total = add_digits(total, BD)` →
- `pad_left(total, 2n)` → **result:**

Single-digit multiplications used:

## multiply_karatsuba([1, 2], [3, 4])

A, B, C, D are the same as above.

Recursive products 1 and 2:

- `AC` =
- `BD` =

Sums and carries:

- `sum_AB = add_digits(A, B)` →   so `carry_x` = , `lo_AB` =
- `sum_CD = add_digits(C, D)` →   so `carry_y` = , `lo_CD` =

Recursive product 3:

- `lo_product = multiply_karatsuba(lo_AB, lo_CD)` →

Rebuild (A+B)(C+D):

- `carry_carry` =
- `cross` =
- `full` (after `pad_left(full, n + 2)`) =    check: (A+B)(C+D) =

Middle term:

- `middle = full − AC − BD` =    check: BC + AD =

Combine:

- `total = add_digits(shift(AC, n), shift(middle, half))` →
- `total = add_digits(total, BD)` →
- `pad_left(total, 2n)` → **result:**

Single-digit multiplications used:

## Why the carry is set aside

(In your own words: what would happen at n = 2 if `sum_AB` — which has
half + 1 digits — were passed straight into the recursion?)
