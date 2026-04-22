import json
import os
import requests
from datetime import datetime, timedelta, timezone

# 1. 动态获取时间 (泰国 UTC+7)
tz = timezone(timedelta(hours=7)) 
now = datetime.now(tz)
today_key = now.strftime("%Y-%m-%d")
now_time = now.strftime("%H:%M:%S")

def get_live_rates():
    # 定义多个备用接口，提高在 GitHub Actions 环境下的稳定性
    urls = [
        "https://er-api.com",
        "https://exchangerate-api.com"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in urls:
        try:
            print(f"正在尝试从接口抓取: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            rates = data.get("rates", {})
            
            if rates:
                print(f"✅ 抓取成功！数据源: {url}")
                return {
                    "update_time": now_time,
                    "USD_THB": round(rates.get("THB", 32.25), 2),
                    "USD_CNY": round(rates.get("CNY", 6.84), 2),
                    "USD_PHP": round(rates.get("PHP", 60.12), 2)
                }
        except Exception as e:
            print(f"⚠️ 接口失败 {url}: {e}")
            continue 
            
    return None

# 执行抓取
today_rates = get_live_rates()

if today_rates:
    # 3. 处理历史数据文件
    history_file = 'history.json'
    history_data = {}

    if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
        with open(history_file, 'r', encoding='utf-8') as f:
            try:
                history_data = json.load(f)
            except Exception as e:
                history_data = {}

    # 存入当天数据
    history_data[today_key] = today_rates

    # 4. 保存为 history.json
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=4, ensure_ascii=False)

    # 5. 保存为 rates.json
    with open('rates.json', 'w', encoding='utf-8') as f:
        json.dump({"date": today_key, **today_rates}, f, indent=4, ensure_ascii=False)

    print(f"🚀 动态数据更新成功: {today_key} {now_time}")
else:
    # 抛出错误让 GitHub Action 变红，从而触发邮件报警
    print("❌ 所有接口均抓取失败，终止更新。")
    exit(1)

