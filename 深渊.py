import pyautogui
import time
import random
from datetime import datetime, timedelta

# ================== 模式开关 ==================
TEST_MODE = True  # True=测试模式（暂不限制0点后） False=正式模式

# ---------------- 初始化 ----------------
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 深渊点击坐标（固定）
CLICK_X = 1469
CLICK_Y = 1131

# ---------------- 各系统材料配置 ----------------
# name: 材料名称
# x, y: 点击坐标
# get_scroll: 领取前向下滚动次数
# prod_scroll: 生产前向下滚动次数

FACTORY_MATERIALS = {
    1: {"name": "图纸", "x": 1478, "y": 672, "get_scroll": 0, "prod_scroll": 0},
    2: {"name": "青铜宝箱", "x": 1478, "y": 772, "get_scroll": 0, "prod_scroll": 0},
    3: {"name": "钻石", "x": 1478, "y": 872, "get_scroll": 0, "prod_scroll": 0},
    4: {"name": "宝石碎片", "x": 1478, "y": 972, "get_scroll": 0, "prod_scroll": 0},
    5: {"name": "电池", "x": 1478, "y": 1072, "get_scroll": 0, "prod_scroll": 0},
    6: {"name": "结晶", "x": 1478, "y": 1010, "get_scroll": 3, "prod_scroll": 3},
    7: {"name": "远古能源", "x": 1478, "y": 1110, "get_scroll": 3, "prod_scroll": 3},
}

WISH_MATERIALS = {
    1: {"name": "升级药水", "x": 1478, "y": 672, "get_scroll": 0, "prod_scroll": 0},
    2: {"name": "命运金币", "x": 1478, "y": 772, "get_scroll": 0, "prod_scroll": 0},
    3: {"name": "角色觉醒材料", "x": 1478, "y": 872, "get_scroll": 0, "prod_scroll": 0},
    4: {"name": "SSR", "x": 1478, "y": 972, "get_scroll": 0, "prod_scroll": 0},
    5: {"name": "远古能源", "x": 1478, "y": 1072, "get_scroll": 0, "prod_scroll": 0},
    6: {"name": "绝招材料", "x": 1472, "y": 900, "get_scroll": 3, "prod_scroll": 2},
    7: {"name": "灵魂结晶", "x": 1472, "y": 1000, "get_scroll": 3, "prod_scroll": 2},
    8: {"name": "全能皇冠", "x": 1472, "y": 1100, "get_scroll": 3, "prod_scroll": 2},
}

PET_MATERIALS = {
    1: {"name": "宠物升星粉尘", "x": 1478, "y": 672, "get_scroll": 0, "prod_scroll": 0},
    2: {"name": "宠物饼干", "x": 1478, "y": 772, "get_scroll": 0, "prod_scroll": 0},
    3: {"name": "水晶小鱼干", "x": 1478, "y": 872, "get_scroll": 0, "prod_scroll": 0},
    4: {"name": "精英宠物碎片", "x": 1478, "y": 972, "get_scroll": 0, "prod_scroll": 0},
    5: {"name": "精英宠物秘宝箱", "x": 1478, "y": 1072, "get_scroll": 0, "prod_scroll": 0},
    6: {"name": "极品宠物碎片", "x": 1472, "y": 800, "get_scroll": 2, "prod_scroll": 2},
    7: {"name": "极品宠物秘宝箱", "x": 1472, "y": 900, "get_scroll": 2, "prod_scroll": 2},
    8: {"name": "远古能源", "x": 1472, "y": 1000, "get_scroll": 2, "prod_scroll": 2},
    9: {"name": "磁带", "x": 1472, "y": 1100, "get_scroll": 2, "prod_scroll": 2},
}
ABYSS_OUTPOST_MATERIALS = {
    1: {"name": "洗炼药水", "x": 1476, "y": 700, "get_scroll": 2, "prod_scroll": 2},
    2: {"name": "灯笼", "x": 1476, "y": 800, "get_scroll": 2, "prod_scroll": 2},
    3: {"name": "远古能源", "x": 1476, "y": 900, "get_scroll": 2, "prod_scroll": 2},
    4: {"name": "散落的祷文", "x": 1476, "y": 1000, "get_scroll": 2, "prod_scroll": 2},
    5: {"name": "透明结晶", "x": 1476, "y": 1100, "get_scroll": 2, "prod_scroll": 2},
}
# ---------------- 全局变量 ----------------
last_daily_run_date = None
main_run_count = 0
territory_initialized = False

# ---------------- 工具函数 ----------------
def now_str():
    return datetime.now().strftime('%H:%M')

def now_full_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def click(x, y, desc="", delta=2):
    rx = x + random.randint(-delta, delta)
    ry = y + random.randint(-delta, delta)
    pyautogui.click(rx, ry)
    if desc:
        print(f"[{now_str()}] 点击：{desc}")

def rand_sleep(a=2, b=3):
    time.sleep(random.uniform(a, b))

def calc_next_main_time():
    interval = random.uniform(7200, 7500)  # 2小时 ~ 2小时5分钟
    return datetime.now() + timedelta(seconds=interval)

def print_next_main_time(next_main_time, task_configs=None):
    print(f"[{now_str()}] 下一轮主任务预计执行时间：{next_main_time.strftime('%H:%M')}")

    if not task_configs:
        return

    pending_tasks = [task for task in task_configs if task["enabled"] and not task["done"]]
    if pending_tasks:
        print(f"[{now_str()}] 当前未执行的领地任务：")
        for task in pending_tasks:
            print(f"[{now_str()}] - {task['name']}：{task['run_time'].strftime('%H:%M')}")

def back_to_main_flow():
    click(1210, 1167, "点击战斗")
    rand_sleep()
    click(1508, 1020, "点击活动")
    rand_sleep()
    click(1280, 448, "点击深渊")
    rand_sleep()
    click(1103, 1065, "点击仓库")
    rand_sleep()

def is_after_midnight():
    return datetime.now().hour >= 0

def all_night_tasks_done(task_list):
    return all(task["done"] for task in task_list)

def scroll_down(times, desc=""):
    if times <= 0:
        return
    if desc:
        print(f"[{now_str()}] {desc}")
    for i in range(times):
        pyautogui.scroll(-300)
        print(f"[{now_str()}] 向下滚动第{i+1}次")
        time.sleep(0.3)
    rand_sleep()

def scroll_up(times, desc=""):
    if times <= 0:
        return
    if desc:
        print(f"[{now_str()}] {desc}")
    for i in range(times):
        pyautogui.scroll(300)
        print(f"[{now_str()}] 向上滚动第{i+1}次")
        time.sleep(0.3)
    rand_sleep()

# ---------------- 输入函数 ----------------
def input_int(prompt, valid_choices=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if valid_choices is not None and value not in valid_choices:
                print("输入无效，请重新输入。")
                continue
            return value
        except ValueError:
            print("输入无效，请输入数字。")

def input_material_choice(task_name, materials, action_text):
    print(f"====== 请选择{task_name}{action_text} ======")
    for k, v in materials.items():
        print(f"{k} - {v['name']}")
    valid_choices = set(materials.keys())
    return input_int(
        f"请输入选择({min(valid_choices)}-{max(valid_choices)})：",
        valid_choices
    )

def input_task_delay(task_name):
    h = input_int(f"请输入{task_name}延迟小时数：")
    m = input_int(f"请输入{task_name}延迟分钟数：")
    return h * 3600 + m * 60

# ---------------- 主任务 ----------------
def main_task_once():
    global main_run_count

    before = pyautogui.pixel(CLICK_X, CLICK_Y)
    click(CLICK_X, CLICK_Y, "深渊点击领取")
    time.sleep(3)
    after = pyautogui.pixel(CLICK_X, CLICK_Y)

    if before != after:
        click(CLICK_X, CLICK_Y, "确认")
        print(f"[{now_str()}] 领取材料")
    else:
        print(f"[{now_str()}] 像素未变化，不再点击")

    main_run_count += 1
    print(f"[{now_str()}] 深渊材料已领取完成 | 已领取次数：{main_run_count}")

# ---------------- 初始化领地 ----------------
def init_territory():
    global territory_initialized

    # ✅ 已执行过，直接跳过（关键）
    if territory_initialized:
        return

    print(f"[{now_str()}] 开始执行初始化领地")

    click(1500, 280, "关闭深渊")
    rand_sleep()
    click(1055, 1162, "深渊返回")
    rand_sleep()
    click(1055, 1162, "返回主页面")
    rand_sleep()
    click(1353, 1174, "进入领地")
    rand_sleep()

    for i in range(3):
        pyautogui.scroll(-300)
        print(f"[{now_str()}] 领地下滑第{i+1}次")
        time.sleep(0.3)

    rand_sleep()
    click(1549, 790, "点击初始位置")
    rand_sleep()

    back_to_main_flow()

    print(f"[{now_str()}] 初始化领地执行完毕")

    # ✅ 标记为已执行（关键）
    territory_initialized = True

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
    print(f"[{now_full_str()}] 开始每日任务前置动作")

    click(1500, 280, "关闭深渊")
    rand_sleep()
    click(1055, 1162, "深渊返回")
    rand_sleep()
    click(1055, 1162, "返回主页面")
    rand_sleep()
    click(1071, 1170, "商店")
    rand_sleep()
    click(1215, 1089, "资源商店")
    rand_sleep()
    for i in range(5):
        before = pyautogui.pixel(GEM_X, GEM_Y)

        click(GEM_X, GEM_Y, f"宝石碎片第{i + 1}次（检测+点击）")
        time.sleep(2)

        after = pyautogui.pixel(GEM_X, GEM_Y)

        # ✅ 每一轮都判断
        if before == after:
            print(f"[{now_str()}] 宝石碎片已无法继续领取，结束循环（第{i + 1}次）")
            break

        # ✅ 正常领取流程
        time.sleep(31)  # 补齐到33秒

        click(AD_CLOSE_X, AD_CLOSE_Y, "关闭广告")

        print(f"[{now_str()}] 执行第{i + 1}次宝石碎片领取")

        if i < 4:
            print(f"[{now_str()}] 等待10分钟后继续下一次...")
            time.sleep(610)

    last_daily_run_date = datetime.now().date()

    print("宝石碎片程序全部执行完毕（或跳过循环）")
    rand_sleep()
    click(1263, 1165, "点击战斗")
    rand_sleep()
    click(1508, 1020, "点击活动")
    rand_sleep()
    click(1280, 448, "点击深渊")
    rand_sleep()
    click(1103, 1065, "点击仓库")
    rand_sleep()

    print(f"[{now_str()}] 每日任务完成")
    if next_main_time is not None:
        print(f"[{now_full_str()}] 每日任务执行完毕，下一轮主任务时间：{next_main_time.strftime('%H:%M')}")
    else:
        print(f"[{now_full_str()}] 每日任务执行完毕")
    print("=" * 50)

# ---------------- 通用领地任务 ----------------
def run_lingdi_task(task_name, enter_x, enter_y, produce_btn_x, produce_btn_y,
                    get_choice, prod_choice, materials, after_close_hook=None):

    get_item = materials[get_choice]
    prod_item = materials[prod_choice]

    print(
        f"[{now_str()}] 开始{task_name}任务，"
        f"领取材料：{get_item['name']}，"
        f"生产材料：{prod_item['name']}"
    )

    click(1500, 280, "关闭深渊")
    rand_sleep()
    click(1055, 1162, "深渊返回")
    rand_sleep()
    click(1055, 1162, "返回主页面")
    rand_sleep()
    click(1353, 1174, "领地")
    rand_sleep()

    click(enter_x, enter_y, f"进入{task_name}")
    rand_sleep()

    click(produce_btn_x, produce_btn_y, f"点击{task_name}生产")
    rand_sleep()

    # 领取前滚动
    if get_item["get_scroll"] > 0:
        scroll_down(get_item["get_scroll"], f"{task_name}领取材料前调整位置")

    for i in range(2):
        click(get_item["x"], get_item["y"], f"领取材料 第{i+1}次")
        rand_sleep()

    time.sleep(3)

    if get_item["get_scroll"] > 0 and prod_item["prod_scroll"] == 0:
        scroll_up(get_item["get_scroll"], f"{task_name}领取完成后恢复到基础材料位置")

    elif prod_item["prod_scroll"] > get_item["get_scroll"]:
        scroll_down(
            prod_item["prod_scroll"] - get_item["get_scroll"],
            f"{task_name}生产材料前继续向下调整位置"
        )

    elif 0 < prod_item["prod_scroll"] < get_item["get_scroll"]:
        scroll_up(
            get_item["get_scroll"] - prod_item["prod_scroll"],
            f"{task_name}生产材料前回调位置"
        )

    # ====== 开始生产 ======
    click(prod_item["x"], prod_item["y"], "开始生产")
    rand_sleep()

    # ====== 关键修改点 ======
    click(1506, 299, "关闭")
    rand_sleep()

    # ⭐ 插入自定义逻辑（只对深渊前哨生效）
    if after_close_hook:
        after_close_hook()

    # ====== 回主流程 ======
    back_to_main_flow()

    print(f"[{now_str()}] {task_name}任务完成")

def factory_task(get_choice, prod_choice):
    run_lingdi_task(
        task_name="工厂",
        enter_x=1290,
        enter_y=672,
        produce_btn_x=1340,
        produce_btn_y=767,
        get_choice=get_choice,
        prod_choice=prod_choice,
        materials=FACTORY_MATERIALS
    )

def wish_pool_task(get_choice, prod_choice):
    run_lingdi_task(
        task_name="祈愿池",
        enter_x=1446,
        enter_y=604,
        produce_btn_x=1484,
        produce_btn_y=699,
        get_choice=get_choice,
        prod_choice=prod_choice,
        materials=WISH_MATERIALS
    )

def pet_training_task(get_choice, prod_choice):
    run_lingdi_task(
        task_name="宠物训练营",
        enter_x=1126,
        enter_y=755,
        produce_btn_x=1166,
        produce_btn_y=847,
        get_choice=get_choice,
        prod_choice=prod_choice,
        materials=PET_MATERIALS
    )

def abyss_outpost_task(get_choice, prod_choice):
    run_lingdi_task(
        task_name="深渊前哨",
        enter_x=1011,
        enter_y=844,
        produce_btn_x=1331,
        produce_btn_y=776,
        get_choice=get_choice,
        prod_choice=prod_choice,
        materials=ABYSS_OUTPOST_MATERIALS,
        after_close_hook=lambda: (
            click(1551, 548, "恢复领地初始位置"),
            rand_sleep()
        )
    )

# ---------------- 任务配置 ----------------
def build_task_config(task_name, task_func, materials):
    get_choice = input_material_choice(task_name, materials, "领取材料")
    prod_choice = input_material_choice(task_name, materials, "生产材料")
    delay_seconds = input_task_delay(task_name)
    run_time = datetime.now() + timedelta(seconds=delay_seconds)

    return {
        "name": task_name,
        "enabled": True,
        "done": False,
        "func": task_func,
        "get_choice": get_choice,
        "prod_choice": prod_choice,
        "run_time": run_time,
        "materials": materials
    }

def configure_tasks():
    print("请输入今晚要执行的领地任务编号，多个用空格分隔，不执行输入0：")
    print("1 - 工厂")
    print("2 - 祈愿池")
    print("3 - 宠物训练营")
    print("4 - 深渊前哨")

    while True:
        raw = input("请输入选择：").strip()
        if raw == "0":
            return []

        try:
            selected = list(dict.fromkeys(int(x) for x in raw.split()))
        except ValueError:
            print("输入无效，请重新输入。")
            continue

        if not all(x in {1, 2, 3, 4} for x in selected):
            print("输入无效，请重新输入。")
            continue

        task_list = []

        for x in selected:
            if x == 1:
                task_list.append(build_task_config("工厂", factory_task, FACTORY_MATERIALS))
            elif x == 2:
                task_list.append(build_task_config("祈愿池", wish_pool_task, WISH_MATERIALS))
            elif x == 3:
                task_list.append(build_task_config("宠物训练营", pet_training_task, PET_MATERIALS))
            elif x == 4:
                task_list.append(build_task_config("深渊前哨", abyss_outpost_task, ABYSS_OUTPOST_MATERIALS))
        return task_list

# ---------------- 主程序 ----------------
# ---------------- 主程序 ----------------
if __name__ == "__main__":
    print(f"[{now_str()}] 开始配置今晚任务...")
    task_configs = configure_tasks()

    print(f"[{now_str()}] 脚本启动...")

    if not task_configs:
        print(f"[{now_str()}] 今晚未启用领地任务，主任务后将立即执行每日任务")
    else:
        for task in task_configs:
            print(f"[{now_str()}] {task['name']}任务将在 {task['run_time'].strftime('%H:%M')} 执行")
        print(f"[{now_str()}] 每日任务优先级最低，将在所有领地任务完成后的主任务执行后触发")

    # 启动先执行一次主任务
    main_task_once()
    next_main_time = calc_next_main_time()
    print_next_main_time(next_main_time, task_configs)

    # ⭐ 新增：无领地任务 → 立即执行每日任务
    if not task_configs:
        if last_daily_run_date != datetime.now().date():
            print(f"[{now_str()}] 无领地任务，主任务完成后立即执行每日任务")
            daily_task_once(next_main_time)

    # 启动后执行初始化领地（只有有领地任务才执行）
    if task_configs:
        print(f"[{now_str()}] 现在开始初始化领地")
        print_next_main_time(next_main_time, task_configs)
        init_territory()
        print(f"[{now_str()}] 初始化领地完成")
        print_next_main_time(next_main_time, task_configs)
    else:
        print(f"[{now_str()}] 未配置领地任务，跳过初始化领地")

    while True:
        now = datetime.now()
        task_executed = False

        # 到时间的夜间任务优先执行
        for task in task_configs:
            if (not task["done"]) and now >= task["run_time"]:
                print(f"[{now_str()}] ===== 执行{task['name']}任务 =====")
                task["func"](task["get_choice"], task["prod_choice"])
                print(f"[{now_str()}] ===== {task['name']}任务完成 =====")

                # 夜间任务完成后，立即补一次主任务
                main_task_once()
                next_main_time = calc_next_main_time()
                task["done"] = True
                print_next_main_time(next_main_time, task_configs)

                # ⭐ 所有领地任务完成 → 立即执行每日任务
                if all_night_tasks_done(task_configs):
                    if last_daily_run_date != datetime.now().date():
                        print(f"[{now_str()}] 所有领地任务已完成，立即执行每日任务")
                        daily_task_once(next_main_time)

                task_executed = True
                break

        if task_executed:
            continue

        # 正常主任务
        if now >= next_main_time:
            main_task_once()
            next_main_time = calc_next_main_time()
            print_next_main_time(next_main_time, task_configs)

            # ⭐统一每日任务触发逻辑（推荐）
            if last_daily_run_date != datetime.now().date():

                # 有领地任务 → 必须全部完成
                if task_configs:
                    if not all_night_tasks_done(task_configs):
                        continue

                # 无领地任务 或 已全部完成 → 执行每日任务
                print(f"[{now_str()}] 主任务后触发每日任务")
                daily_task_once(next_main_time)

            continue

        time.sleep(5)