import json
import os
from datetime import datetime, timedelta, timezone

# 1. 动态获取当天的日期和具体时间（泰国 UTC+7）
tz = timezone(timedelta(hours=7)) 
now = datetime.now(tz)

today_key = now.strftime("%Y-%m-%d")
now_time = now.strftime("%H:%M:%S")

# --- 下面部分保持不变 ---
today_rates = {
    "update_time": now_time,
    "USD_THB": 32.25,
    "USD_CNY": 6.84,
    "USD_PHP": 60.12
}

history_file = 'history.json'
history_data = {}

if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
    with open(history_file, 'r', encoding='utf-8') as f:
        try:
            history_data = json.load(f)
        except:
            history_data = {}

history_data[today_key] = today_rates

with open(history_file, 'w', encoding='utf-8') as f:
    json.dump(history_data, f, indent=4, ensure_ascii=False)

with open('rates.json', 'w', encoding='utf-8') as f:
    json.dump({"date": today_key, **today_rates}, f, indent=4, ensure_ascii=False)

print(f"✅ 更新成功 (泰国时间: {now_time})")

