from sqlalchemy import create_engine, Column, String, DateTime, JSON, Index
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from config import config

engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class CollectedData(Base):
    __tablename__ = "collected_data"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    device_info = Column(JSON, nullable=True)
    gps_data = Column(JSON, nullable=True)
    ip_info = Column(JSON, nullable=True)
    orientation = Column(JSON, nullable=True)
    canvas_fingerprint = Column(String, nullable=True)

    __table_args__ = (
        Index('idx_user_timestamp', 'user_id', 'timestamp'),
    )

def init_db():
    Base.metadata.create_all(bind=engine)