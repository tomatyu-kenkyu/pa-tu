import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from collections import Counter

# =========================
# ScreenshotMachine 設定
# =========================
API_KEY = "YOUR_API_KEY"

# =========================
# スクショ取得関数
# =========================
def get_screenshot(url):

    params = {
        "key": "82ef7e",
        "url": url,

        # Cookie対策
        "device": "desktop",
        "dimension": "1920x1080",
        "cacheLimit": "0",
        "delay": "100",

        # スクショ設定
        "format": "png",
        "cacheLimit": "0"
    }

    api_url = "https://api.screenshotmachine.com"

    response = requests.get(api_url, params=params)

    return response.content

# =========================
# 色抽出
# =========================
def extract_colors(image):

    img = image.convert("RGB")

    pixels = list(img.getdata())

    total = len(pixels)

    counter = Counter(pixels)

    result = []

    for color, count in counter.most_common(20):

        ratio = round(count / total * 100, 2)

        result.append({
            "RGB": color,
            "count": count,
            "ratio": ratio
        })

    return result

# =========================
# Streamlit UI
# =========================
st.title("Web Screenshot + Color Analyzer")

url = st.text_input("URLを入力")

if st.button("解析開始"):

    if url:

        with st.spinner("スクリーンショット取得中..."):

            img_data = get_screenshot(url)

            image = Image.open(BytesIO(img_data))

            st.image(image, caption="取得したスクリーンショット")

        st.subheader("主要色")

        colors = extract_colors(image)

        for c in colors:

            st.write(
                f"RGB: {c['RGB']} | "
                f"Pixels: {c['count']} | "
                f"Ratio: {c['ratio']}%"
            )

    else:
        st.warning("URLを入力してください")