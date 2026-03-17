import pyautogui
import time
import random
from datetime import datetime, timedelta

# ---------------- 初始化 ----------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0

CLICK_X = 1406
CLICK_Y = 1134

last_daily_run_date = None
main_run_count = 0

# ---------------- 随机点击 ----------------
def click(x, y, delta=2):
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.click(rx, ry)

# ---------------- 主任务安全点击 ----------------
def main_click_with_check(x, y, delta=2, check_point=None):
    if check_point is None:
        check_point = (x, y)

    before = pyautogui.pixel(check_point[0], check_point[1])

    # 第一次点击
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.click(rx, ry)

    # 等3秒
    time.sleep(3)

    after = pyautogui.pixel(check_point[0], check_point[1])

    if before != after:
        # 像素变化，再点击1次
        rx = x + random.randint(-delta, delta)
        ry = y + random.randint(-delta, delta)
        pyautogui.click(rx, ry)
        print("像素变化，再点击1次")
    else:
        # 像素没变化，再点击2次
        print("像素未变化，再点击2次")
        for _ in range(2):
            rx = x + random.randint(-delta, delta)
            ry = y + random.randint(-delta, delta)
            pyautogui.click(rx, ry)
            time.sleep(2)

    print("主任务点击成功")

# ---------------- 随机等待 ----------------
def rand_sleep(a=2, b=3):
    time.sleep(random.uniform(a, b))

# ---------------- 每日任务 ----------------
def daily_task():
    print(f"[{datetime.now()}] 开始执行每日任务")

    click(1500, 280)
    rand_sleep()
    click(1055, 1162)
    rand_sleep()
    click(1055, 1162)
    rand_sleep()
    click(1071, 1170)
    rand_sleep()
    click(1215, 1089)
    rand_sleep()

    for i in range(5):
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        click(1096, 895)
        time.sleep(33)
        click(1511, 258)
        print(f"[{start_time}] 执行第{i + 1}次完毕")
        if i < 4:
            print("等待10分钟后继续下一次...")
            time.sleep(610)

    print("宝石碎片程序全部执行完毕")
    rand_sleep()
    click(1263, 1165)
    print("点击战斗")
    rand_sleep()
    click(1508, 1020)
    print("点击活动")
    rand_sleep()
    click(1280, 448)
    print("点击深渊")
    rand_sleep()
    click(1103, 1065)
    print("点击仓库")
    rand_sleep()

    print(f"[{datetime.now()}] 每日任务执行完毕")
    print("=" * 50)

# ---------------- 主循环 ----------------
print(f"[{datetime.now()}] 脚本启动，3秒后开始...")
time.sleep(3)

while True:
    start_main_time = datetime.now()

    # ===== 主任务 =====
    main_click_with_check(CLICK_X, CLICK_Y)
    main_run_count += 1
    now = datetime.now()
    print(f"[{now}] 点击完成时间 | 已领取次数：{main_run_count}")

    # ===== 计算下一次主任务时间 =====
    interval = random.uniform(7200, 7500)  # 2小时 ~ 2小时5分钟
    next_main_time = start_main_time + timedelta(seconds=interval)

    # ===== 每日任务判断 =====
    if last_daily_run_date != now.date() and now.hour >= 6 and (next_main_time - now).total_seconds() >= 3600:
        daily_task()
        last_daily_run_date = now.date()
        # 每日任务结束后，不改变 next_main_time

    # ===== 等待到下一次主任务 =====
    sleep_seconds = (next_main_time - datetime.now()).total_seconds()
    print(f"[{datetime.now()}] 等待 {int(sleep_seconds)} 秒后执行下一轮主任务 | 下次主任务时间：{next_main_time.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(sleep_seconds)