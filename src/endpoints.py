from d import *

def rot(vec):
    return np.array([-vec[1], vec[0]])

def combine_vecs(vec1, vec2):
    v1 = normalize(vec1)
    v2 = normalize(vec2)
    v = v1 + v2
    if zero_ish(v):
        return rot(v1)
    else:
        return normalize(v)

def sd_curve(p, curve):
    if len(curve) == 3:
        return d_quad_bezier_signed(p, curve)
    else:
        return d_segment_signed(p, curve)

class Outvectors:
    def __init__(self):
        self.vecs = dict()
        self.i = 0
        self.k = 0 # At the end 2i = k must hold, or there's an error.
        self.curves = dict()
        self.ps = dict()

    def add_vec(self, point, vec, curve): # any endpoint must appear twice and exactly twice in our shape
        self.k = self.k + 1
        p = point
        point = (float(p[0]), float(p[1])) # so its hashable
        self.ps[point] = p
        if point in self.vecs: # I am assuming floats are exactly equal, because at this point we did no calculations with them
            self.i = self.i + 1
            v = combine_vecs(self.vecs[point], vec)
            self.vecs[point] = v if 0.0 > sd_curve(p + v, self.curves[point])[0] else -v
            #print(self.i, point, self.vecs[point])
        else:
            self.curves[point] = curve
            self.vecs[point] = vec

    def add_end(self, point, vec, curve):
        self.add_vec(point, vec, curve)

    def add_beg(self, point, vec, curve):
        self.add_vec(point, -vec, curve)

    def rescale(self, bbox_center, bbox_scale): # HAS TO BE COMPUTED THE EXACT SAME WAY AS THE RESCALING OF THE CURVES, ELSE LOOKUP WOULD NOT WORK
        new_outs = dict()
        for p1, p2 in self.vecs:
            point = (p1, p2)
            outv = self.vecs[point]
            p = self.ps[point]
            p = np.array(p, np.float32)
            p = (p - bbox_center) / bbox_scale
            p = (float(p[0]), float(p[1]))
            outv_scaled = outv / bbox_scale
            new_outs[p] = normalize(outv_scaled)
            #print(p, outv_scaled)
        self.vecs = new_outs