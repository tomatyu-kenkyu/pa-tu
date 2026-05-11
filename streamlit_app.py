from fastapi import FastAPI
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
import uuid
import os

app = FastAPI()

# 保存フォルダ
os.makedirs("shots", exist_ok=True)

class URLRequest(BaseModel):
    url: str


def take_screenshot(url: str, path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="networkidle")

        # ポップアップ除去
        page.evaluate("""
        () => {
            document.querySelectorAll('[class*="cookie"],[class*="popup"],[class*="modal"],iframe,.overlay')
            .forEach(el => el.remove());
            document.body.style.overflow = "auto";
        }
        """)

        page.wait_for_timeout(1000)
        page.screenshot(path=path, full_page=True)

        browser.close()


@app.post("/screenshot")
def screenshot(req: URLRequest):
    file_id = str(uuid.uuid4())
    file_path = f"shots/{file_id}.png"

    take_screenshot(req.url, file_path)

    return {
        "status": "ok",
        "file": file_path
    }