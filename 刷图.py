import pyautogui
import time
import os
from datetime import datetime
import ddddocr
import re

# ================== 初始化 ==================
ocr = ddddocr.DdddOcr(show_ad=False)

LEFT = 1260
TOP = 953
RIGHT = 1312
BOTTOM = 970

SAVE_DIR = "ocr_test_imgs"
os.makedirs(SAVE_DIR, exist_ok=True)

saved_files = []

# 连续识别不到次数
fail_count = 0

# ================== 工具函数 ==================
def now_str():
    return datetime.now().strftime('%H:%M:%S')

def log(tag, msg):
    print(f"[{tag}][{now_str()}] {msg}")

def fix_ocr_digit(text):
    """纠正常见OCR误识别字符"""
    mapping = {
        'V': '1',
        'I': '1',
        'l': '1',
        '|': '1',
        'O': '0',
        'o': '0',
        'S': '5',
        's': '5'
    }
    return ''.join(mapping.get(c, c) for c in text)

def parse_energy(ocr_text):
    """解析OCR结果成 current/max"""
    ocr_text = fix_ocr_digit(ocr_text)
    ocr_text = re.sub(r'[^0-9/]', '', ocr_text)  # 保留数字和 /
    if '/' not in ocr_text:
        return None, None
    parts = ocr_text.split('/')
    if len(parts) != 2:
        return None, None
    try:
        current = int(parts[0])
        maximum = int(parts[1])
        return current, maximum
    except:
        return None, None

def screenshot_and_ocr():
    global saved_files
    start_time = time.time()

    img = pyautogui.screenshot(region=(LEFT, TOP, RIGHT - LEFT, BOTTOM - TOP))
    img = img.resize((img.width * 2, img.height * 2))
    img = img.convert('L')

    text = ocr.classification(img)

    # 保存截图
    filename = f"{SAVE_DIR}/{datetime.now().strftime('%H%M%S')}.png"
    img.save(filename)
    saved_files.append(filename)
    log("截图", f"保存：{filename}")

    # 只保留最近2张
    if len(saved_files) > 2:
        old_file = saved_files.pop(0)
        if os.path.exists(old_file):
            os.remove(old_file)
            log("清理", f"删除旧截图：{old_file}")

    cost = round(time.time() - start_time, 2)
    return text, cost

# ================== 主循环 ==================
log("系统", "开始OCR截图测试（3分钟一次）")

while True:
    text, cost = screenshot_and_ocr()
    current, maximum = parse_energy(text)

    if current is None or maximum is None:
        fail_count += 1
        log("识别", f"OCR结果异常：{text} | 连续失败次数：{fail_count}")
    else:
        fail_count = 0
        log("识别", f"OCR结果：{current}/{maximum}")
        # 判断体力是否够 5
        if current < 5:
            log("系统", f"体力不足（{current}/{maximum}），程序终止")
            break
        else:
            log("系统", f"体力足够（{current}/{maximum}），进入刷材料流程")
            # ⭐ 这里可以调用刷材料函数，例如：
            # run_materials_cycle()

    log("性能", f"本次OCR耗时：{cost} 秒")

    if fail_count >= 2:
        log("系统", "连续两次识别不到，判断在关卡中，暂停进入新关卡")
        fail_count = 0  # 重置计数
    else:
        log("系统", "等待3分钟后进行下一次识别...\n")
        time.sleep(180)  # 3分钟