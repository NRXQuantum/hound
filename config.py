import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hound.db")
    
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100/minute")
    
    PORT = int(os.getenv("PORT", 8000))
    MODE = os.getenv("MODE", "local")
    GPS_AUTO = os.getenv("GPS_AUTO", "false").lower() == "true"
    COOKIE_TRACK = os.getenv("COOKIE_TRACK", "true").lower() == "true"
    AUTO_COLLECT = os.getenv("AUTO_COLLECT", "true").lower() == "true"
    
    DATA_DIR = BASE_DIR / "data"
    LOG_DIR = BASE_DIR / "logs"
    STATIC_DIR = BASE_DIR / "static"
    
    MAX_LOG_SIZE = int(os.getenv("MAX_LOG_SIZE", 10 * 1024 * 1024))  # 10MB
    BACKUP_COUNT = int(os.getenv("BACKUP_COUNT", 5))

config = Config()
config.DATA_DIR.mkdir(parents=True, exist_ok=True)
config.LOG_DIR.mkdir(parents=True, exist_ok=True)
config.STATIC_DIR.mkdir(parents=True, exist_ok=True)