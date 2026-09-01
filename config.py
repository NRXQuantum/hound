"""
Hound v3.0 - Configuration Module
Handles all environment variables and application settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv('DATA_DIR', './data'))
LOG_DIR = Path(os.getenv('LOG_DIR', './logs'))

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


class Settings:
    """Application Settings"""
    
    # Database
    DATABASE_URL: str = os.getenv(
        'DATABASE_URL', 
        'sqlite:///./hound.db'
    )
    
    # API Configuration
    API_KEY: str = os.getenv('API_KEY', 'default-api-key')
    WEBHOOK_SECRET: str = os.getenv('WEBHOOK_SECRET', 'default-webhook-secret')
    
    # Server
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 8000))
    VIEWER_PORT: int = int(os.getenv('VIEWER_PORT', 8082))
    
    # File Paths
    ORIENTATION_LOG: str = str(LOG_DIR / 'orientation.log')
    DATA_LOG: str = str(DATA_DIR / 'data.txt')
    IP_LOG: str = str(LOG_DIR / 'ip.txt')
    VISITORS_LOG: str = str(LOG_DIR / 'visitors.log')
    ORIENTATION_JSON: str = str(DATA_DIR / 'live_orientation.json')
    RAW_DATA_JSON: str = str(DATA_DIR / 'raw_data.json')
    
    # Logging Configuration
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


# Create settings instance
settings = Settings()
