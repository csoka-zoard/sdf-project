from d import d_segment_signed_with_outvecs, d_quad_bezier_signed_with_outvecs
from grid import Grid
from functools import lru_cache

def sd_curve_with_outvecs(p, curve, ctx):
    if len(curve) == 2:
        return d_segment_signed_with_outvecs(p, curve, ctx)
    else:
        return d_quad_bezier_signed_with_outvecs(p, curve, ctx)

def gridSDF(p, ctx, grid):
    @lru_cache(maxsize=None)
    def sd(i):
        return sd_curve_with_outvecs(p, grid.nth_bezier(i), ctx)[0]

    b_ind, r0 = grid.box_ind(p)
    n = 0
    while True:
        relevant_curve_inds, r = grid.nth_circle(n, b_ind, r0)
        relevant_dists = [sd(i) for i in relevant_curve_inds]
        closest = min(relevant_dists, key = abs) if len(relevant_dists) > 0 else float('inf')
        if abs(closest) <= r:
            return closest
        n = n + 1
