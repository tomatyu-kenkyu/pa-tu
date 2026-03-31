import streamlit as st
from PIL import Image
import numpy as np

st.title("色ヒット判定アプリ（コード指定）")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

# ====== ここを変更するだけ ======
COLOR_1 = np.array([255, 0, 0])   # 色①（赤）
COLOR_2 = np.array([0, 0, 255])   # 色②（青）
TOLERANCE = 10                    # 許容誤差
# ==============================

st.write(f"色①: {COLOR_1}")
st.write(f"色②: {COLOR_2}")
st.write(f"許容誤差: {TOLERANCE}")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_column_width=True)

    img_array = np.array(image)

    # RGBA対策
    if img_array.shape[-1] == 4:
        img_array = img_array[:, :, :3]

    # 差分計算
    diff1 = np.abs(img_array - COLOR_1)
    diff2 = np.abs(img_array - COLOR_2)

    mask1 = np.all(diff1 <= TOLERANCE, axis=-1)
    mask2 = np.all(diff2 <= TOLERANCE, axis=-1)

    hit1 = np.any(mask1)
    hit2 = np.any(mask2)

    if hit1 and hit2:
        st.success("ヒット！")
    else:
        st.error("ノーヒット！")