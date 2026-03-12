#!usr/bin/env python3.11
# -*- coding: utf-8 -*-

import pyautogui
import time
import random
from datetime import datetime

pyautogui.FAILSAFE = True  # 可以保留，用户把鼠标移到屏幕角仍会停止脚本

# ------------------ 随机点击函数 ------------------
def rand_click(x, y, delta=3):
    """在坐标(x, y)附近随机偏移点击"""
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.click(rx, ry)

def rand_double_click(x, y, delta=3):
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.doubleClick(rx, ry)

def rand_sleep(base, variation=0.1):
    """随机浮动睡眠"""
    interval = base * random.uniform(1 - variation, 1 + variation)
    time.sleep(interval)

def rand_sleep_2h_range():
    """主循环随机等待 2小时 ~ 2小时5分钟"""
    interval = random.uniform(7200, 7500)  # 秒
    time.sleep(interval)

# ------------------ 启动延迟 ------------------
print("程序启动，5秒后开始执行...")
rand_sleep(5, 0.1)  # 启动延迟 ±10%

# ------------------ 初始化操作 1-5 ------------------
rand_double_click(180, 1144)       # 1 双击
rand_sleep(10, 0.2)                # 2 等待约10秒 ±20%
rand_click(1497, 1019)             # 3 点击
rand_sleep(2, 0.2)
rand_click(1350, 451)              # 4 点击
rand_sleep(2, 0.2)
rand_click(1125, 1063)             # 5 点击
rand_sleep(2, 0.2)

print("初始化操作完成")

# ------------------ 循环操作 6-10 ------------------
while True:
    rand_click(1406, 1134)          # 6 点击
    rand_sleep(2, 0.2)
    rand_click(1406, 1134)          # 8 再次点击

    # 9 打印当前时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"点击完成，时间：{now}")

    # 10 最小化
    rand_click(1746, 1419)

    print("等待约2小时~2小时5分钟...")
    rand_sleep_2h_range()           # 主循环等待

    # 恢复窗口
    rand_click(1746, 1419)