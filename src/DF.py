from d import d_segment_signed_with_outvecs, d_quad_bezier_signed_with_outvecs

# def UDF(p, ctx): # Unsigned Distance Field
#     minl = min([d_segment(p, seg) for seg in ctx.segments])
#     minc = min([d_quad_bezier(p, seg) for seg in ctx.curves])
#     return min(minl, minc)


def SDF(p, ctx): # SIGNED DISTANCE FIELD
    seg_dists = [d_segment_signed_with_outvecs(p, seg, ctx)[0] for seg in ctx.segments]
    curve_dists = [d_quad_bezier_signed_with_outvecs(p, curve, ctx)[0] for curve in ctx.curves]
    all_dists = seg_dists + curve_dists
    best = min(all_dists, key=abs)
    return best
