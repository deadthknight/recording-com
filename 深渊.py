#!usr/bin/env python3.11
# -*- coding: utf-8 -*-

import pyautogui
import time
import random
from datetime import datetime

# 基础循环间隔 2小时 + 10秒冗余
BASE_INTERVAL = 2 * 3610

pyautogui.FAILSAFE = True

def rand_click(x, y, delta=3):
    """
    在坐标(x, y)附近随机偏移点击
    delta: 最大像素偏移量
    """
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.click(rx, ry)

def rand_double_click(x, y, delta=3):
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.doubleClick(rx, ry)

def rand_sleep(base, variation=0.1):
    """
    base: 基础时间
    variation: 浮动比例，例如0.1表示±10%
    """
    interval = base * random.uniform(1 - variation, 1 + variation)
    time.sleep(interval)

# ===== 启动等待 =====
print("程序启动，5秒后开始执行...")
rand_sleep(5, 0.1)  # 启动等待 ±10%浮动

# ===== 1-5 只执行一次 =====

# 1 双击
rand_double_click(180, 1144)

# 2 等待约30秒
rand_sleep(10, 0.2)  # ±20%浮动

# 3 点击
rand_click(1497, 1019)
rand_sleep(2, 0.2)

# 4 点击
rand_click(1350, 451)
rand_sleep(2, 0.2)

# 5 点击
rand_click(1125, 1063)
rand_sleep(2, 0.2)

print("初始化操作完成")

# ===== 6-10 循环 =====
while True:

    # 6 点击
    rand_click(1406, 1134)
    rand_sleep(2, 0.2)

    # 8 点击
    rand_click(1406, 1134)

    # 9 打印当前时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"点击完成，时间：{now}")

    # 10 最小化
    rand_click(1784, 1422)

    print("等待约2小时...")
    rand_sleep(BASE_INTERVAL, 0.1)  # 主循环等待 ±10%浮动

    # 恢复窗口
    rand_click(1784, 1422)