import os
os.environ["FLAGS_allocator_strategy"] = "auto_growth"

import streamlit as st
import urllib.parse
import requests
import numpy as np

from io import BytesIO
from collections import Counter

from PIL import (
    Image,
    ImageEnhance,
    ImageFilter
)

from paddleocr import PaddleOCR

# ------------------------
# PaddleOCR 初期化
# ------------------------
@st.cache_resource
def load_ocr():
    return PaddleOCR(
        use_angle_cls=True,
        lang='japan'
    )

ocr = load_ocr()

# ------------------------
# ScreenshotMachine API
# ------------------------
SCREENSHOT_KEY = "82ef7e"

def generate_screenshot_api_url(key, options):
    url = "https://api.screenshotmachine.com/?key=" + key
    url += "&" + urllib.parse.urlencode(options)
    return url

# ------------------------
# 危険ワード
# ------------------------
danger_words = [
    "ウイルス",
    "感染",
    "危険",
    "警告",
    "今すぐ",
    "修復",
    "サポート",
    "電話",
    "0120",
    "マルウェア",
    "トロイ",
    "セキュリティ",
    "ブロック",
    "支払い",
    "クレジット",
    "緊急",
    "当選",
    "クリック",
    "インストール"
]

# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(
    page_title="高精度OCR + 危険サイト解析",
    layout="wide"
)

st.title("高精度 OCR + 危険サイト解析")

target_url = st.text_input(
    "解析URL",
    value="https://example.com"
)

if st.button("解析開始"):

    # ------------------------
    # スクリーンショット取得
    # ------------------------
    with st.spinner("スクリーンショット取得中..."):

        options = {
            "url": target_url,
            "dimension": "1920x1080",
            "device": "desktop",
            "cacheLimit": "0",
            "delay": "500"
        }

        api_url = generate_screenshot_api_url(
            SCREENSHOT_KEY,
            options
        )

        try:
            response = requests.get(api_url)

            if response.status_code != 200:
                st.error(f"スクショ取得失敗: {response.status_code}")
                st.stop()

            image_data = response.content

            img = Image.open(
                BytesIO(image_data)
            ).convert("RGB")

        except Exception as e:
            st.error(f"画像取得エラー: {e}")
            st.stop()

    # ------------------------
    # 表示
    # ------------------------
    st.image(
        img,
        caption="取得画像",
        use_container_width=True
    )

    # ------------------------
    # RGB解析
    # ------------------------
    st.subheader("RGB解析（上位20色）")

    pixels = list(img.getdata())

    total_pixels = len(pixels)

    color_count = Counter(pixels)

    for color, count in color_count.most_common(20):

        ratio = count / total_pixels * 100

        st.write(
            f"{color} : {ratio:.2f}%"
        )

    # ------------------------
    # OCR前処理
    # ------------------------
    st.subheader("OCR前処理")

    img_ocr = img.convert("L")

    # シャープ化
    img_ocr = img_ocr.filter(
        ImageFilter.SHARPEN
    )

    # コントラスト強化
    enhancer = ImageEnhance.Contrast(
        img_ocr
    )

    img_ocr = enhancer.enhance(2.5)

    # 拡大
    img_ocr = img_ocr.resize(
        (
            img_ocr.width * 2,
            img_ocr.height * 2
        )
    )

    st.image(
        img_ocr,
        caption="OCR用前処理画像",
        use_container_width=True
    )

    # ------------------------
    # OCR
    # ------------------------
    st.subheader("OCR結果")

    try:

        img_np = np.array(img_ocr)

        result = ocr.ocr(
            img_np,
            cls=True
        )

        extracted_text = ""

        for line in result:

            if line is None:
                continue

            for word in line:

                if word is None:
                    continue

                text = word[1][0]

                extracted_text += text + "\n"

        if extracted_text.strip():

            st.text_area(
                "抽出テキスト",
                extracted_text,
                height=400
            )

        else:
            st.warning(
                "文字が検出できませんでした"
            )

    except Exception as e:
        st.error(f"OCRエラー: {e}")
        st.stop()

    # ------------------------
    # 危険ワード解析
    # ------------------------
    st.subheader("危険ワード解析")

    found_words = []

    for word in danger_words:

        if word in extracted_text:
            found_words.append(word)

    if found_words:

        st.error("危険ワード検出")

        for word in found_words:
            st.write(f"⚠ {word}")

    else:
        st.success("危険ワードなし")

    # ------------------------
    # 危険度スコア
    # ------------------------
    st.subheader("危険度スコア")

    score = min(len(found_words) * 10, 100)

    st.progress(score / 100)

    st.write(f"危険度: {score}/100")