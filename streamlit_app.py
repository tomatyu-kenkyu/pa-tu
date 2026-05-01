import streamlit as st
import requests

st.title("OCR.space × Streamlit（無料OCR）")

API_KEY = "K87828255188957"

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="アップロード画像", use_column_width=True)

    if st.button("OCR実行"):
        with st.spinner("解析中..."):
            url = "https://api.ocr.space/parse/image"

            files = {
                "file": uploaded_file.getvalue()
            }

            data = {
                "apikey": API_KEY,
                "language": "jpn",
                "isOverlayRequired": False
            }

            response = requests.post(url, files=files, data=data)
            result = response.json()

            try:
                text = result["ParsedResults"][0]["ParsedText"]
                st.success("抽出成功！")
                st.text_area("OCR結果", text, height=300)
            except:
                st.error("読み取り失敗（画像サイズ or 形式の可能性）")