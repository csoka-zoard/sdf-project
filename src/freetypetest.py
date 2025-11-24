#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2018 Dean Serenevy <dean@serenevy.net>
# SPDX-License-Identifier: BSD-3-Clause-Clear
'''
Show how to use outline decompose.
'''
import numpy as np
from Ctx import Ctx, move_to, conic_to, cubic_to, line_to
from DF import SDF
from color import d_to_rgb, sd_to_rgb_tuple
from persistence import *
from gridDF import gridSDF
from grid import Grid



def sdf_map(ctx, n, extent = 1.0):
    step = 2.0 / n
    sdf = dict() # (x, y) -> (distance,)
    for i in range(n):
        y = +extent - (i + 0.5) * step
        for j in range(n):
            x = +extent - (j + 0.5) * step
            p = np.array([x, y], dtype=np.float64)
            dist = SDF(p, ctx)
            sdf[(i, j)] = float(dist)
        # print("i =", i)
    return sdf

def grid_sdf_map(ctx, n, N, extent = 1.0):
    step = 2.0 / n
    grid = Grid(ctx, N)
    # print("grid built")
    sdf = dict()
    for i in range(n):
        y = +extent - (i + 0.5) * step
        for j in range(n):
            x = +extent - (j + 0.5) * step
            p = np.array([x, y], dtype=np.float64)
            dist = gridSDF(p, ctx, grid)
            sdf[(i, j)] = float(dist)
        # print("i =", i)
    return sdf

def buildCtx(face):
    ctx = Ctx()
    face.glyph.outline.decompose(ctx, move_to=move_to, line_to=line_to, conic_to=conic_to, cubic_to=cubic_to)
    tmp = np.vstack((np.array(ctx.segments).reshape(-1,2),np.array(ctx.curves).reshape(-1,2)))
    bbox = np.array([tmp.min(axis=0),tmp.max(axis=0)])
    bbox_center = (bbox[0]+bbox[1])/2
    bbox_scale = max(bbox[1]-bbox[0])*0.5*1.2
    if len(ctx.segments)>0:
        segments = np.array(ctx.segments,np.float32)
        segments = (segments-bbox_center)/bbox_scale
        ctx.segments = segments
    if len(ctx.curves)>0:
        curves = np.array(ctx.curves,np.float32)
        ctx.curves = (curves-bbox_center)/bbox_scale
    ctx.outs.rescale(bbox_center, bbox_scale)
    return ctx

if __name__ == '__main__':
    face = load_face()
    ctx = buildCtx(face)

    n = 32
    extent = 1.0
    image_size = 2000
    (img, sdf) = sdf_map(ctx, n, image_size, extent)

    save_img(img)
    print(f"Wrote image (size {image_size}x{image_size}, grid {n}x{n})")
