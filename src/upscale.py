import numpy as np
import math

def bilinear_sample(sdf, n, x, y):
    step = 2.0 / n
    i_f = (1.0 - y) / step - 0.5
    j_f = (1.0 - x) / step - 0.5
    i0 = int(np.floor(i_f))
    j0 = int(np.floor(j_f))
    i1 = i0 + 1
    j1 = j0 + 1
    # clamp
    i0c = max(0, min(n-1, i0))
    i1c = max(0, min(n-1, i1))
    j0c = max(0, min(n-1, j0))
    j1c = max(0, min(n-1, j1))
    # weights
    ti = i_f - i0
    tj = j_f - j0
    # fetch values
    v00 = sdf[(i0c, j0c)]
    v10 = sdf[(i1c, j0c)]
    v01 = sdf[(i0c, j1c)]
    v11 = sdf[(i1c, j1c)]
    # bilin. interpol.
    v0 = v00 * (1 - ti) + v10 * ti
    v1 = v01 * (1 - ti) + v11 * ti
    return v0 * (1 - tj) + v1 * tj


def upscale_sdf(sdf_small, n, m):
    sdf_large = {}
    step_large = 2.0 / m
    for i in range(m):
        y = 1.0 - (i + 0.5) * step_large
        for j in range(m):
            x = 1.0 - (j + 0.5) * step_large
            val = bilinear_sample(sdf_small, n, x, y)
            sdf_large[(i, j)] = float(val)
    return sdf_large


def sdf_diff(sdf1, sdf2):
    n1 = int(math.isqrt(len(sdf1)))
    n2 = int(math.isqrt(len(sdf2)))
    if n1 != n2:
        raise Exception("Error.")
    sdf_diff = {}
    for i in range(n1):
        for j in range(n1):
            sdf_diff[(i, j)] = abs(sdf1[(i, j)] - sdf2[(i, j)])
    return sdf_diff