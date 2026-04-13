import streamlit as st
from PIL import Image
import numpy as np

st.title("色範囲ペア判定（6ペア限定）")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

# ===== 色範囲定義（変更なし）=====
COLOR_RANGES = {
    "白": ([240,240,240], [255,255,255]),
    "黒": ([0,0,0], [30,30,30]),
    "赤": ([120,0,0], [255,60,60]),
    "水色": ([140,180,220], [200,230,255]),
    "緑": ([0,120,0], [100,255,100]),
    "黄色": ([150,100,0], [255,200,80]),
}
# ===============================

# ===== 指定ペア（ここだけ変更）=====
TARGET_PAIRS = [
    ("白","赤"),
    ("白","水色"),
    ("白","グレー"),
    ("赤","水色"),
    ("赤","グレー"),
    ("水色","グレー")
]
# =================================

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

    st.subheader("検出された色ペア")

    # 色存在判定
    color_hits = {}

    for name, (cmin, cmax) in COLOR_RANGES.items():
        color_hits[name] = np.any(match_range(img_array, cmin, cmax))

    color_hits["グレー"] = np.any(match_gray(img_array))

    # 判定（6ペアのみ）
    hit_count = 0
    for c1, c2 in TARGET_PAIRS:
        if color_hits.get(c1, False) and color_hits.get(c2, False):
            st.write(f"{c1}：{c2}")
            hit_count += 1

    if hit_count == 0:
        st.warning("該当なし")
    else:
        st.success(f"検出ペア数: {hit_count}")