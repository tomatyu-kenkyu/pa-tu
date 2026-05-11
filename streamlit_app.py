import mss
import mss.tools
from datetime import datetime
import os

def take_screenshot(save_dir="screenshots"):
    # 保存フォルダ作成
    os.makedirs(save_dir, exist_ok=True)

    # ファイル名（日時）
    filename = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
    filepath = os.path.join(save_dir, filename)

    with mss.mss() as sct:
        # モニター全体取得（0 = 全画面）
        monitor = sct.monitors[1]

        img = sct.grab(monitor)

        # 保存
        mss.tools.to_png(img.rgb, img.size, output=filepath)

    print(f"Saved: {filepath}")
    return filepath


if __name__ == "__main__":
    take_screenshot()