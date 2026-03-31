import streamlit as st
from PIL import Image
import numpy as np
import itertools

st.title("複数色ペア 自動ヒット判定")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

# ====== ここで色リストを定義 ======
COLORS = [
    np.array([255, 0, 0]),   # 赤
    np.array([0, 255, 0]),   # 緑
    np.array([0, 0, 255]),   # 青
    np.array([255, 255, 0])  # 黄色
]

TOLERANCE = 10
# =================================

st.write("対象色一覧:")
for c in COLORS:
    st.write(c)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_column_width=True)

    img_array = np.array(image)

    # RGBA対策
    if img_array.shape[-1] == 4:
        img_array = img_array[:, :, :3]

    results = []

    # すべてのペア組み合わせを生成
    for color1, color2 in itertools.combinations(COLORS, 2):

        diff1 = np.abs(img_array - color1)
        diff2 = np.abs(img_array - color2)

        mask1 = np.all(diff1 <= TOLERANCE, axis=-1)
        mask2 = np.all(diff2 <= TOLERANCE, axis=-1)

        hit1 = np.any(mask1)
        hit2 = np.any(mask2)

        if hit1 and hit2:
            result = "ヒット"
        else:
            result = "ノーヒット"

        results.append(f"{color1.tolist()}：{color2.tolist()} {result}")

    # 結果表示
    st.subheader("判定結果")
    for r in results:
        st.write(r)