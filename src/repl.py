from freetypetest import *
from img import sdf_to_img, img_add_vecs, img_add_curvatures
from persistence import *
import math
from upscale import upscale_sdf, sdf_diff
import time
from curvature import curvature, sdf_gradient

# sdf_map,
# grid_sdf_map,
# img, persistence


face = load_face()
ctx = buildCtx(face)


def task():
    sdf = grid_sdf_map(ctx, 2048, 32, extent = 1.0)
    img = sdf_to_img(sdf, image_size)
    save_img(img)
    save_sdf(sdf, "sdf_big.txt")

def print_sdf(sdf):
    n = int(math.isqrt(len(sdf)))
    for i in range(n):
        for j in range(n):
            print("%.2f" % sdf[(i, j)], end="\t")
        print()

def sdf_apply(sdf, fn):
    sdf_ret = {}
    n = int(math.isqrt(len(sdf)))
    for i in range(n):
        for j in range(n):
            sdf_ret[(i, j)] = fn(sdf[(i, j)])
    return sdf_ret

def measure_grid_time(n, N):
    start = time.time()
    sdf = grid_sdf_map(ctx, n, N, extent)
    end = time.time()
    print(end - start)

def measure_time(n):
    start = time.time()
    sdf = sdf_map(ctx, n, extent)
    end = time.time()
    print(end - start)

def show_upscale_diff(n = 32):
    m = 2048
    extent = 1.0
    image_size = 2048
    sdf_small = sdf_map(ctx, n, extent)
    #img_small = sdf_to_img(sdf_small, image_size)
    sdf_upscaled = upscale_sdf(sdf_small, n, m)
    #img_upscaled = sdf_to_img(sdf_upscaled, image_size)
    sdf_big = load_sdf("sdf_big.txt")
    #img_big = sdf_to_img(sdf_big, image_size)
    sdf_d = sdf_diff(sdf_big, sdf_upscaled)
    #img_d = sdf_to_img(sdf_d, image_size)
    sdf_d2 = sdf_apply(sdf_d, lambda x: x*20.0)
    img = sdf_to_img(sdf_d2, image_size)
    curvat = curvature(ctx)
    img_add_curvatures(img, curvat)
    grad_upscaled = sdf_gradient(sdf_upscaled, m)
    grad_big = sdf_gradient(sdf_big, m)
    img = sdf_to_img(sdf_apply(grad_big, lambda vec: 0.3 * math.sqrt(vec[0]**2+vec[1]**2)), image_size)
    save_img(img)


# TODO:
#  * sdf to contain the curve from which distance was measured
#  * way to display a b-curve on the image
#  * highlight tool that highlights point at (x, y) and its curve
