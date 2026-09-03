Here is a comprehensive, professional, and detailed README.md file in English, covering everything about the tool—from what it does to how to run it, file structures, and step-by-step usage.

---

```markdown
#  Hound v3.0 – Enhanced Information Gathering Toolkitচ

**Original Concept & Base Framework:** TechChip (github.com/techchipnet)  
**Enhanced & Maintained by:** NRXQuantum

---

## 📖 Introduction

Hound is a lightweight yet advanced information-gathering toolkit designed for authorized penetration testing and security research. It generates a single link that, when opened by a target, silently collects a wide array of device data, geolocation, browser fingerprints, and real-time sensor readings—all without requiring any installation on the target's device.

This version is a heavily enhanced fork of the original Hound tool, featuring advanced fingerprinting techniques, a real-time 3D orientation viewer, and significantly improved logging and stability.

---

## ✨ Key Features

| Category | Details |
| :--- | :--- |
| **Device Intelligence** | OS, browser, platform, screen resolution, memory, CPU cores, battery status, timezone |
| **Network & Location** | Public IP, city/region/country, ISP, coordinates (via ipinfo.io), local IP (WebRTC), public IP leak (STUN) |
| **GPS Tracking** | High-accuracy latitude/longitude, altitude, speed, heading – includes a direct Google Maps link |
| **Live Orientation** | Real-time alpha (compass), beta (tilt), and gamma (roll) data – updated continuously |
| **Advanced Fingerprinting** | Canvas SHA-256 hash, WebGL renderer/vendor info, AudioContext signature, installed fonts list, client rects |
| **Peripheral Detection** | Connected USB devices, media devices (camera/microphone/speakers), clipboard content |
| **Real-time 3D Viewer** | Python-based WebSocket server that visualizes orientation data on a 3D phone model with a live compass |
| **Comprehensive Logging** | All data is written to `data.txt` (human-readable), `orientation.log` (sensor stream), and `raw_data.json` (backup) |

---

## 🛠️ System Requirements

- **PHP** (>= 7.0) – required for the web server and webhook.
- **curl** – required for fetching IP location data.
- **cloudflared** (optional) – automatically installed via the script if you choose the tunnel option.
- **Python 3** (>= 3.6) – only required for the 3D orientation viewer (`viewer_server.py`).

> The main script (`hound.sh`) will check for these dependencies and attempt to install `cloudflared` automatically using `apt` or `wget`.

---

## 🚀 How to Run (Step-by-Step)

### 1. Preparation
Clone or download all the provided files into a single directory on your system.

```bash
git clone https://github.com/your-username/hound-v3.git
cd hound-v3
```

Make the main script executable (optional but recommended):

```bash
chmod +x hound.sh
```

2. Launch the Toolkit

Start the main script using the following command:

```bash
bash hound.sh
```

The script will perform the following actions automatically:

· Display the banner.
· Check if PHP and curl are installed.
· Check if cloudflared is installed; if not, it will try to install it.
· Ask you to choose between a Cloudflared tunnel (public link) or a local server (localhost).

3. Choose Your Server Mode

You will be prompted with:

```
Do you want to use Cloudflared tunnel?
Otherwise it will be run on localhost:8080 [Default is Y] [Y/N]:
```

· Type Y (or just press Enter) – This starts a PHP server on 127.0.0.1:3333 and creates a Cloudflared tunnel. A public link (e.g., https://random-name.trycloudflare.com) will be generated and displayed on the screen.
· Type N – This starts the PHP server on 127.0.0.1:8080. The link will only be accessible from your local machine (useful for testing).

4. Share the Link

Once the server is running, you will see a link in the terminal. Share this link with your target (via message, email, etc.). When the target opens the link in their browser:

· Their IP address is instantly logged (ip.txt).
· A chat-like page appears asking them to click a button to "Share Location & Device Info".
· The moment they open the page, all background data collection begins.

5. Monitor Incoming Data

The terminal will display real-time notifications:

```
[+] Target opened the link!
[+] Target IP: 192.168.1.100
[+] Location: City, Region, Country
[+] Collecting device and GPS data...
------------------------------------------------------------
```

You can also monitor the logs in real-time by opening a second terminal and running:

```bash
tail -f data.txt
```

Or for orientation-specific data:

```bash
tail -f orientation.log
```

---

📁 File Structure & Descriptions

To fully understand the toolkit, here is a breakdown of every file and its role:

File Purpose
hound.sh The main orchestrator script. It manages dependencies, starts the PHP server, sets up the Cloudflared tunnel, injects the payload into the HTML, and monitors for incoming connections.
index_chat.html The template for the chat interface. It contains the static HTML and CSS structure. The script injects the payload.txt into this file to create the final index.html.
index.html The final page served to the target. Generated dynamically by merging index_chat.html and payload.txt.
payload.txt The core JavaScript payload. It runs in the target's browser and performs all data collection (device info, GPS, orientation, fingerprints, network, USB, clipboard). It sends the data via POST requests to webhook.php.
webhook.php The central data collection endpoint. It receives JSON data from the payload, writes orientation data to live_orientation.json and orientation.log, and writes all other data to data.txt (without file locks, so tail -f works seamlessly).
ip.php A lightweight script that captures the target's IP address, user-agent, referrer, and request method, and logs them to ip.txt.
template.php A redirect template. The script replaces forwarding_link with the actual Cloudflared URL to redirect the target to the correct index.html.
index.php The final redirector. Generated dynamically from template.php by replacing the placeholder with the active tunnel link.
script.js The original chat UI JavaScript (used for basic message formatting).
style.css The chat UI styling.
viewer_server.py A standalone Python 3 server that provides a real-time 3D visualization of the orientation data. It reads live_orientation.json and broadcasts it via WebSockets to a Three.js frontend.

---

🧭 How It Works (Technical Flow)

1. Initialization (hound.sh)
   · Checks dependencies.
   · Injects payload.txt into index_chat.html → creates index.html.
   · Replaces forwarding_link in template.php → creates index.php.
   · Starts the PHP server (port 3333 or 8080).
   · (If Cloudflared selected) starts the tunnel and extracts the public URL.
2. Target Interaction
   · The target visits the generated link.
   · ip.php logs their IP and redirects them to index.html.
   · The page loads the chat UI and executes the JavaScript payload.
3. Data Collection (JavaScript)
   · The payload immediately sends device specs, IP info, network details, and starts orientation listeners.
   · It requests advanced fingerprints (Canvas, WebGL, Audio) after 1 second.
   · If the user clicks the "Share Location" button, the GPS coordinates are captured and sent.
   · All collected data is sent as JSON to /webhook.php.
4. Data Storage (webhook.php)
   · Orientation/motion data → orientation.log and live_orientation.json.
   · Everything else (device, GPS, fingerprints, etc.) → data.txt (unlocked for instant tail reading).
   · Raw JSON backup → raw_data.json.
5. Real-time Viewer (Optional)
   · Run python3 viewer_server.py.
   · The server reads live_orientation.json and broadcasts updates via WebSockets.
   · The browser client uses Three.js to rotate a 3D phone model and draw a compass based on the alpha/beta/gamma values.

---

🎥 Using the Python 3D Viewer

The 3D viewer provides a stunning visual representation of the target's device orientation in real-time.

To launch it:

1. Ensure the main Hound server (hound.sh) is already running and receiving data.
2. Open a new terminal window.
3. Run the following command:
   ```bash
   python3 viewer_server.py
   ```
4. Your default browser will automatically open http://localhost:8082.
5. The page will connect via WebSocket and display:
   · A rotating 3D phone model.
   · A live compass.
   · Numeric readouts for Alpha, Beta, Gamma, and Heading.

You can drag to rotate the view and scroll to zoom.

---

⚠️ Important Disclaimer

This tool is intended strictly for educational purposes, authorized penetration testing, and personal security research.

· Do not use this tool to spy on individuals, track people without their explicit consent, or violate any privacy laws.
· Do not use this tool on systems or devices you do not own or have explicit written permission to test.
· The author (NRXQuantum) and the original creator (TechChip) are not responsible for any misuse, damage, or legal repercussions caused by this software.

Users are solely responsible for ensuring compliance with all applicable local, state, and federal laws.

---

🤝 Credits & Acknowledgments

· TechChip (techchipnet) – For developing the original Hound framework that laid the foundation for this tool.
· Open-source community – For providing the libraries and tools (PHP, Three.js, Cloudflared) that make this project possible.

---

📌 Final Notes

· All logs are stored locally in the same directory. No data is sent to any external server other than the ipinfo.io API (for IP geolocation) and the Cloudflared tunnel (for link generation).
· The script automatically handles cloudflared installation on most Debian-based systems. If you face issues, ensure you have an active internet connection.
· For the best experience, run both the main script and the Python viewer side-by-side in separate terminal windows.

Happy Testing! 

```

---

This README covers **everything**—from the tool's purpose, features, setup, usage, file breakdown, technical flow, and the optional 3D viewer. Let me know if you need any modifications.
