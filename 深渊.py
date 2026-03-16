import pyautogui
import time
import random
from datetime import datetime, timedelta

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

CLICK_X = 1406
CLICK_Y = 1134

last_daily_run_date = None
main_run_count = 0


# ---------------- 随机点击 ----------------
def click(x, y, delta=2):
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.click(rx, ry)


# ---------------- 随机等待 ----------------
def rand_sleep(a=2, b=3):
    time.sleep(random.uniform(a, b))


# ---------------- 每日任务 ----------------
def daily_task():

    print("开始执行每日任务")

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

    click(1263, 1165)  # 点击战斗
    print("点击战斗")
    rand_sleep()

    click(1508, 1020)  # 活动
    print("点击活动")
    rand_sleep()

    click(1280, 448)   # 深渊
    print("点击深渊")
    rand_sleep()

    click(1103, 1065)  # 仓库
    print("点击仓库")
    rand_sleep()

    print("每日任务执行完毕")
    print("=" * 50)


print("脚本启动，3秒后开始...")
print("执行仓库")
time.sleep(3)

while True:

    # ---------------- 主任务 ----------------
    click(CLICK_X, CLICK_Y)
    rand_sleep()

    click(CLICK_X, CLICK_Y)

    main_run_count += 1

    now = datetime.now()

    print(f"点击完成时间：{now.strftime('%Y-%m-%d %H:%M:%S')} | 已领取次数：{main_run_count}")

    # -------- 计算下一次主任务 --------
    interval = random.uniform(7200, 7500)
    next_main_time = now + timedelta(seconds=interval)

    print("下次主任务时间：", next_main_time.strftime("%Y-%m-%d %H:%M:%S"))

    # ---------------- 每日任务判断 ----------------
    if (
        last_daily_run_date != now.date()
        and now.hour >= 6
        and (next_main_time - now).total_seconds() >= 3600
    ):
        daily_task()
        last_daily_run_date = now.date()

        # 每日任务结束后再次打印主任务时间
        print("每日任务结束")
        print("下次主任务时间：", next_main_time.strftime("%Y-%m-%d %H:%M:%S"))

    # ---------------- 等待下一次 ----------------
    print("等待约 2小时 ~ 2小时5分钟")
    print("-" * 40)

    time.sleep(interval)