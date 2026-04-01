# !usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
# import pyautogui
# import time
#
# while True:
#     print(pyautogui.position())
#     time.sleep(1)

# import pyautogui
#
# print(pyautogui.pixel(1462, 870))

# if __name__ == "__main__":
#     pass

import pyautogui
import ddddocr
import time
import io
from datetime import datetime

ocr = ddddocr.DdddOcr(show_ad=False)

# ✅ 新区域
TEST_REGION =(1205, 346, 145, 72)

def test_ocr():
    img = pyautogui.screenshot(region=TEST_REGION)

    # 保存截图（必须保留）
    ts = datetime.now().strftime("%H%M%S_%f")
    img_path = f"debug_{ts}.png"
    img.save(img_path)

    # 转 PNG bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")

    result = ocr.classification(buf.getvalue())
    text = result.strip()

    print(f"[{ts}] OCR: {repr(text)} | len={len(text)} | 图={img_path}")

if __name__ == "__main__":
    while True:
        test_ocr()
        time.sleep(1)