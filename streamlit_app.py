# ------------------------
# 🧠 OCR（最終安定版）
# ------------------------
st.subheader("OCR結果")

# 🔥 前処理（これが一番重要）
img_ocr = img.convert("L")  # 白黒
img_ocr = img_ocr.resize((img.width * 2, img.height * 2))  # 拡大

buffer = BytesIO()
img_ocr.save(buffer, format="PNG")
image_data_ocr = buffer.getvalue()

ocr_url = "https://api.ocr.space/parse/image"

files = {
    'file': ('image.png', image_data_ocr, 'image/png')
}

payload = {
    'apikey': OCR_API_KEY,
    'language': 'eng',  # ←まずこれで安定させる
    'detectOrientation': True,
    'scale': True
}

r = requests.post(ocr_url, files=files, data=payload)

# 🔍 デバッグ（残してOK）
st.write("Status:", r.status_code)
st.json(r.json())

result = r.json()

if result.get("ParsedResults") and result["ParsedResults"][0]["ParsedText"]:
    text = result["ParsedResults"][0]["ParsedText"]
    st.text_area("抽出結果", text, height=300)
else:
    st.error("OCR失敗（画像 or API制限）")