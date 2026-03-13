import pyautogui
import time
from datetime import datetime

print("程序将在5秒后开始执行...")
time.sleep(5)

for i in range(5):
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pyautogui.click(1165, 814)
    time.sleep(33)
    pyautogui.click(1598, 203)
    print(f"[{start_time}] 执行第{i + 1}次完毕")

    if i < 4:  # 最后一次不需要再等待
        print("等待10分钟后继续下一次...")
        time.sleep(610)  # 10分钟 = 600秒

print("程序全部执行完毕")