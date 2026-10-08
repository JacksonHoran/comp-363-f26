# Classic vs. Karatsuba Multiplication: A Timing Study
>Claude was used to help me format the formulas and spelling and grammar checking

$$T(n) = r\,T\!\left(\frac{n}{c}\right) + n^d$$

Both algorithms fit the theorem with $c = 2$, since `split_in_half` halves each factor. The classic version has four recursive calls ($r = 4$); while Karatsuba makes three recursive calls ($r = 3$). The rest of the work is linear, $O(n^1)$, so $d = 1$: since `split_in_half`, `shift`, `add_digits`, and `subtract_digits` each make one pass over at most $n$ digits, a fixed number of times per call. Each algorithm creates more subproblems per call than the factor by which each subproblem's work shrinks. When $r > c^d$, the Master Theorem says the recursion dominates and $T(n) = O(n^{\log_c r})$. That gives $O(n^{\log_2 4}) = O(n^2)$ for classic and $O(n^{\log_2 3}) \approx O(n^{1.585})$ for Karatsuba.

Counting only digit multiplications,

$$M(n) = 4\,M\!\left(\frac{n}{2}\right), \qquad K(n) = 3\,K\!\left(\frac{n}{2}\right), \qquad M(1) = K(1) = 1,$$

so

$$M(n) = 4^{\log_2 n} = n^2 \qquad \text{and} \qquad K(n) = 3^{\log_2 n} = n^{\log_2 3}.$$

My counts matched exactly: $262{,}144 = 512^2$ and $19{,}683 = 3^9$ at $n = 512$.

Classic was faster through $n = 16$. Karatsuba won from $n = 32$ on, taking 77.5 ms vs. 281.6 ms at $n = 512$. On small inputs I'd expect Classic to outweigh Karatsuba. The graphs show at smaller inputs Classic performs better until $n = 16$. Its extra additions and list copies outweigh the one multiplication it saves.  Doubling $n$ from $n = 8$ on multiplied classic's time by about $4.0$ to $4.2$ and Karatsuba's by $2.8$ to $3.4$ before settling in at $3.07$, as $\Theta(n^2)$ and $\Theta(n^{\log_2 3})$ predict.


At $n = 512$, Karatsuba did $13.3\times$ fewer multiplications but ran only $3.6\times$ faster, because most of the time goes to linear list work, and Karatsuba does more of it per call. That gap held at about 3.6 to 3.9 from $n = 32$ on: a constant factor, not a different growth rate.

For $n \geq 8$, medians were within 12% of the minimum, but the smallest inputs varied up to $2.3\times$. Since noise can only add time, the minimum of seven trials is the most repeatable estimate.