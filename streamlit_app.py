import streamlit as st
import urllib.parse
from PIL import Image
from collections import Counter
from io import BytesIO
import requests

# 🔐 APIキー（本番はst.secrets推奨）
OCR_API_KEY = "K87828255188957"
SCREENSHOT_KEY = "82ef7e"

def generate_screenshot_api_url(key, options):
    url = 'https://api.screenshotmachine.com/?key=' + key
    url += '&' + urllib.parse.urlencode(options)
    return url

st.title("スクリーンショット → RGB解析 + OCR（最終版）")

target_url = st.text_input("URL", value="https://example.com")

if st.button("実行"):
    # ------------------------
    # 📸 スクリーンショット取得
    # ------------------------
    options = {
        'url': target_url,
        'dimension': '1366x768',
        'device': 'desktop',
        'cacheLimit': '0',
        'delay': '200'
    }

    api_url = generate_screenshot_api_url(SCREENSHOT_KEY, options)

    res = requests.get(api_url)

    if res.status_code != 200:
        st.error(f"スクショ取得失敗: {res.status_code}")
        st.text(res.text)
        st.stop()

    image_data = res.content

    try:
        img = Image.open(BytesIO(image_data)).convert("RGB")
    except:
        st.error("画像として読み込めませんでした")
        st.stop()

    st.image(img, caption="スクリーンショット", use_column_width=True)

    # ------------------------
    # 🎨 RGB解析
    # ------------------------
    pixels = list(img.getdata())
    total_pixels = len(pixels)
    color_count = Counter(pixels)

    st.subheader("色の割合（上位20色）")
    for color, count in color_count.most_common(20):
        ratio = count / total_pixels * 100
        st.write(f"{color}: {ratio:.2f}%")

    # ------------------------
    # 🧠 OCR（最重要）
    # ------------------------
    st.subheader("OCR結果")

    # 🔥 前処理（成功率の核）
    img_ocr = img.convert("L")
    img_ocr = img_ocr.resize((img.width * 2, img.height * 2))

    buffer = BytesIO()
    img_ocr.save(buffer, format="PNG")
    image_data_ocr = buffer.getvalue()

    files = {
        'file': ('image.png', image_data_ocr, 'image/png')
    }

    payload = {
        'apikey': OCR_API_KEY,
        'language': 'eng',  # ← 安定優先
        'detectOrientation': True,
        'scale': True
    }

    try:
        r = requests.post("https://api.ocr.space/parse/image", files=files, data=payload)
        result = r.json()

        # デバッグ（残してOK）
        st.write("Status:", r.status_code)

        if result.get("ParsedResults") and result["ParsedResults"][0]["ParsedText"]:
            text = result["ParsedResults"][0]["ParsedText"]
            st.text_area("抽出結果", text, height=300)
        else:
            st.error("OCR失敗（文字が小さい or API制限）")

    except Exception as e:
        st.error(f"OCRエラー: {e}")