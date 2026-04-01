import pyautogui
import pydirectinput as input
import time
import random
from datetime import datetime
import ddddocr

# ================= OCR =================
ocr = ddddocr.DdddOcr(show_ad=False)

VICTORY_REGION = (1205, 346, 145, 72)
UPGRADE_REGION = (1176, 405, 113, 38)
EXTRA_REGION = (1500, 388, 22, 22)


# ================= 状态 =================
last_victory_time = 0
speed_active = False       # 是否已经加速
empty_exit_count = 0
run_count = 0    # 空状态计数（用于退出）
run_start_time = 0
run_durations = []
victory_buffer = []
# ================= 工具 =================
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def click_pos(x, y, desc=""):
    input.click(x, y)
    if desc:
        log(desc)


def rand_sleep(a=1, b=2):
    time.sleep(random.uniform(a, b))
#=====================图像识别=====================
def ocr_image(img):
    return ocr.classification(img).strip()


def ocr_text(region):
    img = pyautogui.screenshot(region=region)
    return ocr_image(img)


def check_victory():
    global victory_buffer

    text = ocr_text(VICTORY_REGION)
    log(f"胜利OCR: {repr(text)}")

    victory_buffer.append(text)

    if len(victory_buffer) > 3:
        victory_buffer.pop(0)

    # ✅ 条件B：识别到“胜利” → 直接返回
    if any("胜利" in t for t in victory_buffer):
        return True

    # ✅ 条件A：连续3次 T → 返回
    if len(victory_buffer) == 3 and all(t == "T" for t in victory_buffer):
        return True

    return False

# ================= 输入 =================
def press_space():
    input.keyDown("space")
    time.sleep(0.1)
    input.keyUp("space")


def click(x, y):
    input.click(x, y)


# ================= 核心检测 =================
def detect():
    global last_victory_time,run_start_time
    global speed_active, empty_exit_count

    now = time.time()

    # ================= 1. 胜利 =================
    if now - last_victory_time > 10:
        if check_victory():
            global run_count, run_start_time, run_durations
            victory_buffer.clear()
            last_victory_time = now
            run_count += 1

            if run_start_time > 0:
                duration = int(now - run_start_time)
                run_durations.append(duration)
            else:
                duration = 0

            m, s = divmod(duration, 60)
            log(f"检测到胜利 → 已刷 {run_count} 次 | 本局耗时 {m}分{s}秒")

            press_space()
            time.sleep(5)

            press_space()
            log("重新进入关卡")

            # ⭐ 关键：重新计时
            run_start_time = time.time()

            speed_active = False
            empty_exit_count = 0
            return

    # ================= 2. OCR =================
    upgrade_text = ocr_text(UPGRADE_REGION)
    speed_text = ocr_text(EXTRA_REGION)

    # if speed_text == "2":
    #     log("加速状态: 加速中")
    # else:
    #     log(f"加速状态: {repr(speed_text)}")

    # log(f"升级OCR: {repr(upgrade_text)}")

    # ================= 3. 已加速 =================
    if speed_text == "2":
        speed_active = True
        empty_exit_count = 0
        return

    # ================= 4. t逻辑 =================
    if upgrade_text and upgrade_text.lower().startswith("t"):
        # log("识别 t → 连按 1 2 3")

        for k in random.sample(["1", "2", "3"], 3):
            input.keyDown(k)
            time.sleep(0.08)
            input.keyUp(k)
            time.sleep(0.1)

        time.sleep(1)
        press_space()
        time.sleep(1)
        press_space()

        empty_exit_count = 0
        return

    # ================= 5. 升级 =================
    if "角色升级" in upgrade_text:
        key = random.choice(["1", "2", "3"])
        input.keyDown(key)
        time.sleep(0.08)
        input.keyUp(key)

        # log(f"角色升级 → 按 {key}")

        empty_exit_count = 0
        return

    # ================= 6. 空状态 =================
    if upgrade_text == "" and speed_text == "":
        empty_exit_count += 1
        # log(f"空状态计数(退出用): {empty_exit_count}")

        # ⭐ 在这里补上加速（关键）
        click(1517, 408)
        # log("空状态 → 点击加速")

        if empty_exit_count >= 3:
            log("体力耗尽，关闭程序，恢复深渊主活动")

            # 2️⃣ 点击关闭
            click_pos(1516, 516, "点击返回主界面")
            rand_sleep()

            # 3️⃣ 点击活动
            click_pos(1508, 1020, "点击活动")
            rand_sleep()

            # 4️⃣ 点击深渊
            click_pos(1280, 448, "点击深渊")
            rand_sleep()

            # 5️⃣ 点击仓库（你原逻辑）
            click_pos(1103, 1065, "点击仓库")
            rand_sleep()

            log("流程完成 → 程序退出")
            print_summary()
            raise SystemExit

        return
    else:
        empty_exit_count = 0

    # ================= 7. 兜底 =================
    press_space()
    # log("兜底 → space")
# ================= 进入关卡 =================
def enter_level():
    global run_start_time, victory_buffer

    victory_buffer.clear()   # ⭐ 必须加

    pyautogui.click(1379, 802)
    time.sleep(0.5)

    press_space()
    log("进入关卡")

    time.sleep(3)
    press_space()

    run_start_time = time.time()

# ================= 总结=================
def print_summary():
    log("========== 刷图统计 ==========")

    for i, d in enumerate(run_durations, 1):
        m, s = divmod(d, 60)
        log(f"第{i}次：{m}分{s}秒")

    if run_durations:
        total = sum(run_durations)
        avg = total / len(run_durations)
        m, s = divmod(int(avg), 60)
        log(f"平均耗时：{m}分{s}秒")

# ================= 战斗循环 =================
def battle_loop():
    log("战斗循环启动")

    while True:
        detect()
        time.sleep(random.randint(5, 10))


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
    print("5s后开始挂机")
    time.sleep(5)
    main()