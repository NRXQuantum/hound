#  Hound v3.5 – Next-Gen Telemetry, OSINT & Device Intelligence Engine

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![ORM](https://img.shields.io/badge/Database-SQLAlchemy-red.svg)](https://www.sqlalchemy.org/)
[![Visualization](https://img.shields.io/badge/3D%20Engine-Three.js-black.svg)](https://threejs.org/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Original Concept & Base Repository:** [TechChip / Hound](https://github.com/techchipnet/hound)  
**Refactored, Enhanced & Maintained by:** NRXQuantum  

---

## ⚠️ Critical Disclaimer & Ethical Advice (نَصِيحَة / Moral Reminder)

> [!WARNING]
> **STRICTLY FOR EDUCATIONAL, RESEARCH, AND AUTHORIZED PENETRATION TESTING PURPOSES ONLY.**

```text
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                 ETHICAL NOTICE & NASIHAT                             ║
║                                                                                      ║
║  Knowledge is a trust (Amanah). Technical capability is not a license to violate     ║
║  privacy, deceive, or cause harm. Do not use this tool to stalk, spy on, or capture  ║
║  data from individuals without explicit, written, and informed consent.              ║
║                                                                                      ║
║  Every individual is solely accountable for their intentions and actions. Build,     ║
║  protect, and defend; do not dismantle trust or oppress others.                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

  - Zero Liability: The developer(s), contributors, and original creator assume
    no liability and are not responsible for any misuse, damage, data breach, or
    legal consequences caused by this software.
  - Compliance: It is the user's sole responsibility to adhere to all applicable
    local, national, and international cybersecurity, privacy, and wiretapping
    laws.
  - Authorized Auditing: Use this toolkit only in isolated lab environments or
    on systems where you possess documented authorization for security
    assessment.

📖 Overview

Hound v3.5 is an asynchronous telemetry gathering and browser intelligence
engine designed for digital forensics, OSINT research, and client-side security
audits.

This project is an advanced evolution of the original Hound toolkit by TechChip.
While the original concept introduced telemetry link interactions, Hound v3.5
has been completely re-engineered from the ground up with a modern FastAPI
asynchronous backend, SQLAlchemy ORM persistence, Three.js 60-FPS 3D orientation
visualizer, and a full-featured Leaflet / Google Maps Level-24 Deep Zoom admin
dashboard.

🔄 What’s New in Version 3.5? (Changelog vs Original)

| Feature / Component  | Hound (Original / Legacy)       | Hound v3.5 (Current)                                                                                 |
| :------------------- | :------------------------------ | :--------------------------------------------------------------------------------------------------- |
| **Backend Core**     | PHP 7.x Web Server              | **FastAPI (Asynchronous Python 3)** + Uvicorn                                                        |
| **Data Persistence** | Plain `.txt` files & JSON dumps | **SQLite via SQLAlchemy ORM** + Rotating Log Engine                                                  |
| **Admin Interface**  | None (Terminal logs only)       | **Full Web Dashboard** (`/admin`) with Real-time Cards                                               |
| **Mapping Engine**   | External Google Maps link       | **Interactive Leaflet Map** with **Google Maps Level 24 Zoom** (Streets, Hybrid, Satellite, Terrain) |
| **3D Orientation**   | Basic WebSocket viewer          | **60 FPS Three.js Visualizer** with LERP Smoothing & Compass HUD                                     |
| **Tunneling Engine** | Basic Cloudflared script        | **Automated Multi-Retry Tunneling** with drop recovery                                               |
| **Spoof Detection**  | None                            | **Lie Detection Engine** (UA vs GPU / Touch Points Mismatch)                                         |
| **Fingerprinting**   | Canvas & Audio                  | **WebGPU, V8 Heap, Display Gamut, Emoji Sub-pixel, Math Quirks**                                     |

✨ Key Capabilities & Telemetry Vectors

1. 🔍 Anti-Spoofing & Lie Detection Engine

  - Cross-examines navigator.userAgent with underlying hardware primitives.
  - Flags desktop spoofing on mobile devices (e.g., detecting Mali/Adreno GPUs
    running on supposed Windows/x86 user agents).
  - Validates touch points against reported platform architectures.

2. 🎮 Deep Hardware & Browser Intelligence

  - Graphics: WebGL unmasked renderer/vendor, WebGPU adapter detection, and
    Canvas SHA-256 fingerprinting.
  - Audio & Media: AudioContext frequency analyzer signature, H.264 4K/60FPS
    hardware decoding capabilities, connected cameras, microphones, and audio
    outputs.
  - System & Memory: V8 JavaScript heap limit inspection, CPU benchmarking
    score, battery level/charging cycle times, and installed system TTS voices.
  - Display & Math: Display color gamut (sRGB/P3), Dark mode preference, device
    pixel ratio, and JavaScript math engine floating-point quirks.

3. 🌐 Multi-Layer Geolocation & Network Reconnaissance

  - Exact GPS Telemetry: High-precision latitude, longitude, altitude, accuracy
    radius, and motion velocity.
  - Triangulated IP Geo: Multi-provider fallback (FreeIPAPI, IPAPI, IPWhois) for
    ISP, ASN, City, and Region discovery.
  - Network Leaks: WebRTC ICE candidate extraction for local LAN IP and STUN
    public IP leak discovery.

4. 🧭 Real-Time 60 FPS 3D Orientation & Compass

  - High-frequency (70ms) sensor telemetry pipeline.
  - Standalone WebSocket broadcast server (viewer_server.py).
  - 3D phone model rendered via Three.js with LERP (Linear Interpolation) and
    shortest-angular difference handling to prevent visual jitter.
  - Interactive 2D heading compass with 8-point cardinal direction readout.

5. 📊 Centralized Admin Dashboard

  - Visual target management accessible via http://localhost:<PORT>/admin.
  - Target profile cards grouped by unique persistent user session (hound_uid).
  - Multi-layer satellite mapping with deep zoom (Level 24) powered by Leaflet.

📁 Repository Structure

├── app/
│   ├── __init__.py           # Package initializer
│   ├── database.py           # SQLAlchemy database schema & engine setup
│   ├── main.py               # FastAPI application, CORS, routers & static mounts
│   ├── models.py             # Pydantic data validation schemas
│   ├── utils.py              # Log rotators, human-readable formatters & file managers
│   └── webhook.py            # Telemetry ingestion endpoint & sensor pipeline
├── data/                     # SQLite database (hound.db) & raw JSON storage
├── logs/                     # Rotating text logs & per-target session logs
├── static/
│   ├── admin.html            # Web dashboard with Leaflet & Google Maps
│   ├── index.html            # Deployed frontend capture template
│   ├── script.js             # UI helper script
│   └── telemetry.js          # Core browser intelligence & telemetry harvester
├── config.py                 # Application configuration & environment manager
├── hound.sh                  # Multi-argument master deployment script
├── requirements.txt          # Python dependencies
└── viewer_server.py          # Standalone 60 FPS 3D WebSocket orientation server

🛠️ Installation & Setup

1. Prerequisites

  - Python 3.9+
  - Pip (Python package manager)
  - Cloudflared (Optional: for public internet tunneling)

2. Clone & Install Dependencies

# Clone this repository
git clone https://github.com/your-username/hound.git
cd hound

# (Recommended) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required Python packages
pip install -r requirements.txt

3. Grant Permissions

chmod +x hound.sh viewer_server.py

🚀 Execution & Usage Guide

Method 1: Using the Master Bash Script (hound.sh)

The script orchestrates server startup, background worker management, and
Cloudflare tunnel initialization.

# Run locally on default port 8000
./hound.sh --local

# Launch with Cloudflare internet tunnel & custom port
./hound.sh --internet --port 8080

# Auto-collect all telemetry + prompt GPS coordinates
./hound.sh --internet --gps --auto

Supported CLI Flags:

| Flag                   | Description                                            |
| :--------------------- | :----------------------------------------------------- |
| `--internet`           | Spins up a public `trycloudflare.com` tunnel.          |
| `--local`              | Binds server to `localhost` (Default).                 |
| `--port <PORT>` / `-p` | Custom port configuration (Default: `8000`).           |
| `--gps`                | Enables automated high-accuracy GPS requesting.        |
| `--cookie`             | Enables persistent cookie-based user session tracking. |
| `--auto`               | Automatically triggers instant telemetry harvesting.   |
| `--viewer`             | Flag indicator for 3D viewer readiness.                |

Method 2: Manual Python Startup

If you prefer to start components individually:

1. Start the FastAPI Telemetry Server:

python3 -m app.main

  - Capture Page: http://localhost:8000
  - Admin Dashboard: http://localhost:8000/admin
  - Interactive API Docs: http://localhost:8000/docs

2. Start the 3D Sensor Visualizer:

python3 viewer_server.py

  - Visualizer UI: http://localhost:8082

📊 Monitoring Logs & Telemetry

Real-Time Terminal Monitoring:

# Stream all incoming target profiles
tail -f logs/data.txt

# Stream live device motion / gyroscope coordinates
tail -f logs/orientation.log

# View profile for a specific target ID
cat logs/targets/usr_<USER_ID>.txt

⚙️ Configuration (.env / config.py)

You can configure global options using environment variables or a .env file:

DEBUG=False
PORT=8000
MODE=local
DATABASE_URL=sqlite:///./hound.db
MAX_LOG_SIZE=10485760   # 10MB per log file before rotation
BACKUP_COUNT=5          # Keep up to 5 rotated backup logs
GPS_AUTO=true
COOKIE_TRACK=true
AUTO_COLLECT=true

🤝 Credits & Acknowledgements

  - TechChip (techchipnet): Creator of the original Hound tool which inspired
    this project architecture.
  - Three.js: Real-time 3D graphics rendering engine.
  - Leaflet: Open-source JavaScript library for interactive mobile-friendly
    maps.
  - FastAPI: High-performance asynchronous backend framework.

📄 License & Open Source Compliance

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) in
compliance with the original work by TechChip.

Hound v3.5 - Advanced Telemetry & OSINT Engine
Copyright (C) 2026 TechChip (Original Author) & NRXQuantum (v3.5 Maintainer)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

See the GNU General Public License v3.0 for full details.

