import pyautogui
import time
import random
from datetime import datetime, timedelta

# ---------------- 初始化 ----------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

CLICK_X = 1406
CLICK_Y = 1134

last_daily_run_date = None
factory_executed_date = None
main_run_count = 0
factory_choice = None

# ---------------- 工具函数 ----------------
def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def click(x, y, desc="", delta=2):
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.click(rx, ry)
    if desc:
        print(f"[{now_str()}] 点击：{desc}")

def rand_sleep(a=2, b=3):
    time.sleep(random.uniform(a, b))

def is_color_match(pixel, target, tolerance=15):
    return all(abs(p - t) <= tolerance for p, t in zip(pixel, target))

# ---------------- 回主页面 ----------------
def go_main_page():
    click(1500, 280, "关闭深渊")
    rand_sleep()

    click(1055, 1162, "返回")
    rand_sleep()

    click(1055, 1162, "返回主页面")
    rand_sleep()

# ---------------- 回仓库（每日任务） ----------------
def back_to_main_daily():
    click(1269, 1174, "战斗")
    rand_sleep()
    back_common()

# ---------------- 回仓库（生产工厂） ----------------
def back_to_main_factory():
    click(1206, 1175, "战斗（工厂）")
    rand_sleep()
    back_common()

# ---------------- 公共路径 ----------------
def back_common():
    click(1508, 1020, "活动")
    rand_sleep()

    click(1280, 448, "深渊")
    rand_sleep()

    click(1103, 1065, "仓库")
    rand_sleep()

# ---------------- 主任务 ----------------
def main_click_with_check(x, y, delta=2, check_point=None):
    if check_point is None:
        check_point = (x, y)

    before = pyautogui.pixel(*check_point)

    click(x, y, "主任务点击")
    time.sleep(3)

    after = pyautogui.pixel(*check_point)

    if before != after:
        click(x, y, "补点击1次")
    else:
        for _ in range(2):
            click(x, y, "补点击2次")
            time.sleep(2)

    print(f"[{now_str()}] 主任务点击成功")

# ---------------- 领取+开始生产 ----------------
def collect_confirm_start(x, y):
    pixel = pyautogui.pixel(x, y)

    # ✔ 可领取颜色（带容差）
    if not is_color_match(pixel, (255, 216, 65), 20):
        print(f"[{now_str()}] 正在生产中，跳过")
        return False

    click(x, y, "领取")
    rand_sleep()

    click(x, y, "确认")
    rand_sleep()

    click(x, y, "开始生产")
    rand_sleep()

    return True

# ---------------- 生产工厂 ----------------
def factory_task(choice):
    print(f"[{now_str()}] 执行生产工厂")

    go_main_page()

    click(1353, 1174, "进入领地")
    rand_sleep()

    for _ in range(3):
        pyautogui.scroll(-300)
        print(f"[{now_str()}] 滚轮向下")
        time.sleep(0.3)
    rand_sleep()

    click(1549, 790, "生产工厂")
    rand_sleep()

    click(1334, 768, "生产")
    rand_sleep()
    resource_map = {
        1: (1470, 671, "图纸"),
        2: (1417, 776, "钻石"),
        3: (1476, 980, "宝石碎片"),
        4: (1435, 1075, "电池")
    }

    x, y, name = resource_map[choice]
    print(f"[{now_str()}] 选择生产：{name}")

    success = collect_confirm_start(x, y)

    click(1506, 299, "关闭生产界面")
    rand_sleep()

    back_to_main_factory()

    return success

# ---------------- 生产条件 ----------------
def should_run_factory(now):
    global factory_executed_date

    hour = now.hour
    in_window = (hour >= 22 or hour < 8)

    if not in_window:
        return False

    if hour >= 22:
        window_date = now.date()
    else:
        window_date = (now - timedelta(days=1)).date()

    if factory_executed_date == window_date:
        return False

    return True

def run_factory_if_needed():
    global factory_executed_date

    now = datetime.now()

    if not should_run_factory(now):
        return

    print(f"[{now_str()}] 满足生产工厂执行条件")

    success = factory_task(factory_choice)

    if success:
        if now.hour >= 22:
            factory_executed_date = now.date()
        else:
            factory_executed_date = (now - timedelta(days=1)).date()

        print(f"[{now_str()}] 本时间段生产完成")

# ---------------- 每日任务 ----------------
def should_run_daily(now, next_time):
    global last_daily_run_date

    in_window = (
        (5 <= now.hour < 8) or
        (now.hour == 8 and now.minute < 5)
    )

    if not in_window:
        return False

    if last_daily_run_date == now.date():
        return False

    remain = (next_time - now).total_seconds()
    if remain < 3600:
        print(f"[{now_str()}] 距离主任务不足1小时，跳过每日任务")
        return False

    return True

def daily_task():
    print(f"[{now_str()}] 开始每日任务")

    go_main_page()

    click(1071, 1170, "商店")
    rand_sleep()

    click(1215, 1089, "资源商店")
    rand_sleep()

    for i in range(5):
        start_time = now_str()

        if i == 0:
            before = pyautogui.pixel(1096, 895)
            click(1096, 895, "宝石碎片检测")
            time.sleep(2)
            after = pyautogui.pixel(1096, 895)

            if before == after:
                print(f"[{now_str()}] 今日宝石碎片已领完")
                break

        click(1096, 895, f"宝石碎片第{i+1}次")
        time.sleep(33)

        click(1511, 258, "关闭广告")
        print(f"[{start_time}] 第{i + 1}次领取完成")

        if i < 4:
            print(f"[{now_str()}] 等待10分钟")
            time.sleep(610)

    print(f"[{now_str()}] 每日任务完成")

    back_to_main_daily()

# ---------------- 选择生产 ----------------
def choose_factory():
    print("====== 请选择生产类型 ======")
    print("1 - 图纸")
    print("2 - 钻石")
    print("3 - 宝石碎片")
    print("4 - 电池")

    while True:
        try:
            c = int(input("请输入(1-4)："))
            if c in [1,2,3,4]:
                return c
        except:
            pass
        print("输入错误")

# ---------------- 主程序 ----------------
if __name__ == "__main__":
    factory_choice = choose_factory()

    print(f"[{now_str()}] 脚本启动，3秒后开始...")
    time.sleep(3)

    while True:
        start_main_time = datetime.now()

        # ===== 主任务 =====
        main_click_with_check(CLICK_X, CLICK_Y)
        main_run_count += 1

        now = datetime.now()
        print(f"[{now_str()}] 点击完成 | 已领取次数：{main_run_count}")

        # ===== 提前计算下次时间 =====
        interval = random.uniform(7200, 7500)
        next_time = start_main_time + timedelta(seconds=interval)

        # ===== 生产工厂 =====
        run_factory_if_needed()

        # ===== 每日任务 =====
        if should_run_daily(now, next_time):
            daily_task()
            last_daily_run_date = now.date()

        # ===== 下一轮 =====
        print(f"[{now_str()}] 下次主任务时间：{next_time.strftime('%Y-%m-%d %H:%M:%S')}")

        sleep_seconds = (next_time - datetime.now()).total_seconds()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)