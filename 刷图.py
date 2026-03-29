import pyautogui
import pydirectinput as input
import time
import os
import random
from datetime import datetime
import ddddocr

# ================= OCR =================
ocr = ddddocr.DdddOcr(show_ad=False)


UPGRADE_REGION = (1176, 405, 113, 38)
EXTRA_REGION = (1500, 388, 22, 22)

IMG_DIR = r"D:\PycharmProjects\recording-com\ocr_debug"

# ================= 状态 =================
is_speed_mode = False
empty_count = 0
exit_lock_until = 0
speed_lock = False
speed_triggered = False
exit_count = 0


# ================= 工具 =================
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def save_img(img, prefix):
    # ⭐ 只保留 energy 调试图
    if prefix != "energy":
        return

    os.makedirs(IMG_DIR, exist_ok=True)
    img.save(os.path.join(IMG_DIR, f"{prefix}_{datetime.now().strftime('%H%M%S')}.png"))


# ================= OCR =================
def ocr_text(region, scale=2):
    img = pyautogui.screenshot(region=region)
    img = img.resize((img.width * scale, img.height * scale)).convert("L")
    return ocr.classification(img).strip()


# ================= 输入 =================
def press_space():
    input.keyDown("space")
    time.sleep(0.1)
    input.keyUp("space")


def click(x, y):
    input.click(x, y)


# ================= 核心检测 =================
def detect():
    global empty_count, exit_lock_until,exit_count

    now = time.time()

    upgrade_text = ocr_text(UPGRADE_REGION, 2)
    extra_text = ocr_text(EXTRA_REGION, 3)

    log(f"升级OCR: {repr(upgrade_text)}")
    log(f"额外OCR: {repr(extra_text)}")

    # ================= 1. 已加速状态（最优先）=================
    if extra_text == "2":
        empty_count = 0  # 成功后清空计数
        exit_count = 0
        # 已经加速成功 → 不做任何操作
        return

    # ================= 2. 空状态逻辑（未加速才会进）=================
    is_empty = (upgrade_text == "" and extra_text == "")

    if is_empty:

        empty_count += 1
        log(f"空状态：{empty_count}/3")

        if empty_count <= 2:
            click(1517, 408)
            log("空状态 → 点击加速")
            return

        if empty_count >= 3 and now > exit_lock_until:
            exit_lock_until = now + 5

            log("连续3次空 → 回主界面")

            press_space()
            time.sleep(5)

            empty_count = 0

            # ⭐新增：体力验证
            check_stamina_and_exit()



            return

        return

    else:
        empty_count = 0

    # ================= 3. 战斗逻辑 =================
    if "角色升级" in upgrade_text:
        key = random.choice(["1", "2", "3"])
        input.keyDown(key)
        time.sleep(0.08)
        input.keyUp(key)
        log(f"角色升级 → 按 {key}")
        return

    # ================= t 逻辑 =================
    if upgrade_text.startswith("t"):
        log("识别 t → 连按 1 2 3")

        for k in random.sample(["1", "2", "3"], 3):
            input.keyDown(k)
            time.sleep(0.08)
            input.keyUp(k)
            time.sleep(0.1)

        time.sleep(0.1)
        press_space()
        log("t逻辑结束 → 补空格")

        return

    # ================= 默认战斗 =================
    press_space()
    log("默认战斗 → space")


# ================= 进入关卡 =================
def enter_level():
    pyautogui.click(1379, 802)
    time.sleep(0.5)

    press_space()
    log("进入关卡")

    time.sleep(3)
    press_space()

    return True


# ================= 战斗循环 =================
def battle_loop():
    log("战斗循环启动")

    while True:

        detect()

        time.sleep(random.randint(5, 10))

def check_stamina_and_exit():
    global empty_count

    log("开始体力验证：按空格尝试进入")

    # 1️⃣ 尝试进入关卡
    press_space()
    time.sleep(3)

    # 2️⃣ 连续检测3次
    empty_count = 0

    for i in range(3):
        upgrade_text = ocr_text(UPGRADE_REGION, 2)
        extra_text = ocr_text(EXTRA_REGION, 3)

        log(f"[体力检测{i+1}] {upgrade_text} | {extra_text}")

        is_empty = (upgrade_text.strip() == "" and extra_text.strip() == "")

        if is_empty:
            empty_count += 1
        else:
            log("体力恢复/可进入关卡 → 继续运行")
            return False

        time.sleep(1)

    # 3️⃣ 连续3次空 → 体力不足
    log("连续3次OCR为空 → 体力不足，退出程序")
    raise SystemExit
# ================= 主流程 =================
def main():
    log("启动")

    pyautogui.click(1112, 200)
    log("切换到游戏窗口")
    time.sleep(3)

    while True:
        enter_level()
        battle_loop()


if __name__ == "__main__":
    time.sleep(5)
    main()