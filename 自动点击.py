import pyautogui
import time
import random
from datetime import datetime, timedelta
import threading

# ================== 模式开关 ==================
TEST_MODE = True  # True=测试模式（无时间限制） False=正式模式

# ---------------- 初始化 ----------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 深渊点击位置（固定）
ABYSS_CLICK_X = 1469
ABYSS_CLICK_Y = 1131

last_daily_run_date = None
main_run_count = 0
factory_done = False

# ---------------- 工具函数 ----------------
def now_str():
    return datetime.now().strftime('%H:%M')

def click(x, y, desc="", delta=2):
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.click(rx, ry)
    if desc:
        print(f"[{now_str()}] 点击：{desc}")

def rand_sleep(a=2, b=3):
    time.sleep(random.uniform(a, b))

# ---------------- 主任务 ----------------
def main_task():
    global main_run_count
    while True:
        before = pyautogui.pixel(ABYSS_CLICK_X, ABYSS_CLICK_Y)
        click(ABYSS_CLICK_X, ABYSS_CLICK_Y, "深渊点击领取")
        time.sleep(3)
        after = pyautogui.pixel(ABYSS_CLICK_X, ABYSS_CLICK_Y)
        if before != after:
            click(ABYSS_CLICK_X, ABYSS_CLICK_Y, "确认")
            print(f"[{now_str()}] 材料已领取")
        else:
            print(f"[{now_str()}] 像素未变化，不再点击")
        main_run_count += 1
        print(f"[{now_str()}] 深渊材料已领取完成 | 已领取次数：{main_run_count}")

        # 随机等待2小时左右
        interval = random.uniform(7200, 7500)
        next_time = datetime.now() + timedelta(seconds=interval)
        print(f"[{now_str()}] 下一轮主任务预计执行时间：{next_time.strftime('%H:%M')}")
        if factory_choice != 0 and not factory_done:
            next_factory_time = factory_start_time
            print(f"[{now_str()}] 工厂任务预计执行时间：{next_factory_time.strftime('%H:%M')}")
        time.sleep(interval)

# ---------------- 每日任务 ----------------
def daily_task():
    global last_daily_run_date
    GEM_X, GEM_Y = 1096, 895
    AD_CLOSE_X, AD_CLOSE_Y = 1511, 258
    while True:
        now = datetime.now()
        hour = now.hour
        today = now.date()
        if 5 <= hour < 8 and last_daily_run_date != today:
            start_time = now_str()
            print(f"[{start_time}] 开始每日任务")
            for i in range(5):
                if i == 0:
                    before = pyautogui.pixel(GEM_X, GEM_Y)
                    pyautogui.click(GEM_X, GEM_Y)
                    time.sleep(2)
                    after = pyautogui.pixel(GEM_X, GEM_Y)
                    if before == after:
                        print(f"[{now_str()}] 今日宝石碎片已领完，跳过每日任务循环")
                        break
                click(GEM_X, GEM_Y, f"宝石碎片第{i+1}次")
                time.sleep(33)
                click(AD_CLOSE_X, AD_CLOSE_Y, "关闭广告")
                print(f"[{start_time}] 执行第{i+1}次宝石碎片领取")
                if i < 4:
                    print(f"[{now_str()}] 等待10分钟后继续下一次...")
                    time.sleep(610)
            last_daily_run_date = datetime.now().date()
            print(f"[{now_str()}] 每日任务完成")
        time.sleep(30)  # 每30秒检查一次时间

# ---------------- 工厂任务 ----------------
# 工厂材料领取+生产坐标
MATERIAL_COORDS = {
    1: {"click": (1478, 672), "start_prod": (1454, 774)},  # 图纸
    2: {"click": (1478, 872), "start_prod": (1454, 874)},  # 钻石
    3: {"click": (1478, 972), "start_prod": (1454, 974)},  # 宝石碎片
    4: {"click": (1478, 1072), "start_prod": (1454, 1074)} # 电池
}

def lingdi_production_task():
    material_x, material_y = MATERIAL_COORDS[factory_choice]["click"]
    start_prod_x, start_prod_y = MATERIAL_COORDS[factory_choice]["start_prod"]

    print(f"[{now_str()}] 开始工厂任务，生产材料 {factory_choice}")
    click(material_x, material_y, "领取")
    rand_sleep()
    click(start_prod_x, start_prod_y, "开始生产")
    rand_sleep()
    # 返回主流程
    click(1210, 1167); print("点击战斗"); rand_sleep()
    click(1508, 1020); print("点击活动"); rand_sleep()
    click(1280, 448); print("点击深渊"); rand_sleep()
    click(1103, 1065); print("点击仓库"); rand_sleep()
    print(f"[{now_str()}] 工厂任务完成")

def factory_task_at_time(delay_seconds):
    global factory_start_time, factory_done
    factory_start_time = datetime.now() + timedelta(seconds=delay_seconds)
    print(f"[{now_str()}] 工厂任务将在 {factory_start_time.strftime('%H:%M')} 执行")
    while True:
        now = datetime.now()
        if now >= factory_start_time:
            lingdi_production_task()
            factory_done = True
            break
        time.sleep(5)

# ---------------- 工厂选择 ----------------
def choose_factory_material():
    print("====== 请选择生产类型 ======")
    print("0 - 不执行工厂任务")
    print("1 - 图纸")
    print("2 - 钻石")
    print("3 - 宝石碎片")
    print("4 - 电池")
    while True:
        try:
            c = int(input("请输入(0-4)："))
            if c in [0, 1, 2, 3, 4]:
                return c
        except:
            pass
        print("输入错误，请重新输入")

# ---------------- 主程序 ----------------
if __name__ == "__main__":
    factory_choice = choose_factory_material()
    if factory_choice == 0:
        factory_delay_seconds = None
    else:
        while True:
            try:
                h = int(input("请输入工厂任务延迟小时数："))
                m = int(input("请输入工厂任务延迟分钟数："))
                factory_delay_seconds = h * 3600 + m * 60
                break
            except:
                print("输入有误，请重新输入数字")

    print(f"[{now_str()}] 脚本启动...")

    # ===== 启动线程 =====
    threads = []

    t_main = threading.Thread(target=main_task, daemon=True)
    threads.append(t_main)
    t_main.start()

    t_daily = threading.Thread(target=daily_task, daemon=True)
    threads.append(t_daily)
    t_daily.start()

    if factory_choice != 0:
        t_factory = threading.Thread(target=factory_task_at_time, args=(factory_delay_seconds,), daemon=True)
        threads.append(t_factory)
        t_factory.start()

    # 主线程保持活跃
    for t in threads:
        t.join()