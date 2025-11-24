import numpy as np

def lerp(a, b, t):
    return a + (b - a) * t

def color_from_scale(t, colors):
    t = max(0.0, min(1.0, t))
    n = len(colors)
    if n == 1:
        return colors[0]

    pos = t * (n - 1)
    idx = int(np.floor(pos))
    frac = pos - idx

    if idx >= n - 1:
        return colors[-1]

    c0 = np.array(colors[idx], dtype=np.float32)
    c1 = np.array(colors[idx + 1], dtype=np.float32)
    c = lerp(c0, c1, frac)
    return tuple(c.astype(int))


def d_to_rgb(d, max_d=0.5):
    colors = [
        (255, 0, 0),    # red
        (255, 255, 0),  # yellow
        (0, 255, 0),    # green
        (0, 255, 255),  # cyan
        (0, 0, 255)     # blue
    ]
    t = min(d / max_d, 1.0)
    r, g, b = color_from_scale(t, colors)
    return f"rgb({r},{g},{b})"

def sd_to_rgb(d, max_d=0.4):
    colors = [
        (255, 0, 0),    # red
        (0, 255, 0),    # green
        (0, 0, 255)     # blue
    ]
    d = max(-max_d, min(max_d, d))
    t = 0.5 * (d / max_d + 1.0)
    r, g, b = color_from_scale(t, colors)
    return f"rgb({r},{g},{b})"

def sd_to_rgb_tuple(d, max_d=0.4):
    colors = [
        (255, 0, 0),    # red
        (255, 255, 0),  # yellow
        (0, 255, 0),    # green
        (0, 255, 255),  # cyan
        (0, 0, 255)     # blue
    ]
    d = max(-max_d, min(max_d, d))
    t = 0.5 * (d / max_d + 1.0)
    r, g, b = color_from_scale(t, colors)
    return (r, g, b)
