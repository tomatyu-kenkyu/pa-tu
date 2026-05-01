import streamlit as st
import urllib.parse
import hashlib
from PIL import Image
from collections import Counter
from io import BytesIO
import requests

OCR_API_KEY = "K87828255188957"

def generate_screenshot_api_url(customer_key, options):
    api_url = 'https://api.screenshotmachine.com/?key=' + customer_key
    api_url += '&' + urllib.parse.urlencode(options)
    return api_url

st.title("スクリーンショット → RGB解析 + OCR（安定版）")

customer_key = "82ef7e"

# Googleは失敗しやすいので変更
target_url = st.text_input("URL", value="https://example.com")

if st.button("実行"):
    options = {
        'url': target_url,
        'dimension': '1366x768',
        'device': 'desktop',
        'cacheLimit': '0',
        'delay': '200'
    }

    api_url = generate_screenshot_api_url(customer_key, options)

    # ------------------------
    # 🔥 安定版（requests使用）
    # ------------------------
    response = requests.get(api_url)

    if response.status_code != 200:
        st.error(f"スクショ取得失敗: {response.status_code}")
        st.text(response.text)
        st.stop()

    image_data = response.content

    img = Image.open(BytesIO(image_data)).convert("RGB")

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
        st.write(f"{color}: {count} ({ratio:.2f}%)")

    # ------------------------
    # 🧠 OCR
    # ------------------------
    st.subheader("OCR結果")

    ocr_url = "https://api.ocr.space/parse/image"

    files = {
        'file': ('image.png', image_data)
    }

    payload = {
        'apikey': OCR_API_KEY,
        'language': 'jpn+eng',
        'detectOrientation': True,
        'scale': True
    }

    r = requests.post(ocr_url, files=files, data=payload)
    result = r.json()

    if result.get("ParsedResults"):
        text = result["ParsedResults"][0]["ParsedText"]
        st.text_area("抽出結果", text, height=300)
    else:
        st.error("OCR失敗")