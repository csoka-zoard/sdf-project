import freetype
import numpy as np
from endpoints import Outvectors

class Ctx:
        def __init__(self):

            self.last_point = None
            self.curves=[]
            self.segments=[]
            self.outs = Outvectors()

        # def scale_point(self,a):
        #     if type(a)==freetype.ft_structs.FT_Vector:
        #         a_x = (float(a.x)-self.bbox_center[0])/self.bbox_scale
        #         a_y = (float(a.y)-self.bbox_center[1])/self.bbox_scale
        #         return (a_x,a_y)
        #     else:
        #         a_x = (float(a[0])-self.bbox_center[0])/self.bbox_scale
        #         a_y = (float(a[1])-self.bbox_center[1])/self.bbox_scale
        #         return (a_x,a_y)

def isRealCurve(p0,p1,p2):
    
    # p0 = np.array(p0,dtype=np.float64)
    # p1 = np.array(p1,dtype=np.float64)
    # p2 = np.array(p2,dtype=np.float64)

    # Vector from p0 to p2
    line_vec = p2 - p0
    
    # Vector from p0 to p1
    point_vec = p1 - p0
    
    # Area of the parallelogram formed by the vectors
    area = abs(line_vec[0] * point_vec[1] - line_vec[1] * point_vec[0])
    
    # # Length of the line segment from p0 to p2
    # line_length = np.linalg.norm(line_vec)
    
    # # Distance from p1 to the line formed by p0 and p2
    # distance = area / line_length
    
    return area > 0




def move_to(a, ctx):
    # a_x,a_y=ctx.scale_point(a)
    ctx.last_point = np.array([a.x,a.y],dtype=np.int32)

def line_to(a, ctx):
    # a_x,a_y = ctx.scale_point(a)
    if a.x==ctx.last_point[0] and a.y==ctx.last_point[1]:
        return
    # ctx.segments.append( np.array((ctx.scale_point( ctx.last_point ), (a_x,a_y))) )
    a = np.array([a.x,a.y],dtype=np.int32)
    curve = ( ctx.last_point, a)
    ctx.segments.append( curve )
    
    dir_vec = a - ctx.last_point
    ctx.outs.add_beg(ctx.last_point, dir_vec, curve)
    ctx.outs.add_end(a, dir_vec, curve)

    ctx.last_point = a

def conic_to(a, b, ctx):
    #a_x,a_y = ctx.scale_point(a)
    #b_x,b_y = ctx.scale_point(b)

    #ctx.curves.append( np.array((ctx.scale_point( ctx.last_point ), (a_x,a_y), (b_x,b_y))))
    a=np.array([a.x,a.y],dtype=np.int32)
    b=np.array([b.x,b.y],dtype=np.int32)

    # ctx.curves.append( (ctx.last_point,a,b))
    if isRealCurve(ctx.last_point,a,b):
      curve = (ctx.last_point,a,b)
      ctx.curves.append( curve )
      ctx.outs.add_beg(ctx.last_point, a - ctx.last_point, curve)
      ctx.outs.add_end(b, b - a, curve)
    else:
      curve = (ctx.last_point, b)
      ctx.segments.append( curve )
      dir_vec = b - ctx.last_point
      ctx.outs.add_beg(ctx.last_point, dir_vec, curve)
      ctx.outs.add_end(b, dir_vec, curve)
    ctx.last_point = b

def cubic_to(a, b, c, ctx):
    raise NotImplementedError("cubic_to not implemented")








