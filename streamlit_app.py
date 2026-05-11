import streamlit as st
import urllib.parse
import requests
from PIL import Image
from io import BytesIO

# ------------------------
# Screenshot API Key
# ------------------------
SCREENSHOT_KEY = "82ef7e"

# ------------------------
# URL生成
# ------------------------
def generate_screenshot_api_url(key, options):
    url = "https://api.screenshotmachine.com/?key=" + key
    url += "&" + urllib.parse.urlencode(options)
    return url

# ------------------------
# UI
# ------------------------
st.set_page_config(page_title="スクリーンショット取得", layout="wide")

st.title("URLスクリーンショット取得ツール")

target_url = st.text_input("URLを入力", "https://example.com")

if st.button("スクリーンショット取得"):

    if not target_url.startswith("http"):
        st.error("http または https から始まるURLを入力してください")
        st.stop()

    with st.spinner("スクリーンショット取得中..."):

        options = {
            "url": target_url,
            "dimension": "1920x1080",
            "device": "desktop",
            "cacheLimit": "0",
            "delay": "500"
        }

        api_url = generate_screenshot_api_url(SCREENSHOT_KEY, options)

        try:
            response = requests.get(api_url, timeout=30)

            if response.status_code != 200:
                st.error(f"取得失敗: {response.status_code}")
                st.stop()

            img = Image.open(BytesIO(response.content)).convert("RGB")

        except Exception as e:
            st.error(f"エラー: {e}")
            st.stop()

    st.success("取得完了")

    st.image(img, caption="スクリーンショット", use_container_width=True)