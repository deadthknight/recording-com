#!usr/bin/env python3.11    # Python解释器
# -*- coding: utf-8 -*-
import time
import os
import platform
from obswebsocket import obsws, requests as obs_requests
import requests as http_requests
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import wait_until
from loguru import logger

logger.add("record_log_{time}.log", format="{time} {level} {message}", level="INFO", rotation="1 week")

def create_browser():
    co = ChromiumOptions()
    co.headless(False)
    co.set_argument('--start-maximized')
    co.set_argument('--autoplay-policy=no-user-gesture-required')
    return ChromiumPage(co)

def check_bilibili_live(room_id):
    try:
        url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://live.bilibili.com/{room_id}"
        }
        response = http_requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        live_status = data.get("data", {}).get("live_status", 0)
        return live_status == 1
    except Exception as e:
        logger.error(f"[B站API错误] {e}")
        return False

def stop_obs_process():
    try:
        system = platform.system()
        logger.info("📴 正在关闭 OBS 软件...")
        if system == "Windows":
            os.system("taskkill /f /im obs64.exe")
        elif system == "Darwin":  # macOS
            os.system("pkill -f OBS")
        elif system == "Linux":
            os.system("pkill obs")
        logger.info("✅ OBS 已关闭")
    except Exception as e:
        logger.error(f"[关闭 OBS 失败] {e}")

def wait_until_live(room_id):
    logger.info("⏳ 开始轮询检查直播状态（每10分钟检查一次）")
    while True:
        if check_bilibili_live(room_id):
            logger.info("✅ 直播已开始！准备启动录制流程")
            return
        logger.info("🔁 直播未开始，10分钟后再次检查...")
        time.sleep(600)

def auto_record(max_minutes, room_id):
    ws = None
    page = None
    try:
        page = create_browser()
        logger.info("🧭 正在打开直播页面...")
        page.get(f"https://live.bilibili.com/{room_id}?")
        time.sleep(5)  # 等待页面加载

        # 连接 OBS
        ws = obsws("localhost", 4455, password="111111")
        try:
            ws.connect()
        except Exception as e:
            logger.error(f"[OBS连接失败] {e}，请确认 OBS 已启动并开启 obs-websocket 插件")
            return False

        # 启动录制
        ws.call(obs_requests.StartRecord())
        start_time = time.time()
        logger.info(f"⏺ {time.strftime('%H:%M:%S')} 录制已启动")

        max_duration = max_minutes * 60
        failed_checks = 0
        last_check = 0

        while True:
            now = time.time()
            elapsed = now - start_time
            remaining = max(0, int(max_duration - elapsed))
            mins, secs = divmod(remaining, 60)
            print(f"\r剩余时间: {mins:02d}:{secs:02d} | 状态: 直播中", end="")

            if now - last_check >= 60:
                last_check = now
                if not check_bilibili_live(room_id):
                    failed_checks += 1
                    logger.warning(f"\n⚠️ 直播检测失败次数: {failed_checks}/3")
                    if failed_checks >= 3:
                        logger.warning("❌ 直播已结束，停止录制")
                        break
                else:
                    failed_checks = 0

            if elapsed >= max_duration:
                logger.info("⌛ 达到最大录制时长，准备停止录制")
                break

            time.sleep(1)

        # 停止录制
        ws.call(obs_requests.StopRecord())
        logger.info(f"⏹ {time.strftime('%H:%M:%S')} 录制已停止")

        # 关闭 OBS 软件
        stop_obs_process()

        return True

    except Exception as e:
        logger.error(f"[脚本错误] {e}")
        return False
    finally:
        if ws:
            ws.disconnect()
        if page:
            page.close()

if __name__ == "__main__":
    room_id = 1616  # 替换为你想录制的房间号
    max_minutes = 500 #录制时间（分钟）

    wait_until_live(room_id)
    success = auto_record(max_minutes, room_id)

    if success:
        logger.info("🎉 录制流程已完成")

