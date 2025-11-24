from pathlib import Path
import json
import math
import freetype


BASE_DIR = Path(__file__).parent.parent
type_path = BASE_DIR / "data/input/wmanimals2.ttf"


def load_face():
    face = freetype.Face(str(type_path))
    face.load_char('A', freetype.FT_LOAD_DEFAULT | freetype.FT_LOAD_NO_BITMAP | freetype.FT_LOAD_NO_SCALE)
    return face

def save_img(img):
    out_path = BASE_DIR / "data/output/output.png"
    img.save(out_path)

def save_sdf(sdf, filename):
    out_path = BASE_DIR / ("data/output/" + filename)
    with open(str(out_path), "w") as file:
        file.write(sdf_to_json(sdf))

def load_sdf(filename):
    out_path = BASE_DIR / ("data/output/" + filename)
    filecontent = 0
    with open(str(out_path)) as file:
        filecontent = file.read()
    return sdf_from_json(filecontent)

def sdf_to_json(sdf):
    N = math.isqrt(len(sdf))
    arr = []
    for x in range(N):
        for y in range(N):
            arr.append(sdf[(x, y)])
    return json.dumps(arr)

def sdf_from_json(json_arr):
    arr = json.loads(json_arr)
    N = math.isqrt(len(arr))
    sdf = dict()
    i = 0
    for x in range(N):
        for y in range(N):
            sdf[(x, y)] = arr[i]
            i = i + 1
    return sdf