#!/usr/bin/env python3
"""
🐕 Hound v3.5 - 60 FPS Ultra-Smooth 3D Sensor Orientation & Compass Viewer Server
Run: python3 viewer_server.py
"""

import asyncio
import json
import os
from pathlib import Path
from aiohttp import web, WSMsgType

BASE_DIR = Path(__file__).resolve().parent
LIVE_FILE = BASE_DIR / "data" / "live_orientation.json"
FALLBACK_FILE = BASE_DIR / "live_orientation.json"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hound 3D Live Orientation Visualizer (60 FPS)</title>
    
    <!-- Three.js & OrbitControls CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }
        body { background: #0d1117; overflow: hidden; color: #fff; width: 100vw; height: 100vh; }
        
        #hud {
            position: absolute; top: 20px; left: 20px;
            background: rgba(17, 24, 39, 0.85); padding: 18px 22px;
            border-radius: 12px; z-index: 100; font-size: 13.5px;
            border-left: 4px solid #10b981; border: 1px solid #374151;
            min-width: 220px; backdrop-filter: blur(8px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        }
        #hud h2 { font-size: 16px; color: #10b981; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
        #hud .metric { padding: 3px 0; color: #9ca3af; }
        #hud .metric span { color: #38bdf8; font-weight: bold; }
        #hud .heading-row { margin-top: 8px; padding-top: 8px; border-top: 1px solid #374151; }
        #hud .heading-text { color: #f59e0b; font-size: 15px; font-weight: bold; }

        #compass-box {
            position: absolute; top: 20px; right: 20px;
            background: rgba(17, 24, 39, 0.85); border-radius: 50%; padding: 10px;
            z-index: 100; border: 2px solid #374151;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6); backdrop-filter: blur(8px);
        }
        #compassCanvas { display: block; width: 90px; height: 90px; }

        #status {
            position: absolute; bottom: 25px; left: 50%;
            transform: translateX(-50%);
            background: rgba(17, 24, 39, 0.85); padding: 8px 20px;
            border-radius: 20px; font-size: 13px; z-index: 100;
            border: 1px solid #374151; backdrop-filter: blur(8px);
        }
        .connected { color: #10b981; font-weight: bold; }
        .disconnected { color: #ef4444; font-weight: bold; }

        #controls-hint {
            position: absolute; bottom: 25px; right: 25px;
            color: #6b7280; font-size: 12px;
            background: rgba(17, 24, 39, 0.6); padding: 6px 14px;
            border-radius: 12px; border: 1px solid #1f2937;
        }
    </style>
</head>
<body>

    <div id="hud">
        <h2>📱 Live Sensor Telemetry</h2>
        <div class="metric">Alpha (Z): <span id="valAlpha">0.0</span>°</div>
        <div class="metric">Beta (X):  <span id="valBeta">0.0</span>°</div>
        <div class="metric">Gamma (Y): <span id="valGamma">0.0</span>°</div>
        <div class="heading-row">
            🧭 Compass: <span class="heading-text" id="valHeading">0.0°</span> 
            <span class="heading-text" id="valDirection" style="color:#10b981;">N</span>
        </div>
    </div>

    <div id="compass-box">
        <canvas id="compassCanvas" width="180" height="180"></canvas>
    </div>

    <div id="status">🔄 Connecting to Sensor Stream...</div>
    <div id="controls-hint">🖱️ Drag to rotate | Scroll to zoom</div>

    <script>
        // ----------------- THREE.JS SCENE SETUP -----------------
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0b0e14);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(2.5, 2.5, 4);
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.shadowMap.enabled = true;
        document.body.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
        dirLight.position.set(5, 10, 7);
        scene.add(dirLight);

        const blueFill = new THREE.DirectionalLight(0x38bdf8, 0.6);
        blueFill.position.set(-5, -2, -5);
        scene.add(blueFill);

        // Ground Grid
        const grid = new THREE.GridHelper(5, 12, 0x10b981, 0x1f2937);
        grid.position.y = -0.8;
        scene.add(grid);

        // ----------------- 3D PHONE MODEL (HIERARCHY) -----------------
        const headingGroup = new THREE.Group();
        scene.add(headingGroup);

        const tiltGroup = new THREE.Group();
        headingGroup.add(tiltGroup);

        const rollGroup = new THREE.Group();
        tiltGroup.add(rollGroup);

        const phoneGroup = new THREE.Group();
        phoneGroup.rotation.x = -Math.PI / 2;
        rollGroup.add(phoneGroup);

        // Phone Body
        const bodyMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.2, metalness: 0.8 });
        const body = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.7, 0.08), bodyMat);
        phoneGroup.add(body);

        // Phone Screen
        const screenMat = new THREE.MeshStandardMaterial({
            color: 0x0284c7,
            emissive: 0x0369a1,
            emissiveIntensity: 0.6,
            roughness: 0.1
        });
        const screen = new THREE.Mesh(new THREE.BoxGeometry(0.82, 1.55, 0.02), screenMat);
        screen.position.z = 0.045;
        phoneGroup.add(screen);

        // Camera Notch
        const camMat = new THREE.MeshStandardMaterial({ color: 0x000000 });
        const cam = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.02, 16), camMat);
        cam.rotation.x = Math.PI / 2;
        cam.position.set(0, 0.7, 0.05);
        phoneGroup.add(cam);

        // Direction Arrow
        const arrowMat = new THREE.MeshStandardMaterial({ color: 0x10b981, emissive: 0x059669 });
        const arrowShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.6), arrowMat);
        arrowShaft.position.set(0, 0.3, 0.06);
        phoneGroup.add(arrowShaft);

        const arrowHead = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.15, 16), arrowMat);
        arrowHead.position.set(0, 0.65, 0.06);
        phoneGroup.add(arrowHead);

        // ----------------- 2D COMPASS DRAWING -----------------
        const compassCanvas = document.getElementById('compassCanvas');
        const ctx = compassCanvas.getContext('2d');

        function drawCompass(headingDeg) {
            const w = compassCanvas.width, h = compassCanvas.height;
            const cx = w / 2, cy = h / 2, radius = (w / 2) - 10;
            ctx.clearRect(0, 0, w, h);

            // Dial Circle
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.fillStyle = '#111827';
            ctx.fill();
            ctx.strokeStyle = '#374151';
            ctx.lineWidth = 3;
            ctx.stroke();

            // Directions
            const dirs = [
                { angle: 0, label: 'N', color: '#ef4444' },
                { angle: 90, label: 'E', color: '#38bdf8' },
                { angle: 180, label: 'S', color: '#9ca3af' },
                { angle: 270, label: 'W', color: '#38bdf8' }
            ];
            ctx.font = 'bold 20px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            dirs.forEach(d => {
                const rad = (d.angle - 90) * Math.PI / 180;
                const x = cx + (radius - 22) * Math.cos(rad);
                const y = cy + (radius - 22) * Math.sin(rad);
                ctx.fillStyle = d.color;
                ctx.fillText(d.label, x, y);
            });

            // Needle
            const radHeading = (headingDeg - 90) * Math.PI / 180;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx + (radius - 12) * Math.cos(radHeading), cy + (radius - 12) * Math.sin(radHeading));
            ctx.strokeStyle = '#ef4444';
            ctx.lineWidth = 4;
            ctx.stroke();

            // Center Pin
            ctx.beginPath();
            ctx.arc(cx, cy, 5, 0, Math.PI * 2);
            ctx.fillStyle = '#ffffff';
            ctx.fill();
        }

        function getDirection(deg) {
            const d = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
            return d[Math.round(((deg % 360) + 360) % 360 / 45) % 8];
        }

        // ----------------- 60 FPS MOTION INTERPOLATION (LERP) -----------------
        let targetAlpha = 0, targetBeta = 0, targetGamma = 0;
        let currentAlpha = 0, currentBeta = 0, currentGamma = 0;
        let smoothHeading = 0;

        const valAlpha = document.getElementById('valAlpha');
        const valBeta = document.getElementById('valBeta');
        const valGamma = document.getElementById('valGamma');
        const valHeading = document.getElementById('valHeading');
        const valDirection = document.getElementById('valDirection');
        const statusEl = document.getElementById('status');

        // Shortest Angular Difference Helper (0° - 360° Wrap-around Fix)
        function lerpAngle(current, target, factor) {
            const diff = (target - current) % 360;
            const shortestDiff = ((2 * diff) % 360) - diff;
            return current + shortestDiff * factor;
        }

        function connectWS() {
            const ws = new WebSocket((location.protocol === 'https:' ? 'wss:' : 'ws:') + '//' + location.host + '/ws');
            
            ws.onopen = () => {
                statusEl.innerHTML = '✅ Connected (60 FPS Stream)';
                statusEl.className = 'connected';
            };

            ws.onmessage = (e) => {
                try {
                    const data = JSON.parse(e.data);
                    if (data.alpha !== undefined) {
                        targetAlpha = Number(data.alpha) || 0;
                        targetBeta = Number(data.beta) || 0;
                        targetGamma = Number(data.gamma) || 0;
                    }
                } catch(err) {}
            };

            ws.onclose = () => {
                statusEl.innerHTML = '❌ Stream Offline. Reconnecting...';
                statusEl.className = 'disconnected';
                setTimeout(connectWS, 1500);
            };
        }

        connectWS();
        drawCompass(0);

        // 60 FPS Render Loop with Smooth Interpolation
        function animate() {
            requestAnimationFrame(animate);

            // Smooth Motion Interpolation (LERP Factor: 0.18)
            currentAlpha = lerpAngle(currentAlpha, targetAlpha, 0.18);
            currentBeta += (targetBeta - currentBeta) * 0.18;
            currentGamma += (targetGamma - currentGamma) * 0.18;

            // HUD Updates
            valAlpha.textContent = currentAlpha.toFixed(1);
            valBeta.textContent = currentBeta.toFixed(1);
            valGamma.textContent = currentGamma.toFixed(1);

            smoothHeading = ((currentAlpha % 360) + 360) % 360;
            valHeading.textContent = smoothHeading.toFixed(1) + '°';
            valDirection.textContent = getDirection(smoothHeading);
            drawCompass(smoothHeading);

            // 3D Euler Angles Mapping
            const rad = Math.PI / 180;
            headingGroup.rotation.y = currentAlpha * rad;
            tiltGroup.rotation.x = currentBeta * rad;
            rollGroup.rotation.z = -currentGamma * rad;

            controls.update();
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

class ViewerServer:
    def __init__(self):
        self.clients = set()
        self.last_mtime = 0
        self.last_data = ""

    def get_live_file_path(self):
        if LIVE_FILE.exists():
            return LIVE_FILE
        return FALLBACK_FILE

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.clients.add(ws)
        print(f"✅ Viewer Client Connected. Active: {len(self.clients)}", flush=True)

        try:
            if self.last_data:
                await ws.send_str(self.last_data)
            async for msg in ws:
                if msg.type == WSMsgType.ERROR:
                    break
        finally:
            self.clients.remove(ws)
            print(f"❌ Viewer Client Disconnected. Active: {len(self.clients)}", flush=True)
        return ws

    async def broadcast_loop(self):
        while True:
            file_path = self.get_live_file_path()
            if file_path.exists():
                try:
                    mtime = os.path.getmtime(file_path)
                    if mtime > self.last_mtime:
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = f.read().strip()
                        if data and data != self.last_data:
                            self.last_data = data
                            self.last_mtime = mtime
                            if self.clients:
                                await asyncio.gather(*[c.send_str(data) for c in self.clients], return_exceptions=True)
                except Exception:
                    pass
            await asyncio.sleep(0.015) # ১৫ms আল্ট্রা-ফাস্ট লাইভ ব্রডকাস্ট

    async def index_handler(self, request):
        return web.Response(text=HTML, content_type="text/html")

    def start(self):
        app = web.Application()
        app.router.add_get("/", self.index_handler)
        app.router.add_get("/ws", self.websocket_handler)

        async def on_startup(app):
            asyncio.create_task(self.broadcast_loop())
            print("🚀 60 FPS Ultra-Smooth Broadcast Initialized", flush=True)

        app.on_startup.append(on_startup)

        print("\n" + "="*50)
        print("🐕 Hound 3D 60-FPS Ultra-Smooth Viewer Running")
        print("📡 Open in Browser: http://localhost:8082")
        print("="*50 + "\n", flush=True)

        web.run_app(app, host="0.0.0.0", port=8082)

if __name__ == "__main__":
    server = ViewerServer()
    server.start()