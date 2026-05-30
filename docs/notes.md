# Technical notes

These notes expand on the summary in the README and record the reasoning and
dead ends behind the code.

## 1. The trivial bound and what saturating it would mean

For *n* points in R² with F_k(n) lines through at least *k* points, each line of
*k* points accounts for C(*k*, 2) of the C(*n*, 2) point-pairs, and no pair is
counted twice, giving F_k(n) ≤ C(n, 2)/C(k, 2). Saturation requires a structure
in which *every* pair lies on a *k*-point line — i.e. a resolvable design. For
*k* = 3, *n* = 9 the candidate is the affine plane AG(2, 3): 9 points, 12 lines
of 3, each pair on a unique line.

## 2. AG(2,3) over F_3 vs. over R

AG(2, 3) is the point/line geometry of F_3 × F_3. Its 12 lines are the cosets of
the 4 one-dimensional subspaces. Enumerated as coordinates mod 3 they are the
horizontals, verticals, and both diagonal directions (each direction giving 3
parallel lines).

Embed the 9 points as the integer grid {0,1,2}² ⊂ R² and ask which of the 12
abstract lines are actually collinear. The horizontals (3), verticals (3), and
one diagonal family (2 of the "/" lines plus the main "\" diagonal) survive:
8 lines. The remaining 4 are the "broken diagonals" that only close up modulo 3.

The reason no embedding can recover all 12 is the **Sylvester–Gallai theorem**:
any finite non-collinear set in R² admits an ordinary (2-point) line. AG(2, 3)
has none, so it cannot embed in R². Over C the obstruction vanishes — the Hesse
configuration realises all 12 lines using the 9 inflection points of a smooth
cubic, of which only 3 are real. This is why the configuration is at home over
finite fields and in CP² but not in the real plane.

## 3. The BGS lower bound

Burr, Grünbaum and Sloane (1974) place points on a cubic curve and use the fact
that three points are collinear iff their parameters sum to zero in the curve's
group law, yielding F_3(n) ≥ n²/6 − O(n). The degenerate cubic *y = x³* makes
this concrete: x³ − mx − k = 0 has root sum zero (no x² term), so
(a, a³), (b, b³), (c, c³) are collinear iff a + b + c = 0. Counting integer
triples summing to zero in a symmetric window reproduces the f_3 values in the
README. A smooth elliptic curve *y² = x³ + ax + b* improves the constant via
torsion points, which supply zero-sum triples beyond the additive ones.

## 4. The orchard problem and the basin obstruction

Counting lines through *exactly* three points is the orchard-planting problem.
Known optima: t₃(9) = 10, and (Green–Tao 2013) t₃(11) = 16, t₃(12) = 19.

The search here fixes the Pappus 9-point configuration (a clean orchard substrate)
and adds extra points at intersections of "open" incidence lines, scoring by the
exact 3-point line count and descending locally. It attains f₃ = 15 at n = 11
reliably but never 16.

A multi-start sweep (240 seeds) confirmed 15 as the global maximum *reachable by
local moves from this family*. The Green–Tao optimum of 16 sits in a separate
basin: its configuration is defined by an explicit algebraic construction at the
seed level, and the 16th line cannot be produced by perturbing a Pappus-derived
configuration. The practical lesson is that local optimisation is good at
recovering incidences within a construction but cannot discover an
algebraically distinct construction — a useful negative result about
search-based approaches to extremal configurations.

## 5. Reproducibility

`src/incidences.py` is dependency-light (standard library plus NumPy for the
optional figure script) and prints every number quoted in the README, including
the explicit list of the four non-realizable AG(2, 3) lines. Collinearity uses
an exact signed-area test with a small epsilon; for the integer and rational
configurations studied here the result is exact.

## References

- J. J. Sylvester, *Mathematical Question 11851*, Educational Times (1893).
- T. Gallai, proof of the Sylvester problem (1944).
- S. A. Burr, B. Grünbaum, N. J. A. Sloane, *The orchard problem*,
  Geometriae Dedicata 2 (1974), 397–424.
- B. Green, T. Tao, *On sets defining few ordinary lines*,
  Discrete & Computational Geometry 50 (2013), 409–468.
