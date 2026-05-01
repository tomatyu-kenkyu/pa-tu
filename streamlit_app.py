import streamlit as st
import requests

st.title("OCR.space × Streamlit（安定版）")

API_KEY = "K87828255188957"

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file)

    if uploaded_file.size > 1 * 1024 * 1024:
        st.error("画像サイズが大きすぎます（1MB以下）")
    else:
        if st.button("OCR実行"):
            with st.spinner("解析中..."):
                url = "https://api.ocr.space/parse/image"

                files = {
                    "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }

                data = {
                    "apikey": API_KEY,
                    "language": "jpn+eng"
                }

                response = requests.post(url, files=files, data=data)
                result = response.json()

                st.write(result)  # デバッグ表示

                try:
                    text = result["ParsedResults"][0]["ParsedText"]
                    st.success("成功")
                    st.text_area("結果", text)
                except:
                    st.error("OCR失敗")