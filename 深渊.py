import pyautogui
import time
import random
from datetime import datetime, timedelta

pyautogui.FAILSAFE = True

CLICK_X = 1406
CLICK_Y = 1134

# 点击函数（不移动鼠标）
def click(x, y):
    pyautogui.click(x, y)

# 随机等待 2小时 ~ 2小时5分钟
def wait_next():
    interval = random.uniform(7200, 7500)

    next_time = datetime.now() + timedelta(seconds=interval)

    print("等待约 2小时 ~ 2小时5分钟")
    print("下次点击时间：", next_time.strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 40)

    time.sleep(interval)

print("脚本启动，3秒后开始...")
time.sleep(3)

while True:

    # 点击两次
    click(CLICK_X, CLICK_Y)
    time.sleep(2)
    click(CLICK_X, CLICK_Y)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("点击完成时间：", now)

    # 等待下一次
    wait_next()