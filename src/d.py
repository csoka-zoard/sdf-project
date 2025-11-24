import numpy as np

_eps = 1e-12

def normalize(vec):
    l = np.linalg.norm(vec)
    return vec / l

def zero_ish(vec):
    l = np.linalg.norm(vec)
    return l <= _eps

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def norm2(v):
    return np.sqrt(dot(v, v))

def d(a, b):
    return norm2(a - b)

def d_segment(p, curve):
    a = curve[0]
    b = curve[1]
    ab = b - a
    ap = p - a

    epsilon = 1e-8
    dab = dot(ab, ab)
    if abs(dab) > epsilon:
      t = dot(ap, ab) / dab
      q = a + t * ab
      if t <= 0:
          return d(p, a)
      elif t >= 1:
          return d(p, b)
      else:
          return d(p, q)
    else:
        return d(p, a)

def d_quad_bezier(p, curve): # AI (ChatGPT), based on tests, seems correct
    """Unsigned distance from point p to quadratic Bezier (P0, P1, P2)."""
    P0, P1, P2 = [np.array(pt, dtype=np.float64) for pt in curve]
    p = np.array(p, dtype=np.float64)

    # Coefficients for B(t) = A t^2 + B t + C
    A = P0 - 2*P1 + P2
    B = 2*(P1 - P0)
    C = P0 - p

    # f(t) = ||A t^2 + B t + C||^2
    # f'(t) = 2*(A·A)t^3 + 3*(A·B)t^2 + 2*(A·C + B·B/2)t + B·C = 0
    a = 2*np.dot(A, A)
    b = 3*np.dot(A, B)
    c = 2*np.dot(A, C) + np.dot(B, B)
    d = np.dot(B, C)

    # Solve cubic a*t^3 + b*t^2 + c*t + d = 0
    coeffs = [a, b, c, d]
    roots = np.roots(coeffs)

    # Consider only real roots in [0, 1]
    ts = [0.0, 1.0]
    for r in roots:
        if np.isreal(r):
            t = np.real(r)
            if 0.0 <= t <= 1.0:
                ts.append(t)

    # Evaluate distances
    def B(t): return (1 - t)**2 * P0 + 2*(1 - t)*t * P1 + t**2 * P2
    dists = [np.linalg.norm(B(t) - p) for t in ts]

    return min(dists)


def perp(v):
    # 2d perpendicular
    return np.array([-v[1], v[0]])

def sign_of_cross(tangent, v):
    """-1, 0, or -1 depending on cross product's sign"""
    c = tangent[0]*v[1] - tangent[1]*v[0]
    if c > 0: return 1
    if c < 0: return -1
    return 0

def closest_point_on_segment_and_t(p, seg):
    a = np.array(seg[0], dtype=np.float64)
    b = np.array(seg[1], dtype=np.float64)
    ab = b - a
    dab = np.dot(ab, ab)
    if dab < _eps:
        return a, 0.0  # degenerate -> at A
    t = np.dot(p - a, ab) / dab
    t_clamped = max(0.0, min(1.0, t))
    q = a + t_clamped * ab
    return q, t_clamped

def d_segment_signed(p, seg):
    """Return signed distance to a segment: (signed_distance, foot_point, t)."""
    a = np.array(seg[0], dtype=np.float64)
    b = np.array(seg[1], dtype=np.float64)
    q, t = closest_point_on_segment_and_t(p, seg)
    dist = np.linalg.norm(p - q)

    tangent = b - a
    s = sign_of_cross(tangent, p - q)

    # if interior foot, we can determine sign from tangent
    if t > _eps and t < 1.0 - _eps:
        
        # tangent normalization not necessary for sign
        if s == 0:
            # numeric collinear: treat as outside (or fallback to winding below)
            return dist, 0, q, t
        return s * dist, s, q, t
    else:
        return s * dist, s, q, t

# Quadratic bezier helpers

def bezier_point(P0, P1, P2, t):
    return (1.0 - t)**2 * P0 + 2*(1.0 - t)*t * P1 + t**2 * P2

def bezier_tangent(P0, P1, P2, t):
    # derivative B'(t) = 2*( (1-t)*(P1 - P0) + t*(P2 - P1) )
    return 2.0 * ((1.0 - t)*(P1 - P0) + t*(P2 - P1))

def closest_t_on_quadratic_bezier(p, curve):
    """Return t in [0,1] that minimizes distance; this uses your cubic root solver approach."""
    P0, P1, P2 = [np.array(pt, dtype=np.float64) for pt in curve]
    p = np.array(p, dtype=np.float64)

    A = P0 - 2*P1 + P2
    B = 2*(P1 - P0)
    C = P0 - p

    a = 2*np.dot(A, A)
    b = 3*np.dot(A, B)
    c = 2*np.dot(A, C) + np.dot(B, B)
    d = np.dot(B, C)

    if abs(a) < _eps:
        # Degenerate to linear (tangent constant) -> treat as line from P0 to P2
        # Solve quadratic or fallback to endpoints
        ts = [0.0, 1.0]
    else:
        coeffs = [a, b, c, d]
        roots = np.roots(coeffs)
        ts = [0.0, 1.0]
        for r in roots:
            if np.isreal(r):
                t = float(np.real(r))
                if -_eps <= t <= 1.0 + _eps:
                    ts.append(max(0.0, min(1.0, t)))
    # deduplicate near-equal t
    ts = sorted(set([round(t,10) for t in ts]))
    best_t = None
    best_dist = None
    for t in ts:
        q = bezier_point(P0, P1, P2, t)
        dist = np.linalg.norm(q - p)
        if best_dist is None or dist < best_dist:
            best_dist = dist
            best_t = t
    return best_t


def d_quad_bezier_signed(p, curve):
    """Return (signed_distance, sign, foot_point, t). sign==0 means ambiguous->fall back."""
    P0, P1, P2 = [np.array(pt, dtype=np.float64) for pt in curve]
    p = np.array(p, dtype=np.float64)

    t = closest_t_on_quadratic_bezier(p, (P0, P1, P2))
    q = bezier_point(P0, P1, P2, t)
    dist = np.linalg.norm(p - q)

    # If t interior, use curve tangent to determine sign
    if t > _eps and t < 1.0 - _eps:
        tangent = bezier_tangent(P0, P1, P2, t)
        if np.linalg.norm(tangent) < _eps:
            # degenerate tangent -> ambiguous
            return dist, 0, q, t
        s = sign_of_cross(tangent, p - q)
        if s == 0:
            return dist, 0, q, t
        return s * dist, s, q, t
    else:
        # Endpoint case: still determine sign from tangent at endpoint
        # TODO: COMPUTE WITH outvecs
        if t <= _eps:
            tangent = P1 - P0
        else:
            tangent = P2 - P1
        if np.linalg.norm(tangent) < _eps:
            return dist, 0, q, t
        s = sign_of_cross(tangent, p - q)
        if s == 0:
            return dist, 0, q, t
        return s * dist, s, q, t

def sign(x):
    if x < 0:
        return -1
    else:
        return 1

def d_endpoint(p, t, P_first, P_last, ctx):
    P = 0
    if t <= _eps:
        P = P_first
        t = 0.0
    else: # t >= 1.0 - _eps
        P = P_last
        t = 1.0
    dist = np.linalg.norm(P - p)
    Pf = (float(P[0]), float(P[1]))
    outvec = ctx.outs.vecs[Pf]
    #print(Pf, outvec)
    c = dot(outvec, P - p)
    s = sign(c)
    return s * dist, s, P, t

def d_quad_bezier_signed_with_outvecs(p, curve, ctx):
    P0, P1, P2 = [np.array(pt, dtype=np.float64) for pt in curve]
    p = np.array(p, dtype=np.float64)

    t = closest_t_on_quadratic_bezier(p, (P0, P1, P2))
    q = bezier_point(P0, P1, P2, t)
    dist = np.linalg.norm(p - q)

    if t > _eps and t < 1.0 - _eps:
        tangent = bezier_tangent(P0, P1, P2, t)
        if np.linalg.norm(tangent) < _eps:
            return dist, 0, q, t
        s = sign_of_cross(tangent, p - q)
        if s == 0:
            return dist, 0, q, t
        return s * dist, s, q, t
    else:
        return d_endpoint(p, t, P0, P2, ctx)

def d_segment_signed_with_outvecs(p, seg, ctx):
    a = np.array(seg[0], dtype=np.float64)
    b = np.array(seg[1], dtype=np.float64)
    q, t = closest_point_on_segment_and_t(p, seg)
    dist = np.linalg.norm(p - q)

    tangent = b - a
    s = sign_of_cross(tangent, p - q)

    if t > _eps and t < 1.0 - _eps:
        if s == 0:
            return dist, 0, q, t
        return s * dist, s, q, t
    else:
        return d_endpoint(p, t, a, b, ctx)
