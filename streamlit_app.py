import streamlit as st
from PIL import Image
import numpy as np
import itertools

st.title("色範囲ペア判定（グループ名表示）")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

# ===== 色範囲定義 =====
COLOR_RANGES = [
    {"name": "白", "min": [240,240,240], "max": [255,255,255]},
    {"name": "黒", "min": [0,0,0], "max": [30,30,30]},
    {"name": "赤", "min": [120,0,0], "max": [255,60,60]},
    {"name": "水色", "min": [140,180,220], "max": [200,230,255]},
    {"name": "緑", "min": [0,120,0], "max": [100,255,100]},
    {"name": "黄色", "min": [150,100,0], "max": [255,200,80]},
]
# =====================

def match_range(img, cmin, cmax):
    cmin = np.array(cmin)
    cmax = np.array(cmax)
    return np.all((img >= cmin) & (img <= cmax), axis=-1)

def match_gray(img):
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]

    cond1 = (np.abs(r - g) <= 20)
    cond2 = (np.abs(g - b) <= 20)
    cond3 = (np.abs(r - b) <= 20)
    cond4 = (r >= 30) & (r <= 240)
    cond5 = (g >= 30) & (g <= 240)
    cond6 = (b >= 30) & (b <= 240)

    return cond1 & cond2 & cond3 & cond4 & cond5 & cond6

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="アップロード画像", use_column_width=True)

    img_array = np.array(image)

    st.subheader("ヒットした色ペア")

    # 色ごとの存在判定
    color_hits = {}

    for c in COLOR_RANGES:
        mask = match_range(img_array, c["min"], c["max"])
        color_hits[c["name"]] = np.any(mask)

    # グレー
    color_hits["グレー"] = np.any(match_gray(img_array))

    # ペア判定（名前で表示）
    hit_count = 0
    for c1, c2 in itertools.combinations(color_hits.keys(), 2):
        if color_hits[c1] and color_hits[c2]:
            st.write(f"{c1}：{c2} ヒット")
            hit_count += 1

    if hit_count == 0:
        st.warning("ヒットなし")
    else:
        st.success(f"ヒット数: {hit_count}")