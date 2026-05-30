# Line incidences in the plane: AG(2,3), Sylvester–Gallai, and the orchard problem

A self-directed computational study of the Erdős function **F_k(n)** — the
maximum number of lines through at least *k* of *n* points in the plane — for
the smallest interesting case, *k* = 3. The project reaches the classical
results (Sylvester–Gallai, the Burr–Grünbaum–Sloane lower bound, and the
Green–Tao orchard optima) from scratch, verifies them in code, and characterises
why a natural heuristic search stalls below the known optimum.

## The question

Given *n* points in R², let

- **F_k(n)** = number of lines through **at least** *k* points,
- **f_k(n)** = number of lines through **exactly** *k* points.

Every pair of points determines at most one line, and a *k*-point line uses up
C(*k*, 2) pairs, so there is a trivial upper bound

```
F_k(n) ≤ C(n, 2) / C(k, 2).
```

For *n* = 9, *k* = 3 this is F_3(9) ≤ 36 / 3 = **12**. The natural question:
does any real configuration of 9 points attain it?

## Result 1 — the abstract optimum exists, but not over R

The affine plane **AG(2, 3)** has 9 points and 12 lines of 3, with every pair on
a unique line. As an abstract incidence structure it *saturates* the bound:
F_3 = 12. So the combinatorics permit 12 — the obstruction, if any, is geometric.

Embedding AG(2, 3) as the 3×3 integer grid in R² and counting incidences
exactly (`src/incidences.py`) gives:

| Configuration            | f_2 | f_3 | F_3 | bound |
|--------------------------|-----|-----|-----|-------|
| 3×3 grid in R²           | 12  |  8  |  8  | 12    |
| 9 points on *y = x³*     | 12  |  8  |  8  | 12    |
| AG(2, 3), abstract       |  0  | 12  | 12  | 12    |

Only **8 of the 12** abstract lines survive as straight lines in R². The four
that fail are the "wrap-around" lines of the torus (Z/3)² — they close up modulo
3 but bend in the plane:

```
(0,0) (1,2) (2,1)
(0,1) (1,0) (2,2)
(0,1) (1,2) (2,0)
(0,2) (1,0) (2,1)
```

This gap is not an artefact of the grid. It is the **Sylvester–Gallai theorem**
(conjectured 1893, proved by Gallai 1944): every finite, non-collinear point set
in R² has at least one *ordinary* line through exactly two points. A real
AG(2, 3) would have zero ordinary lines, which is impossible. AG(2, q) realises
only over finite fields, or in the complex projective plane (the Hesse
configuration for *q* = 3), never over R for *q* ≥ 2.

![Realization gap](figures/realization_gap.png)

## Result 2 — the lower bound that *is* tight

The **Burr–Grünbaum–Sloane** construction (1974) gives F_3(n) ≥ n²/6 − O(n) by
placing points on a cubic curve, where three points are collinear iff their
parameters sum to zero in the curve's group law. For the degenerate cubic
*y = x³* this is just Vieta's formula. The code verifies it:

| n  | f_3 on *y = x³* | n²/6 | bound C(n,2)/3 |
|----|-----------------|------|----------------|
| 9  | 8               | 13.5 | 12             |
| 12 | 15              | 24   | 22             |

A *smooth* elliptic curve does better still, thanks to torsion points that
contribute extra zero-sum triples. None of these beat the trivial bound — that
is reserved for AG-type configurations that only live over finite fields or C.

## Result 3 — where a heuristic search stalls (the orchard problem)

Counting lines through *exactly* 3 points is the **orchard problem**, whose
optima *t₃(n)* are known: t₃(9) = 10, t₃(11) = 16, t₃(12) = 19 (the *n* = 11, 12
values from Green–Tao, 2013). I built a continuous-space local search (anchored
descent from the Pappus 9-point configuration, adding extra points at
intersections of incidence lines) to try to reach these optima.

The search reliably finds **f₃ = 15 at n = 11** but cannot reach the optimum of
16. Characterising *why* turned out to be the interesting part: the Green–Tao
optimal configuration lives in a different, algebraically defined basin (its
16th line requires the explicit Green–Tao construction at the seed level), and
no sequence of single-point local moves connects the Pappus basin to it. This is
a clean illustration of a general phenomenon — local optimisation recovers
incidence structure within a basin but cannot cross between algebraically distant
constructions.

## Running it

```bash
pip install -r requirements.txt
python src/incidences.py
```

This reproduces every number in the tables above and prints the four
non-realizable AG(2, 3) lines.

## Files

```
src/incidences.py        Exact F_k / f_k incidence counting; AG(2,3) and BGS checks
figures/realization_gap.png   Abstract vs. real realization of AG(2,3)
docs/notes.md            Longer technical notes and references
```

## References

- J. J. Sylvester (1893); T. Gallai (1944) — the Sylvester–Gallai theorem.
- S. Burr, B. Grünbaum, N. Sloane, *The orchard problem*, Geometriae Dedicata (1974).
- B. Green, T. Tao, *On sets defining few ordinary lines*, Discrete & Computational Geometry (2013).

## Scope and honesty

This is a learning project, not new mathematics. It does not improve any known
bound. Its value is in reaching the classical theorems independently, verifying
them in reproducible code, and pinning down precisely why a natural search
heuristic falls short of the proven optimum.
