from Ctx import Ctx
import math

def empty_grid(N):
    ret = dict()
    for i in range(N):
        for j in range(N):
            ret[(i, j)] = set()
    return ret

def box(seg_or_curve):
    xs = [p[0] for p in seg_or_curve]
    ys = [p[1] for p in seg_or_curve]
    return ((min(xs), min(ys)),
            (max(xs), max(ys)))

def rescale(p):
    return ((p[0] + 1.0) / 2.0, (p[1] + 1.0) / 2.0)

def grid_ind(p, N):
    p = rescale(p)
    #print(p)
    return (math.floor(p[0] * N), math.floor(p[1] * N))

# Does provide a very slight speedup in computing very large grids
class Grid:
    def __init__(self, ctx, N):
        self.N = N
        self.grid = []
        self.grid.append(empty_grid(N))
        self.ctx = ctx
        self.seg_num = len(ctx.segments)
        self.cur_num = len(ctx.curves)
        self.bez_num = self.seg_num + self.cur_num
        for i in range(self.bez_num):
            self.add_bezier_with_bbox(self.nth_bezier(i), i)
        
        for lvl in range(1, N): # terribly inefficient, but is a fraction of the runtime if N <= 32
            self.grid.append(empty_grid(N))
            for x in range(N):
                for y in range(N):
                    self.grid[lvl][(x, y)] = self.nth_level(lvl, (x, y))


    def nth_bezier(self, n):
        if n < self.seg_num:
            return self.ctx.segments[n]
        n = n - self.cur_num
        return self.ctx.curves[n]

    def add_segment(self, seg, c_ind):
        self.add_bezier_with_bbox(seg, c_ind)

    def add_curve(self, curve, c_ind):
        self.add_bezier_with_bbox(curve, c_ind)

    def add_bezier_with_bbox(self, c, c_ind): # can be improved
        bbox = box(c)
        (minp, maxp) = bbox
        (x0, y0) = grid_ind(minp, self.N)
        (x1, y1) = grid_ind(maxp, self.N)
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                self.grid[0][(x, y)].add(c_ind)
    
    def box_ind(self, p):
        ind = grid_ind(p, self.N)
        from_upper_left_corner = (p[0] - ind[0] / float(self.N), p[1] - ind[1] / float(self.N))
        r1 = min(from_upper_left_corner[0], 1.0 / float(self.N) - from_upper_left_corner[0])
        r2 = min(from_upper_left_corner[1], 1.0 / float(self.N) - from_upper_left_corner[1])
        return ind, min(r1, r2)
    
    def nth_level(self, n, box_ind): # could be improved
        ret = set()
        x0 = max(box_ind[0] - n, 0)
        y0 = max(box_ind[1] - n, 0)
        x1 = min(box_ind[0] + n, self.N - 1)
        y1 = min(box_ind[1] + n, self.N - 1)
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for c_ind in self.grid[0][(x, y)]:
                    ret.add(c_ind)
        return ret

    def nth_circle(self, n, box_ind, r0):
        return self.grid[n][box_ind], r0 + n * (1.0 / float(self.N)) if n < self.N-1 else float('inf')
