import streamlit as st
from PIL import Image
import numpy as np

st.title("色ヒット判定アプリ（2色両方必要）")

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

# 色①
st.subheader("色①（RGB）")
r1 = st.slider("R1", 0, 255, 255)
g1 = st.slider("G1", 0, 255, 0)
b1 = st.slider("B1", 0, 255, 0)

# 色②
st.subheader("色②（RGB）")
r2 = st.slider("R2", 0, 255, 0)
g2 = st.slider("G2", 0, 255, 0)
b2 = st.slider("B2", 0, 255, 255)

tolerance = st.slider("色の許容誤差", 0, 100, 10)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_column_width=True)

    img_array = np.array(image)

    if img_array.shape[-1] == 4:
        img_array = img_array[:, :, :3]

    target1 = np.array([r1, g1, b1])
    target2 = np.array([r2, g2, b2])

    # 高速処理
    diff1 = np.abs(img_array - target1)
    diff2 = np.abs(img_array - target2)

    mask1 = np.all(diff1 <= tolerance, axis=-1)
    mask2 = np.all(diff2 <= tolerance, axis=-1)

    # それぞれ存在するか確認
    hit1 = np.any(mask1)
    hit2 = np.any(mask2)

    # 両方存在したらヒット
    if hit1 and hit2:
        st.success("ヒット！")
    else:
        st.error("ノーヒット！")