import pyautogui
import time
import random
from datetime import datetime, timedelta

# ================== 模式开关 ==================
TEST_MODE = True  # True=测试模式（无时间限制） False=正式模式

# ---------------- 初始化 ----------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 深渊点击坐标（固定）
CLICK_X = 1469
CLICK_Y = 1131

# 材料坐标（工厂任务选择）
MATERIAL_COORDS = {
    1: (1478, 672),   # 图纸
    2: (1478, 872),   # 钻石
    3: (1478, 972),   # 宝石碎片
    4: (1478, 1072)   # 电池
}

# ---------------- 全局变量 ----------------
last_daily_run_date = None
main_run_count = 0

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

def calc_next_main_time():
    interval = random.uniform(7200, 7500)
    return datetime.now() + timedelta(seconds=interval)

# ---------------- 主任务 ----------------
def main_task_once():
    global main_run_count

    before = pyautogui.pixel(CLICK_X, CLICK_Y)
    click(CLICK_X, CLICK_Y, "深渊点击领取")
    time.sleep(3)
    after = pyautogui.pixel(CLICK_X, CLICK_Y)

    if before != after:
        # 像素有变化，点击两次
        click(CLICK_X, CLICK_Y, "确认")
        print(f"[{now_str()}] 领取材料")
    else:
        print(f"[{now_str()}] 像素未变化，不再点击")

    main_run_count += 1
    print(f"[{now_str()}] 深渊材料已领取完成 | 已领取次数：{main_run_count}")

# ---------------- 每日任务 ----------------
def daily_task_once(next_main_time=None):
    global last_daily_run_date
    GEM_X, GEM_Y = 1096, 895
    AD_CLOSE_X, AD_CLOSE_Y = 1511, 258

    today = datetime.now().date()
    if last_daily_run_date == today:
        print(f"[{now_str()}] 今日每日任务已执行过，跳过")
        return

    start_time = now_str()
    print(f"[{start_time}] 开始每日任务")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始每日任务前置动作")

    # 前置操作
    click(1500, 280)  # 关闭深渊
    rand_sleep()
    click(1055, 1162)  # 深渊返回
    rand_sleep()
    click(1055, 1162)  # 返回主页面
    rand_sleep()
    click(1071, 1170)  # 商店
    rand_sleep()
    click(1215, 1089)  # 资源商店
    rand_sleep()

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

    # 后续动作
    print("宝石碎片程序全部执行完毕（或跳过循环）")
    rand_sleep()
    click(1263, 1165)
    print("点击战斗")
    rand_sleep()
    click(1508, 1020)
    print("点击活动")
    rand_sleep()
    click(1280, 448)
    print("点击深渊")
    rand_sleep()
    click(1103, 1065)
    print("点击仓库")
    rand_sleep()

    print(f"[{now_str()}] 每日任务完成")
    if next_main_time is not None:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 每日任务执行完毕，下一轮主任务时间：{next_main_time.strftime('%H:%M')}")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 每日任务执行完毕")
    print("=" * 50)

# ---------------- 工厂任务 ----------------
def lingdi_production_task(get_choice, prod_choice):
    get_x, get_y = MATERIAL_COORDS[get_choice]
    prod_x, prod_y = MATERIAL_COORDS[prod_choice]
    print(f"[{now_str()}] 开始工厂任务，领取材料 {get_choice}，生产材料 {prod_choice}")

    click(1500, 280)  # 关闭深渊
    rand_sleep()
    click(1055, 1162)  # 深渊返回
    rand_sleep()
    click(1055, 1162)  # 返回主页面
    rand_sleep()
    click(1353, 1174)  # 领地
    rand_sleep()
    for _ in range(3):
        pyautogui.scroll(-300)
        time.sleep(0.3)
    rand_sleep()
    click(1549, 790)  # 进入生产工厂
    rand_sleep()
    click(1340, 767)  # 点击生产
    rand_sleep()

    # 领取材料点击2次
    for i in range(2):
        click(get_x, get_y, f"领取材料 第{i+1}次")
        rand_sleep()
    # 开始生产点击1次
    click(prod_x, prod_y, "开始生产")
    rand_sleep()

    click(1506, 299)  # 关闭
    rand_sleep()
    # 返回主流程
    click(1210, 1167)
    print("点击战斗")
    rand_sleep()
    click(1508, 1020)
    print("点击活动")
    rand_sleep()
    click(1280, 448)
    print("点击深渊")
    rand_sleep()
    click(1103, 1065)
    print("点击仓库")
    rand_sleep()
    print(f"[{now_str()}] 工厂任务完成")

# ---------------- 主程序 ----------------
if __name__ == "__main__":
    # 输入工厂任务领取和生产材料选择
    print("====== 请选择领取材料 ======")
    print("1 - 图纸  2 - 钻石  3 - 宝石碎片  4 - 电池")
    get_choice = int(input("请输入领取材料选择(1-4)："))

    print("====== 请选择生产材料 ======")
    print("1 - 图纸  2 - 钻石  3 - 宝石碎片  4 - 电池")
    prod_choice = int(input("请输入生产材料选择(1-4)："))

    # 延迟时间
    h = int(input("请输入工厂任务延迟小时数："))
    m = int(input("请输入工厂任务延迟分钟数："))
    factory_delay_seconds = h * 3600 + m * 60

    print(f"[{now_str()}] 脚本启动...")

    factory_run_time = datetime.now() + timedelta(seconds=factory_delay_seconds)
    factory_done = False
    print(f"[{now_str()}] 工厂任务将在 {factory_run_time.strftime('%H:%M')} 执行")

    # 启动先执行一次主任务
    main_task_once()
    next_main_time = calc_next_main_time()
    print(f"[{now_str()}] 下一轮主任务预计执行时间：{next_main_time.strftime('%H:%M')}")

    while True:
        now = datetime.now()

        # 工厂任务到时间后：先工厂 -> 再主任务 -> 再每日任务 -> 后面继续主任务
        if (not factory_done) and now >= factory_run_time:
            print(f"[{now_str()}] ===== 执行工厂任务 =====")
            lingdi_production_task(get_choice, prod_choice)
            print(f"[{now_str()}] ===== 今天夜里工厂任务完成 =====")

            main_task_once()
            next_main_time = calc_next_main_time()

            daily_task_once(next_main_time)

            factory_done = True
            continue

        # 正常主任务
        if now >= next_main_time:
            main_task_once()
            next_main_time = calc_next_main_time()
            print(f"[{now_str()}] 下一轮主任务预计执行时间：{next_main_time.strftime('%H:%M')}")
            continue

        time.sleep(5)