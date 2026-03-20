import pyautogui
import time
import random
from datetime import datetime, timedelta

# ================== 模式开关 ==================
TEST_MODE = True  # True=测试模式（无时间限制） False=正式模式

# ---------------- 初始化 ----------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

CLICK_X = 1406
CLICK_Y = 1134

last_daily_run_date = None
factory_executed_time = None  # 工厂任务上一次执行时间
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


# ---------------- 每日任务 ----------------
def daily_task():
    print(f"[{now_str()}] 开始每日任务")
    go_main_page()
    click(1071, 1170, "商店")
    rand_sleep()
    click(1215, 1089, "资源商店")
    rand_sleep()

    for i in range(5):
        if i == 0:
            before = pyautogui.pixel(1096, 895)
            pyautogui.click(1096, 895)
            time.sleep(2)
            after = pyautogui.pixel(1096, 895)
            if before == after:
                print(f"[{now_str()}] 今日宝石碎片已领完，跳过每日任务循环")
                break

        click(1096, 895, f"宝石碎片第{i + 1}次")
        time.sleep(33)
        click(1511, 258, "关闭广告")
        print(f"[{now_str()}] 执行第{i + 1}次宝石碎片领取")

        if i < 4:
            print("等待10分钟后继续下一次...")
            time.sleep(610)

    print(f"[{now_str()}] 每日任务完成")
    back_to_main_daily()


# ---------------- 工厂任务 ----------------
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

    click(x, y, "领取/确认/开始生产")
    rand_sleep()
    click(1506, 299, "关闭生产界面")
    rand_sleep()
    back_to_main_factory()
    return True


def should_run_factory(now):
    """判断是否满足延迟时间并且还没执行过工厂"""
    global factory_executed_time
    if factory_executed_time is None:
        elapsed = (now - start_script_time).total_seconds()
        return elapsed >= factory_delay_seconds
    else:
        return False


def run_factory_if_needed():
    now = datetime.now()
    if should_run_factory(now):
        factory_task(factory_choice)
        global factory_executed_time
        factory_executed_time = now
        print(f"[{now_str()}] 工厂任务执行完毕")


# ---------------- 页面跳转函数 ----------------
def go_main_page():
    click(1500, 280, "关闭深渊")
    rand_sleep()
    click(1055, 1162, "返回")
    rand_sleep()
    click(1055, 1162, "返回主页面")
    rand_sleep()


def back_to_main_daily():
    click(1269, 1174, "战斗")
    rand_sleep()
    back_common()


def back_common():
    click(1508, 1020, "活动")
    rand_sleep()
    click(1280, 448, "深渊")
    rand_sleep()
    click(1103, 1065, "仓库")
    rand_sleep()


def back_to_main_factory():
    click(1206, 1175, "战斗（工厂）")
    rand_sleep()
    back_common()


# ---------------- 主程序 ----------------
if __name__ == "__main__":
    # 用户输入工厂延迟时间
    while True:
        try:
            h = int(input("请输入工厂任务延迟小时数："))
            m = int(input("请输入工厂任务延迟分钟数："))
            factory_delay_seconds = h * 3600 + m * 60
            break
        except:
            print("输入有误，请重新输入数字")

    factory_choice = 3  # 默认选择宝石碎片，可改 1-4
    print(f"[{now_str()}] 脚本启动，3秒后开始...")
    time.sleep(3)

    start_script_time = datetime.now()  # 记录脚本启动时间

    while True:
        start_main_time = datetime.now()

        # ===== 主任务 =====
        main_click_with_check(CLICK_X, CLICK_Y)
        main_run_count += 1
        print(f"[{now_str()}] 点击完成 | 已领取次数：{main_run_count}")

        # ===== 每日任务 =====
        daily_task()

        # ===== 工厂任务 =====
        run_factory_if_needed()

        # ===== 下一轮主任务时间 =====
        interval = random.uniform(7200, 7500)
        next_time = start_main_time + timedelta(seconds=interval)
        print(f"[{now_str()}] 下次主任务时间：{next_time.strftime('%Y-%m-%d %H:%M:%S')}")
        sleep_seconds = (next_time - datetime.now()).total_seconds()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)