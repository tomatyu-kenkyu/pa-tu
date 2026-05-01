import streamlit as st
import urllib.request
import urllib.parse
import hashlib
from PIL import Image
from collections import Counter
from io import BytesIO
import requests  # ← OCR用

# OCR APIキー
OCR_API_KEY = "K87828255188957"

def generate_screenshot_api_url(customer_key, secret_phrase, options):
    api_url = 'https://api.screenshotmachine.com/?key=' + customer_key
    if secret_phrase:
        api_url += '&hash=' + hashlib.md5(
            (options.get('url') + secret_phrase).encode('utf-8')
        ).hexdigest()
    api_url += '&' + urllib.parse.urlencode(options)
    return api_url

st.title("スクリーンショット → RGB解析 + OCR")

# 入力
customer_key = "82ef7e"
secret_phrase = st.text_input("Secret Phrase（任意）", value="")
target_url = st.text_input("スクリーンショットURL", value="https://www.google.com")

if st.button("実行"):
    options = {
        'url': target_url,
        'dimension': '1366x768',
        'device': 'desktop',
        'cacheLimit': '0',
        'delay': '200',
        'zoom': '100'
    }

    # スクショURL生成
    api_url = generate_screenshot_api_url(customer_key, secret_phrase, options)

    # 画像取得
    with urllib.request.urlopen(api_url) as response:
        image_data = response.read()

    img = Image.open(BytesIO(image_data)).convert("RGB")

    # 表示
    st.image(img, caption="取得したスクリーンショット", use_column_width=True)

    # ------------------------
    # 🎨 RGB解析
    # ------------------------
    pixels = list(img.getdata())
    total_pixels = len(pixels)
    color_count = Counter(pixels)

    st.subheader("色の割合（上位20色）")

    for color, count in color_count.most_common(20):
        ratio = count / total_pixels * 100
        st.write(f"{color}: {count} ピクセル ({ratio:.2f}%)")

    # ------------------------
    # 🧠 OCR（ここ追加）
    # ------------------------
    st.subheader("OCR結果（文字抽出）")

    # 画像をバイトとして送る
    ocr_url = "https://api.ocr.space/parse/image"

    files = {
        'file': ('screenshot.png', image_data)
    }

    payload = {
        'apikey': OCR_API_KEY,
        'language': 'jpn',
        'detectOrientation': True,
        'scale': True
    }

    try:
        r = requests.post(ocr_url, files=files, data=payload)
        result = r.json()

        if result.get("ParsedResults"):
            text = result["ParsedResults"][0]["ParsedText"]
            st.text_area("抽出されたテキスト", text, height=300)
        else:
            st.error("OCRに失敗しました")

    except Exception as e:
        st.error(f"OCRエラー: {e}")