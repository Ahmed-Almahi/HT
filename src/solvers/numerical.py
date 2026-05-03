import numpy as np
from scipy.linalg import solve_banded

def solve_implicit_fdm_slab(obj, nodes, dt, total_time):
    """
    Implicit FDM (Backward Euler) for a plane wall (slab) of thickness 2*Lc.
    Symmetry at x=0, convection at x=Lc.
    Compatible with lecture notes (Heisler charts, one-term approximation).
    """
    if total_time <= 0:
        return np.full(nodes, obj.Ti, dtype=float)

    L = obj.Lc
    dx = L / (nodes - 1)
    Fo = obj.alpha * dt / dx**2
    # Implicit is unconditionally stable, but keep Fo not huge for accuracy
    Fo = min(Fo, 10.0)

    # Precompute r values (x positions)
    x = np.linspace(0, L, nodes)
    T = np.full(nodes, obj.Ti, dtype=float)
    steps = int(total_time / dt)

    for _ in range(steps):
        A = np.zeros((3, nodes))
        B = np.zeros(nodes)
        for i in range(nodes):
            if i == 0:
                # Symmetry at x=0: T0 = T1  -> T0 - T1 = 0
                A[1, 0] = 1.0
                A[2, 0] = -1.0
                B[0] = 0.0
            elif i == nodes - 1:
                # Convection at x=L: -k dT/dx = h (T - Tinf)
                # Using backward difference: -k (T_{N-1} - T_{N-2})/dx = h (T_{N-1} - Tinf)
                # Rearranged: (1 + Bi_dx) T_{N-1} - T_{N-2} = Bi_dx Tinf
                Bi_dx = obj.h * dx / obj.k
                A[1, i] = 1.0 + Bi_dx
                A[0, i] = -1.0
                B[i] = Bi_dx * obj.T_inf
            else:
                # Interior nodes (Cartesian, slab)
                # Discretization: (1+2Fo) T_i^{n+1} - Fo T_{i-1}^{n+1} - Fo T_{i+1}^{n+1} = T_i^n
                a = Fo
                A[1, i] = 1.0 + 2.0 * a
                A[0, i] = -a
                A[2, i] = -a
                B[i] = T[i]
        T = solve_banded((1, 1), A, B)
        T[0] = T[1]   # enforce symmetry
    return T


def solve_implicit_fdm_cylinder(obj, nodes, dt, total_time):
    """
    Implicit FDM for an infinitely long cylinder (radial coordinate).
    Symmetry at r=0, convection at r=R.
    Compatible with lecture notes (Bessel functions, Heisler charts).
    """
    if total_time <= 0:
        return np.full(nodes, obj.Ti, dtype=float)

    R = obj.Lc
    dr = R / (nodes - 1)
    Fo = obj.alpha * dt / dr**2
    Fo = min(Fo, 10.0)   # implicit stable, but keep reasonable

    r = np.linspace(0, R, nodes)
    r[0] = 1e-12   # avoid division by zero
    T = np.full(nodes, obj.Ti, dtype=float)
    steps = int(total_time / dt)

    for _ in range(steps):
        A = np.zeros((3, nodes))
        B = np.zeros(nodes)
        for i in range(nodes):
            if i == 0:
                # Symmetry at r=0: T0 = T1
                A[1, 0] = 1.0
                A[2, 0] = -1.0
                B[0] = 0.0
            elif i == nodes - 1:
                # Convection at r=R: -k dT/dr = h (T - Tinf)
                Bi_dr = obj.h * dr / obj.k
                A[1, i] = 1.0 + Bi_dr
                A[0, i] = -1.0
                B[i] = Bi_dr * obj.T_inf
            else:
                # Interior nodes for cylinder: 1D radial with variable coefficients
                a = Fo
                r_i = r[i]
                # Discretization: (1 + 2Fo + Fo*dr/(2r_i)) T_i - Fo(1 - dr/(2r_i)) T_{i-1} - Fo(1 + dr/(2r_i)) T_{i+1} = T_i_old
                A[1, i] = 1.0 + 2.0 * a + a * dr / (2.0 * r_i)
                A[0, i] = -a * (1.0 - dr / (2.0 * r_i))
                A[2, i] = -a * (1.0 + dr / (2.0 * r_i))
                B[i] = T[i]
        T = solve_banded((1, 1), A, B)
        T[0] = T[1]
    return T


def solve_implicit_fdm_sphere(obj, nodes, dt, total_time):
    """
    Implicit FDM for a sphere (radial coordinate).
    Symmetry at r=0, convection at r=R.
    Fully compatible with lecture notes (sinusoidal eigenfunctions, Heisler charts).
    """
    if total_time <= 0:
        return np.full(nodes, obj.Ti, dtype=float)

    R = obj.Lc
    dr = R / (nodes - 1)
    Fo = obj.alpha * dt / dr**2
    Fo = min(Fo, 10.0)   # implicit stable

    r = np.linspace(0, R, nodes)
    r[0] = 1e-12
    T = np.full(nodes, obj.Ti, dtype=float)
    steps = int(total_time / dt)

    for _ in range(steps):
        A = np.zeros((3, nodes))
        B = np.zeros(nodes)
        for i in range(nodes):
            if i == 0:
                # Symmetry: T0 = T1
                A[1, 0] = 1.0
                A[2, 0] = -1.0
                B[0] = 0.0
            elif i == nodes - 1:
                # Convection boundary: -k dT/dr = h (T - Tinf)
                Bi_dr = obj.h * dr / obj.k
                A[1, i] = 1.0 + Bi_dr
                A[0, i] = -1.0
                B[i] = Bi_dr * obj.T_inf
            else:
                a = Fo
                r_i = r[i]
                # Spherical coordinates: coefficient includes 2*dr/r terms
                A[1, i] = 1.0 + 2.0 * a + 2.0 * a * dr / r_i
                A[0, i] = -a * (1.0 - dr / r_i)
                A[2, i] = -a * (1.0 + dr / r_i)
                B[i] = T[i]
        T = solve_banded((1, 1), A, B)
        T[0] = T[1]
    return T


def solve_implicit_fdm_semi_sphere(obj, nodes, dt, total_time):
    """
    Semi-sphere (dome) with insulated base. 
    Identical to full sphere because the base is adiabatic and the problem is spherically symmetric.
    Provided for convenience; simply calls solve_implicit_fdm_sphere.
    """
    return solve_implicit_fdm_sphere(obj, nodes, dt, total_time)