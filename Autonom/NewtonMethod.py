import numpy as np
from copy import deepcopy
from time import monotonic
from scipy.optimize import fsolve

A = [5, 3, 2]
B = [10, 7, 2]
C = [2, 5, 2]

DA = pow(6, 0.5)
DB = 7
DC = 3

S = np.array([1, 1, 1], dtype=np.float64)


def f(p):
    x, y, z = p
    x1 = (A[0] - x)**2 + (A[1] - y)**2 + (A[2] - z)**2 - DA**2
    x2 = (B[0] - x)**2 + (B[1] - y)**2 + (B[2] - z)**2 - DB**2
    x3 = (C[0] - x)**2 + (C[1] - y)**2 + (C[2] - z)**2 - DC**2
    return np.array([x1, x2, x3])


def J(p):
    x, y, z = p
    return np.array([
        [2 * (A[0] - x), 2 * (A[1] - y), 2 * (A[2] - z)],
        [2 * (B[0] - x), 2 * (B[1] - y), 2 * (B[2] - z)],
        [2 * (C[0] - x), 2 * (C[1] - y), 2 * (C[2] - z)]])


if __name__ == "__main__":
    s = deepcopy(S)
    t1 = monotonic()
    for i in range(8):
        print("s:", s)
        j_inv = np.linalg.inv(J(s))
        dx = np.matmul(j_inv, (-f(s)))
        s = s - dx
    print(monotonic() - t1)

    print("scipy")

    t1 = monotonic()
    s = fsolve(f, (0, 0, 0))
    print(monotonic() - t1)
    print(s)
