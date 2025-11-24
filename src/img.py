# TODO: separate image stuff to here

from PIL import Image, ImageDraw
from color import d_to_rgb, sd_to_rgb_tuple
import math
import numpy as np

def img_add_vecs(img, ctx, extent = 1.0):
    lam = 0.1  # length scale of vector arrow (in SDF units)
    r_px = 2    # circle radius in pixels
    draw = ImageDraw.Draw(img)
    image_size, _ = img.size
    for (x, y), v in ctx.outs.vecs.items():
        v = np.array(v, dtype=np.float64)
        if np.linalg.norm(v) == 0:
            continue
        # Compute start (p) and end (p + lam * v) in SDF coordinates
        p = np.array([x, y])
        q = p + lam * v
        # Convert SDF coordinates -> pixel coordinates
        def world_to_px(coord):
            xw, yw = coord
            px = int(round((extent - xw) * image_size / (2 * extent)))
            py = int(round((extent - yw) * image_size / (2 * extent)))
            return (px, py)
        p_px = world_to_px(p)
        q_px = world_to_px(q)
        # Draw a small red circle at p
        draw.ellipse(
            [p_px[0] - r_px, p_px[1] - r_px, p_px[0] + r_px, p_px[1] + r_px],
            fill=(0, 0, 0)
        )
        # Draw a short red line in direction v
        draw.line([p_px, q_px], fill=(0, 0, 0), width=1)

def img_add_curvatures(img, curvatures, extent = 1.0):
    r_px = 2    # circle radius in pixels
    draw = ImageDraw.Draw(img)
    image_size, _ = img.size
    for (x, y), v in curvatures:
        p = np.array([x, y])
        def world_to_px(coord):
            xw, yw = coord
            px = int(round((extent - xw) * image_size / (2 * extent)))
            py = int(round((extent - yw) * image_size / (2 * extent)))
            return (px, py)
        p_px = world_to_px(p)
        draw.ellipse(
            [p_px[0] - r_px, p_px[1] - r_px, p_px[0] + r_px, p_px[1] + r_px],
            fill=(int(v * 16.0), 0, 0)
        )

def sdf_to_img(sdf, image_size):
    n = int(math.isqrt(len(sdf)))
    cell_px = image_size / n
    img = Image.new("RGB", (image_size, image_size), (0,0,0))
    draw = ImageDraw.Draw(img)
    for i in range(n):
        top = int(round(i * cell_px))
        bottom = int(round((i + 1) * cell_px))
        for j in range(n):
            left = int(round(j * cell_px))
            right = int(round((j + 1) * cell_px))
            dist = sdf[(i, j)]
            color = sd_to_rgb_tuple(dist)
            draw.rectangle([left, top, right, bottom], fill=color)
    return img
