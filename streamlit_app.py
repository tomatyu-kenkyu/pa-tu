import streamlit as st
import requests
from PIL import Image

st.title("無料OCR（OCR.space × Streamlit 完全版）")

API_KEY = "K87828255188957"

uploaded_file = st.file_uploader("画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_column_width=True)

    # サイズチェック（1MB制限）
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
                    "language": "japanese",  # ← 重要（jpnはNG）
                    "isOverlayRequired": False
                }

                try:
                    response = requests.post(url, files=files, data=data)
                    result = response.json()

                    # デバッグ（必ず残すと便利）
                    st.write("APIレスポンス", result)

                    # エラーチェック
                    if result.get("IsErroredOnProcessing"):
                        st.error("OCRエラーが発生しました")
                        st.write(result.get("ErrorMessage"))

                    elif "ParsedResults" not in result:
                        st.error("解析結果が取得できませんでした")
                        st.write(result)

                    else:
                        parsed = result["ParsedResults"]

                        if not parsed or "ParsedText" not in parsed[0]:
                            st.error("テキストが見つかりません")
                            st.write(result)

                        else:
                            text = parsed[0]["ParsedText"]

                            st.success("抽出成功！")
                            st.text_area("OCR結果", text, height=300)

                except Exception as e:
                    st.error("通信または処理エラー")
                    st.write(str(e))