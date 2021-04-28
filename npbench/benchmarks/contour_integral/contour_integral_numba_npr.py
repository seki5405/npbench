# Copyright 2021 ETH Zurich and the NPBench authors. All rights reserved.

import numpy as np
import numba as nb


@nb.jit(nopython=True, parallel=True, fastmath=True)
def contour_integral(NR, NM, slab_per_bc, Ham, int_pts, Y):
    P0 = np.zeros((NR, NM), dtype=np.complex128)
    P1 = np.zeros((NR, NM), dtype=np.complex128)
    # for z in int_pts:
    for i in nb.prange(len(int_pts)):
        z = int_pts[i]
        Tz = np.zeros((NR, NR), dtype=np.complex128)
        for n in nb.prange(slab_per_bc + 1):
            zz = np.power(z, slab_per_bc / 2 - n)
            Tz += zz * Ham[n]
        if NR == NM:
            X = np.linalg.inv(Tz)
        else:
            X = np.linalg.solve(Tz, Y)
        if abs(z) < 1.0:
            X = -X
        P0 += X
        P1 += z * X

    return P0, P1
