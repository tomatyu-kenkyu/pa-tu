import urllib.parse
import requests
from PIL import Image
from io import BytesIO

# ------------------------
# ScreenshotMachine API
# ------------------------
SCREENSHOT_KEY = "82ef7e"

def generate_screenshot_api_url(key, options):
    url = "https://api.screenshotmachine.com/?key=" + key
    url += "&" + urllib.parse.urlencode(options)
    return url

# ------------------------
# 取得したいURL
# ------------------------
target_url = "https://example.com"

# ------------------------
# スクリーンショット取得
# ------------------------
options = {
    "url": target_url,
    "dimension": "1920x1080",
    "device": "desktop",
    "cacheLimit": "0",
    "delay": "500"
}

api_url = generate_screenshot_api_url(SCREENSHOT_KEY, options)

response = requests.get(api_url)

if response.status_code == 200:
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img.show()  # 画像表示（ローカル実行時）
else:
    print("スクリーンショット取得失敗:", response.status_code)