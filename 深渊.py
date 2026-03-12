#!usr/bin/env python3.11
# -*- coding: utf-8 -*-

import pyautogui
import time
from datetime import datetime

INTERVAL = 2 * 3610   # 2小时 + 10秒冗余

pyautogui.FAILSAFE = True

print("程序启动，5秒后开始执行...")
time.sleep(2)

# ===== 1-5 只执行一次 =====

# 1 双击
pyautogui.doubleClick(180, 1144)

# 2 等待30秒
time.sleep(20)

# 3
pyautogui.click(1497, 1019)

time.sleep(2)

# 4
pyautogui.click(1350, 451)

time.sleep(2)
# 5
pyautogui.click(1125, 1063)

time.sleep(2)

print("初始化操作完成")

# ===== 6-10 循环 =====
while True:

    # 6
    pyautogui.click(1406, 1134)

    # 7
    time.sleep(2)

    # 8
    pyautogui.click(1406, 1134)

    # 9 打印当前时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"点击完成，时间：{now}")

    # 10 最小化
    pyautogui.click(1784, 1422)

    print("等待2小时...")

    time.sleep(INTERVAL)

    # 恢复窗口
    pyautogui.click(1784, 1422)