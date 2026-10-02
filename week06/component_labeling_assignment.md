# Assignment: Labeling Connected Components

## What you already have

In class, and in [`graphs.ipynb`](graphs.ipynb),
we built `reached(starting_vertex, g)`: given a starting vertex and an
adjacency matrix, it returns every vertex reachable from that start. On top
of that we built `count_components(g)`, which calls `reached` from every
vertex not yet swept into a component and counts how many times it had to
start over.

`count_components` tells you *how many* components a graph has — on the
class's six-vertex example, 3 — but it throws the actual membership away.
After calling `reached(starting_vertex, g)`, all it keeps is the length of
the list it got back (indirectly, by extending `marked` and moving on); it
never records *which* component each vertex ended up in. This is the same
"we kept the value but lost the detail" situation from the knapsack unit,
except there the lost detail was *which items* were in the optimal subset,
and here it's *which component* each vertex belongs to. The outline for
this unit calls the fix "component **labeling**," and that's this
assignment.

## The assignment

Write a function `label_components(g)` that returns a list `labels` of
length $n$ (the number of vertices) such that:

- `labels[v]` is a non-negative integer — the id of the component vertex
  $v$ belongs to ($0, 1, 2, \ldots$).
- Two vertices $u$ and $v$ get the **same** label if and only if they are
  mutually reachable (i.e., they're in the same connected component).

Build it directly on top of `reached`, reusing the same structure
`count_components` already uses — try every vertex as a starting point, and
if it hasn't been dealt with yet, sweep in everything reachable from it.
The only change is what you do with the result of that sweep: instead of
just counting, record the current label for every vertex in it, then move
to the next label.

Once `label_components` works, add two small things on top of it:

1. `connected(u, v, g)` — using `labels`, answer whether $u$ and $v$ are in
   the same component, without calling `reached` again.
2. The **largest component**: its size, and the vertices in it. Lecture's
   running analogy was the continental US versus Hawaii and Puerto Rico —
   this is asking your code to identify which one is the "mainland."

## Questions to work through before you write code

- `count_components` increments a counter every time it finds an unlabeled
  vertex, then discards the list that `reached` handed it. What do you do
  with that list instead, and when exactly do you do it?
- What value marks a vertex as "not yet labeled"? It can't be a valid label
  (so not `0`), and it has to be distinguishable from every label you'll
  ever assign. What are a couple of reasonable choices in Python, and what
  would go wrong with the most obvious one you'd rule out?
- `reached` explores vertices in last-in-first-out order (because of
  `gonext.pop()`), so two different starting vertices can visit their
  component's members in different orders. Does that affect *which* numeric
  label a component gets? Does it need to? (Compare this to the order
  question we raised about `reached` itself — the final set didn't depend
  on exploration order; ask the same thing here about the final grouping.)
- Your `labels` list and `count_components`'s final count are two different
  views of the same underlying fact. If they ever disagree on the same
  graph, which one would you trust less, and why?

## Checking your work

A labeling is correct as a *grouping*, not as a specific set of numbers —
relabeling every `0` to `2` and every `2` to `0` throughout is still
correct, as long as vertices that belong together still share a label and
vertices that don't, don't. Check your output against these graphs that
way, not number-for-number:

| Graph | Vertices | Edges | Expected grouping | Expected count |
|---|---|---|---|---|
| Class example | 0–5 | 0–1, 0–2, 3–4 | $\{0,1,2\}$, $\{3,4\}$, $\{5\}$ | 3 |
| No edges | 0–3 | (none) | $\{0\}$, $\{1\}$, $\{2\}$, $\{3\}$ | 4 |
| Complete graph $K_4$ | 0–3 | every pair | $\{0,1,2,3\}$ | 1 |
| Two triangles | 0–5 | 0–1, 1–2, 0–2, 3–4, 4–5, 3–5 | $\{0,1,2\}$, $\{3,4,5\}$ | 2 |
| A path | 0–4 | 0–1, 1–2, 2–3, 3–4 | $\{0,1,2,3,4\}$ | 1 |

For the class example and the two triangles, also confirm your "largest
component" logic picks a three-vertex group (there's a tie — either is a
correct answer). For at least one graph produced by
`create_random_undirected_graph`, confirm that the number of distinct
labels `label_components` produces matches what `count_components` reports
for that same graph — they're built from the same primitive, so a
disagreement means a bug in one of them, not a modeling choice.

## Something to think about, not to hand in

Everything here assumes an *undirected* graph, where reachability is
symmetric — if $u$ can reach $v$, $v$ can reach $u$, so "same component" is
a clean, mutual relationship. Lecture also discussed directed graphs, where
in-degree and out-degree can differ. If you tried to reuse `label_components`
on a directed adjacency matrix as-is, what would it actually compute —
still "mutual reachability," or something weaker? What would have to change
for the two ideas to match again? (This is the question that strongly
connected components answers, later in the course — you don't need the
answer now, just notice that the question is live.)
