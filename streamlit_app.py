import streamlit as st
import requests
from PIL import Image

st.title("無料OCR（OCR.space × Streamlit 最終版）")

API_KEY = "K87828255188957"

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_column_width=True)

    # サイズチェック（1MB制限対策）
    if uploaded_file.size > 1 * 1024 * 1024:
        st.error("画像サイズが大きすぎます（1MB以下にしてください）")
    else:
        if st.button("OCR実行"):
            with st.spinner("解析中..."):
                url = "https://api.ocr.space/parse/image"

                files = {
                    "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }

                data = {
                    "apikey": API_KEY,
                    "language": "japanese",  # ← ここ重要
                    "isOverlayRequired": False
                }

                response = requests.post(url, files=files, data=data)
                result = response.json()

                # デバッグ表示（問題時に確認）
                if result.get("IsErroredOnProcessing"):
                    st.error("OCRエラー")
                    st.write(result)
                else:
                    text = result["ParsedResults"][0]["ParsedText"]

                    st.success("抽出成功！")
                    st.text_area("OCR結果", text, height=300)