import pyautogui
import time

DELAY = 4 * 3600 + 12 * 60

pyautogui.FAILSAFE = True

click_points = [
    (2264, 844),
    (2311, 949),
    (2364,1128),
    (2364,1128),
    (2364,1128),
]

print("程序启动，开始等待...")
time.sleep(DELAY)

print("开始执行点击...")

for x, y in click_points:
    pyautogui.click(x, y)
    print(f"已点击 ({x}, {y})")
    time.sleep(1)

print("执行完成，程序结束")