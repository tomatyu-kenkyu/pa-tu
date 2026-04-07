import streamlit as st
from PIL import Image
import numpy as np
import itertools

st.title("複数色ペア ヒット判定（ヒットのみ表示）")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

# ====== 色データ ======
raw_colors = [
    (252,254,251),(35,36,34),(33,35,32),(30,31,28),(248,252,249),
    (249,254,255),(255,252,255),(241,243,239),(244,247,243),(37,40,37),

    (140,0,0),(252,254,251),(241,242,239),(249,251,248),(157,198,238),
    (244,247,243),(139,0,1),(149,0,1),(132,1,0),(141,0,0),

    (252,255,251),(244,239,239),(164,201,235),(250,255,255),(162,199,233),
    (255,253,255),(159,200,239),(249,251,248),(255,252,250),(162,203,242),

    (253,255,252),(236,239,235),(242,244,241),(234,236,233),(210,212,209),
    (0,62,119),(0,58,110),(0,0,0),(0,51,98),(2,74,150),

    (252,254,251),(43,55,84),(234,236,233),(214,217,214),(20,154,24),
    (249,251,248),(83,85,82),(248,253,255),(245,247,243),(225,228,224),

    (252,254,251),(239,242,245),(250,254,255),(249,251,248),(0,156,208),
    (255,252,255),(240,242,239),(244,247,243),(234,239,241),(224,43,18),

    (253,255,252),(241,243,240),(0,104,184),(113,142,155),(0,0,0),
    (135,144,157),(131,140,153),(206,157,6),(203,205,202),(129,146,157)
]

# 重複削除
unique_colors = list(set(raw_colors))
COLORS = [np.array(c) for c in unique_colors]

TOLERANCE = 10
# =====================

st.write(f"ユニーク色数: {len(COLORS)}")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_column_width=True)

    img_array = np.array(image)

    if img_array.shape[-1] == 4:
        img_array = img_array[:, :, :3]

    st.subheader("ヒットしたペアのみ")

    hit_count = 0

    for color1, color2 in itertools.combinations(COLORS, 2):

        diff1 = np.abs(img_array - color1)
        diff2 = np.abs(img_array - color2)

        mask1 = np.all(diff1 <= TOLERANCE, axis=-1)
        mask2 = np.all(diff2 <= TOLERANCE, axis=-1)

        if np.any(mask1) and np.any(mask2):
            st.write(f"{color1.tolist()}：{color2.tolist()} ヒット")
            hit_count += 1

    if hit_count == 0:
        st.warning("ヒットなし")
    else:
        st.success(f"ヒット数: {hit_count}")