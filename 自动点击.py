import pyautogui
import time

DELAY = 12 * 3600 + 41 * 60   # 45660 秒

pyautogui.FAILSAFE = True

click_points = [
    (2371, 877),
    (2418, 967),
    (2425, 1166),
    (2425, 1166),
    (2425, 1166),
]

print("程序启动，开始等待 12小时41分钟...")
time.sleep(DELAY)

print("开始执行点击...")

for x, y in click_points:
    pyautogui.click(x, y)
    print(f"已点击 ({x}, {y})")
    time.sleep(1)

print("执行完成，程序结束")