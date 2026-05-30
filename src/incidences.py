"""
Line incidences on small planar point configurations.

For a set of points P in R^2:
    F_k(n) = number of lines passing through >= k of the points
    f_k(n) = number of lines passing through exactly k of the points

Trivial upper bound (each pair of points lies on at most one line, and a
k-point line consumes C(k, 2) pairs):

    F_k(n) <= C(n, 2) / C(k, 2)

For n = 9, k = 3 this gives F_3(9) <= 36 / 3 = 12.

This module provides exact incidence counting and uses it to study a classic
question: can the affine plane AG(2, 3) -- 9 points, 12 lines of 3, which
saturates the bound above -- be realized as 9 actual points in R^2? It cannot,
and the obstruction is the Sylvester-Gallai theorem. The code quantifies the
gap and verifies the Burr-Grunbaum-Sloane lower-bound construction.
"""

from itertools import combinations
from collections import defaultdict
from math import comb


# --- Collinearity and line bookkeeping --------------------------------------

def line_key(p, q, eps=1e-9):
    """Canonical key (a, b, c) for the line ax + by + c = 0 through p and q."""
    a = q[1] - p[1]
    b = p[0] - q[0]
    c = q[0] * p[1] - p[0] * q[1]
    norm = max(abs(a), abs(b), abs(c))
    if norm < eps:
        return None
    a, b, c = a / norm, b / norm, c / norm
    # Sign normalization: first nonzero coefficient positive.
    for x in (a, b, c):
        if abs(x) > eps:
            if x < 0:
                a, b, c = -a, -b, -c
            break
    return (round(a, 9), round(b, 9), round(c, 9))


def collinear(p, q, r, eps=1e-9):
    """True if p, q, r are collinear (signed-area test)."""
    return abs((q[0] - p[0]) * (r[1] - p[1]) -
               (q[1] - p[1]) * (r[0] - p[0])) < eps


def lines_through_points(points, eps=1e-9):
    """
    Returns:
        line_to_pts: dict mapping a canonical line key -> sorted tuple of the
                     indices of all points on that line.
        histogram:   dict mapping k -> number of lines through exactly k points.
    """
    n = len(points)
    line_to_pts = defaultdict(set)
    for i, j in combinations(range(n), 2):
        key = line_key(points[i], points[j], eps)
        if key is None:
            continue
        line_to_pts[key].add(i)
        line_to_pts[key].add(j)

    # Absorb any further points that happen to lie on an existing line.
    for key, pts_on_line in list(line_to_pts.items()):
        anchor = list(pts_on_line)[:2]
        p, q = points[anchor[0]], points[anchor[1]]
        for k in range(n):
            if k in pts_on_line:
                continue
            if collinear(p, q, points[k], eps):
                line_to_pts[key].add(k)

    histogram = defaultdict(int)
    for pts_on_line in line_to_pts.values():
        histogram[len(pts_on_line)] += 1

    return {k: tuple(sorted(v)) for k, v in line_to_pts.items()}, dict(histogram)


def report(name, points, eps=1e-9):
    """Print the incidence profile of a configuration and return it."""
    lines, hist = lines_through_points(points, eps)
    n = len(points)
    print(f"\n=== {name} (n={n}) ===")
    print(f"  Total lines (>=2 pts): {len(lines)}")
    for k in sorted(hist):
        print(f"    f_{k} (lines through exactly {k} pts): {hist[k]}")
    keys = sorted(hist)
    for k in (2, 3, 4):
        Fk = sum(hist[j] for j in keys if j >= k)
        print(f"  F_{k} (lines through >= {k} pts): {Fk}")
    print(f"  Trivial bound F_3 <= C(n,2)/C(3,2) = {comb(n, 2) // 3}")
    return lines, hist


# --- Reference configurations -----------------------------------------------

# The natural 3x3 integer grid.
grid_3x3 = [(i, j) for i in range(3) for j in range(3)]

# Nine points on the cubic y = x^3. Three points (a, a^3), (b, b^3), (c, c^3)
# are collinear iff a + b + c = 0 (Vieta on x^3 - mx - k = 0). This is the
# Burr-Grunbaum-Sloane (BGS) lower-bound construction in its simplest form.
cubic_n9 = [(x, x ** 3) for x in range(-4, 5)]

# The same construction at n = 12, where it begins to pull ahead of the grid.
cubic_n12 = [(x, x ** 3) for x in range(-5, 7)]


def perturbed_grid(eps=0.0):
    """3x3 grid with a small radial perturbation -- a degeneracy sanity check."""
    pts = []
    for i in range(3):
        for j in range(3):
            r = 1 + eps * ((i - 1) ** 2 + (j - 1) ** 2)
            pts.append((i * r, j * r))
    return pts


# --- AG(2, 3): the abstract affine plane over F_3 ---------------------------

def ag23_lines():
    """The 12 lines of AG(2, 3) as triples of (i, j) coordinates mod 3."""
    points = [(i, j) for i in range(3) for j in range(3)]
    seen = set()
    lines = []
    for p in points:
        for q in points:
            if p == q:
                continue
            di = (q[0] - p[0]) % 3
            dj = (q[1] - p[1]) % 3
            line = [((p[0] + t * di) % 3, (p[1] + t * dj) % 3) for t in range(3)]
            fs = frozenset(line)
            if fs in seen:
                continue
            seen.add(fs)
            lines.append(sorted(line))
    return lines


def realized_in_R2(line_3pts, eps=1e-9):
    """Does an AG(2,3) line (3 grid points) lie on a real line in R^2?"""
    p, q, r = line_3pts
    return collinear(p, q, r, eps)


# --- Driver -----------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("NINE-POINT CONFIGURATIONS")
    print("=" * 60)
    report("3x3 integer grid", grid_3x3)
    report("9 points on the cubic y = x^3 (BGS)", cubic_n9)
    report("Perturbed grid (eps=0.05)", perturbed_grid(0.05))

    print("\n" + "=" * 60)
    print("AG(2,3): ABSTRACT vs. REAL REALIZATION")
    print("=" * 60)
    abstract = ag23_lines()
    realized = [L for L in abstract if realized_in_R2(L)]
    unrealized = [L for L in abstract if not realized_in_R2(L)]
    print(f"AG(2,3) has {len(abstract)} abstract lines of 3 points each.")
    print(f"{len(realized)} are collinear once the grid is embedded in R^2;")
    print(f"{len(unrealized)} are not -- the gap forced by Sylvester-Gallai:")
    for L in unrealized:
        print(f"  {L}")

    print("\n" + "=" * 60)
    print("BGS SCALING CHECK AT n=12")
    print("=" * 60)
    report("12 points on the cubic y = x^3", cubic_n12)
