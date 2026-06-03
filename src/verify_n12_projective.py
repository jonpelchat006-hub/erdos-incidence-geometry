"""
Verifying an optimal orchard configuration at n = 12: f_3 = 19.

The orchard-planting problem asks for the maximum number of lines through
exactly three of n points. The proven optimum at n = 12 is t_3(12) = 19
(Green-Tao, 2013). This script exhibits a configuration that ATTAINS that
optimum and verifies it independently, at strict tolerance.

The construction is projective: 11 ordinary points in the plane plus one
point at infinity (the vertical direction, homogeneous coordinates (0, 1, 0)).
A point at infinity is legitimate in the orchard problem -- the problem lives
in the projective plane, and this configuration is projectively equivalent to
12 ordinary points (a projective transformation slides the point at infinity
to a finite position without changing a single incidence, because the line at
infinity contains only that one configuration point).

The 19 decomposes as 15 + 4:
  * 15 ordinary 3-point lines among the 11 affine points, and
  * 4 lines, each a vertically-aligned pair of affine points together with
    the vertical point at infinity.

IMPORTANT: 19 is the proven MAXIMUM at n = 12. This matches the record; it
does not beat it (it cannot be beaten). The value of this script is an
independent, strict-tolerance confirmation that the configuration is genuine
and not a loose-tolerance artifact.

Run:
    python src/verify_n12_projective.py
"""

from itertools import combinations
import numpy as np


# 11 affine points: a slanted Pappus 9-point configuration plus 2 extras
# placed at algebraic intersection clusters. Full-precision doubles so the
# collinearities hold under strict tolerance.
AFFINE = np.array([
    (0.0,                1.0),
    (1.0,                1.0),
    (2.0,                1.0),
    (0.0,               -1.0),
    (1.0,               -0.3819660112501052),
    (2.0,                0.23606797749978958),
    (0.5913719988157784, 0.1827439976315568),
    (1.447213595499958,  0.44721359549995776),
    (1.6440035777631468, 0.5080250443420277),
    (1.31943828249997,   0.6051525682142556),
    (1.3194382824999702, 0.21030513642851156),
], dtype=float)

# The "bouncing drop": one point at infinity in the vertical direction.
IDEAL = np.array([(0.0, 1.0, 0.0)])


def homogeneous(affine):
    """Affine points (x, y) -> unit-normalized homogeneous (x, y, 1)."""
    h = np.hstack([affine, np.ones((len(affine), 1))])
    return h / np.linalg.norm(h, axis=1, keepdims=True)


def count_exact_3_lines(points_h, tol):
    """
    Count lines through exactly 3 points using homogeneous collinearity.
    Point k lies on the line through i, j iff |p_k . (p_i x p_j)| < tol.
    Returns (f3, f4plus).
    """
    n = len(points_h)
    maximal = set()
    for i, j in combinations(range(n), 2):
        line = np.cross(points_h[i], points_h[j])
        nrm = np.linalg.norm(line)
        if nrm < 1e-14:
            continue
        line = line / nrm
        on = tuple(k for k in range(n) if abs(points_h[k] @ line) < tol)
        maximal.add(tuple(sorted(on)))
    f3 = sum(1 for s in maximal if len(s) == 3)
    f4plus = sum(1 for s in maximal if len(s) >= 4)
    return f3, f4plus


def main():
    affine_h = homogeneous(AFFINE)
    projective_h = np.vstack([affine_h, IDEAL / np.linalg.norm(IDEAL)])

    print("=" * 64)
    print("n = 12 orchard configuration: 11 affine points + 1 point at infinity")
    print("Proven optimum: t_3(12) = 19 (Green-Tao, 2013)")
    print("=" * 64)

    print("\nProjective count (all 12 points), across tolerances:")
    print("  {:>12}  {:>5}  {:>13}".format("tolerance", "f_3", "lines>=4 pts"))
    passed = True
    for tol in (1e-4, 1e-6, 1e-8, 1e-10):
        f3, f4 = count_exact_3_lines(projective_h, tol)
        print("  {:>12}  {:>5}  {:>13}".format(tol, f3, f4))
        if f3 != 19 or f4 != 0:
            passed = False

    print("\nAffine-only count (the 11 ordinary points), for the decomposition:")
    for tol in (1e-6, 1e-8, 1e-10):
        f3a, f4a = count_exact_3_lines(affine_h, tol)
        print("  tol={:<8}  f_3 = {}   (>=4-pt lines: {})".format(tol, f3a, f4a))

    print("\nDecomposition: 15 ordinary 3-point lines + 4 vertical pairs")
    print("through the point at infinity = 19.")
    verdict = "PASS - matches the proven t_3(12)=19 optimum." if passed else "FAIL"
    print("\nVERDICT:", verdict)


if __name__ == "__main__":
    main()
