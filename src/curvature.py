import numpy as np

def B_segment(curve, t):
    P0 = curve[0]
    P1 = curve[1]
    Q0 = t * P0 + (1 - t) * P1
    return (float(Q0[0]), float(Q0[1])), 0

def B_quad(curve, t):
    P0 = curve[0]
    P1 = curve[1]
    P2 = curve[2]
    Q0 = t * P0 + (1 - t) * P1
    Q1 = t * P1 + (1 - t) * P2
    R0 = t * Q0 + (1 - t) * Q1
    # B'
    dB = 2 * ((1 - t) * (P1 - P0) + t * (P2 - P1))
    # B''
    ddB = 2 * (P2 - 2 * P1 + P0)

    numer = dB[0] * ddB[1] - dB[1] * ddB[0]
    denom = (dB[0]**2 + dB[1]**2)**1.5
    kappa = np.abs(numer) / denom # if denom > 1e-12 else 0.0
    return (float(R0[0]), float(R0[1])), kappa

def B(curve, fn, n, ret):
    for i in range(n + 1):
        t = float(i) / float(n)
        ret.append(fn(curve, t))

def curvature(ctx): # [((x, y), kappa)]
    ret = []
    detail = 100
    for seg in ctx.segments:
        B(seg, B_segment, detail, ret)
    for qd in ctx.curves:
        B(qd, B_quad, detail, ret)
    return ret

def sdf_gradient(sdf, n):
    step = 2.0 / n
    grad = {}
    for i in range(n):
        for j in range(n):
            im1 = max(i - 1, 0)
            ip1 = min(i + 1, n - 1)
            jm1 = max(j - 1, 0)
            jp1 = min(j + 1, n - 1)

            sL = sdf[(i, jm1)]   # left
            sR = sdf[(i, jp1)]   # right
            sD = sdf[(ip1, j)]   # down
            sU = sdf[(im1, j)]   # up

            # centrális differencia
            gx = (sR - sL) / (2.0 * step)
            gy = (sU - sD) / (2.0 * step)

            grad[(i, j)] = (gx, gy)
    return grad
