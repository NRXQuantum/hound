#!/usr/bin/env python3
"""
Python 3D Viewer Server with Compass & Heading (Gimbal Lock Fixed)
Run: python viewer_server.py
"""

import asyncio
import json
import os
import webbrowser
from aiohttp import web, WSMsgType

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-time 3D Orientation Viewer (Python)</title>
    <style>
        body { margin: 0; overflow: hidden; background: #1a1a2e; color: white; font-family: Arial; }
        #info {
            position: absolute; top: 20px; left: 20px;
            background: rgba(0,0,0,0.8); padding: 15px 25px;
            border-radius: 10px; z-index: 100; font-size: 14px;
            border-left: 4px solid #00ff88;
            min-width: 200px; backdrop-filter: blur(5px);
        }
        #info h2 { margin: 0 0 10px 0; font-size: 18px; color: #00ff88; }
        #info div { padding: 3px 0; }
        #info span { color: #ffcc00; font-weight: bold; }
        #info .heading-text { color: #88ddff; font-weight: bold; font-size: 16px; }

        #compass-container {
            position: absolute; top: 20px; right: 20px;
            background: rgba(0,0,0,0.7); border-radius: 50%; padding: 10px;
            z-index: 100; border: 2px solid #333;
            box-shadow: 0 0 20px rgba(0,0,0,0.8); backdrop-filter: blur(5px);
        }
        #compass-container canvas { display: block; width: 80px; height: 80px; }

        #status {
            position: absolute; bottom: 30px; left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.7); padding: 10px 25px;
            border-radius: 20px; font-size: 14px; z-index: 100;
            backdrop-filter: blur(5px);
        }
        .connected { color: #00ff88; }
        .disconnected { color: #ff4444; }
        #controls-hint {
            position: absolute; bottom: 80px; right: 30px;
            color: #666; font-size: 12px;
            background: rgba(0,0,0,0.5); padding: 8px 15px;
            border-radius: 15px;
        }
    </style>
</head>
<body>
    <div id="info">
        <h2>📱 Live Orientation</h2>
        <div>Alpha: <span id="alpha">0.0</span>°</div>
        <div>Beta:  <span id="beta">0.0</span>°</div>
        <div>Gamma: <span id="gamma">0.0</span>°</div>
        <div style="margin-top: 8px; border-top: 1px solid #444; padding-top: 8px;">
            🧭 Heading: <span class="heading-text" id="heading">0.0°</span> 
            <span class="heading-text" id="direction">N</span>
        </div>
    </div>
    <div id="compass-container"><canvas id="compassCanvas" width="160" height="160"></canvas></div>
    <div id="status">🔄 Connecting to WebSocket...</div>
    <div id="controls-hint">🖱️ Drag to rotate | Scroll to zoom</div>

    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }
        }
    </script>
    <script type="module">
        import * as THREE from 'three';
        import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

        const scene = new THREE.Scene(); scene.background = new THREE.Color(0x1a1a2e);
        const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(3, 2, 5); camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true; controls.dampingFactor = 0.08;
        controls.target.set(0, 0, 0); controls.update();

        const ambient = new THREE.AmbientLight(0x404060); scene.add(ambient);
        const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
        dirLight.position.set(5, 10, 7); dirLight.castShadow = true; scene.add(dirLight);
        const fillLight = new THREE.DirectionalLight(0x4488ff, 0.5);
        fillLight.position.set(-3, 1, -2); scene.add(fillLight);
        const backLight = new THREE.DirectionalLight(0xff8844, 0.3);
        backLight.position.set(0, -2, -5); scene.add(backLight);

        const gridHelper = new THREE.GridHelper(4, 10, 0x00ff88, 0x336633);
        gridHelper.position.y = -0.6; scene.add(gridHelper);
        const axesHelper = new THREE.AxesHelper(1.8);
        axesHelper.position.y = -0.6; scene.add(axesHelper);

        function makeLabel(text, color, pos) {
            const canvas = document.createElement('canvas');
            canvas.width = 64; canvas.height = 64;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = color; ctx.font = 'Bold 40px Arial';
            ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.fillText(text, 32, 32);
            const texture = new THREE.CanvasTexture(canvas);
            const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false });
            const sprite = new THREE.Sprite(material);
            sprite.position.copy(pos); sprite.scale.set(0.4, 0.4, 1);
            return sprite;
        }
        scene.add(makeLabel('X', '#ff4444', new THREE.Vector3(2, -0.6, 0)));
        scene.add(makeLabel('Y', '#44ff44', new THREE.Vector3(0, 1.8, 0)));
        scene.add(makeLabel('Z', '#4488ff', new THREE.Vector3(0, -0.6, 2)));

        // ===== 3D Phone Model (Gimbal Lock Fix: World Axis) =====
        const headingGroup = new THREE.Group(); headingGroup.position.y = 0.5; scene.add(headingGroup);
        const tiltGroup = new THREE.Group(); headingGroup.add(tiltGroup);
        const rollGroup = new THREE.Group(); tiltGroup.add(rollGroup);
        const phoneGroup = new THREE.Group(); phoneGroup.rotation.x = -Math.PI / 2; rollGroup.add(phoneGroup);

        const bodyMat = new THREE.MeshStandardMaterial({ color: 0x2a2a3e, roughness: 0.3, metalness: 0.8 });
        const body = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.5, 0.2), bodyMat);
        body.castShadow = true; phoneGroup.add(body);
        const screenMat = new THREE.MeshStandardMaterial({ color: 0x00aaff, emissive: new THREE.Color(0x0066ff), emissiveIntensity: 0.6 });
        const screen = new THREE.Mesh(new THREE.BoxGeometry(0.75, 1.25, 0.03), screenMat);
        screen.position.z = 0.12; phoneGroup.add(screen);
        const dotMat = new THREE.MeshStandardMaterial({ color: 0x111111 });
        const dot = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 8), dotMat);
        dot.position.set(0, 0.7, 0.12); phoneGroup.add(dot);
        const spkMat = new THREE.MeshStandardMaterial({ color: 0x333344 });
        const spk = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.02, 0.02), spkMat);
        spk.position.set(0, -0.7, 0.12); phoneGroup.add(spk);
        const btnMat = new THREE.MeshStandardMaterial({ color: 0x555566 });
        const btn1 = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.1, 0.04), btnMat);
        btn1.position.set(0.46, 0.3, 0); phoneGroup.add(btn1);
        const btn2 = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.1, 0.04), btnMat);
        btn2.position.set(0.46, -0.1, 0); phoneGroup.add(btn2);

        const arrowGroup = new THREE.Group(); phoneGroup.add(arrowGroup);
        const shaftMat = new THREE.MeshStandardMaterial({ color: 0xff6644, emissive: new THREE.Color(0xff2200), emissiveIntensity: 0.2 });
        const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.0), shaftMat);
        shaft.position.y = 0.5; arrowGroup.add(shaft);
        const headMat = new THREE.MeshStandardMaterial({ color: 0xff6644, emissive: new THREE.Color(0xff2200), emissiveIntensity: 0.3 });
        const head = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.2, 8), headMat);
        head.position.y = 1.1; arrowGroup.add(head);

        // ===== Compass Drawing =====
        const compassCanvas = document.getElementById('compassCanvas');
        const ctx = compassCanvas.getContext('2d');
        function drawCompass(headingDeg) {
            const w = compassCanvas.width, h = compassCanvas.height, cx = w/2, cy = h/2, radius = Math.min(w,h)/2 - 10;
            ctx.clearRect(0, 0, w, h);
            ctx.beginPath(); ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.fillStyle = '#1a1a2e'; ctx.fill();
            ctx.strokeStyle = '#444'; ctx.lineWidth = 2; ctx.stroke();
            const dirs = [{ angle: 0, label: 'N' }, { angle: 90, label: 'E' }, { angle: 180, label: 'S' }, { angle: 270, label: 'W' }];
            ctx.font = 'Bold 18px Arial'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            dirs.forEach(d => {
                const rad = (d.angle - 90) * Math.PI / 180;
                const x = cx + (radius - 20) * Math.cos(rad), y = cy + (radius - 20) * Math.sin(rad);
                ctx.fillStyle = d.label === 'N' ? '#ff4444' : '#88aaff';
                ctx.fillText(d.label, x, y);
            });
            for (let i = 0; i < 360; i += 30) {
                if (i % 90 === 0) continue;
                const rad = (i - 90) * Math.PI / 180;
                const ox = cx + radius * Math.cos(rad), oy = cy + radius * Math.sin(rad);
                const ix = cx + (radius - 8) * Math.cos(rad), iy = cy + (radius - 8) * Math.sin(rad);
                ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(ix, iy);
                ctx.strokeStyle = '#666'; ctx.lineWidth = 1; ctx.stroke();
            }
            const radHeading = (headingDeg - 90) * Math.PI / 180;
            ctx.beginPath(); ctx.moveTo(cx, cy);
            ctx.lineTo(cx + (radius - 10) * Math.cos(radHeading), cy + (radius - 10) * Math.sin(radHeading));
            ctx.strokeStyle = '#ff3333'; ctx.lineWidth = 3; ctx.stroke();
            ctx.beginPath(); ctx.arc(cx, cy, 4, 0, Math.PI * 2);
            ctx.fillStyle = '#ffffff'; ctx.fill();
            ctx.strokeStyle = '#333'; ctx.lineWidth = 1; ctx.stroke();
        }

        // ===== WebSocket =====
        const statusEl = document.getElementById('status');
        const alphaEl = document.getElementById('alpha');
        const betaEl = document.getElementById('beta');
        const gammaEl = document.getElementById('gamma');
        const headingEl = document.getElementById('heading');
        const directionEl = document.getElementById('direction');

        function getDirection(deg) {
            const dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
            return dirs[Math.round(((deg % 360) + 360) % 360 / 45) % 8];
        }

        let ws;
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            ws.onopen = function() { statusEl.innerHTML = '✅ Connected to Python WebSocket'; statusEl.className = 'connected'; };
            ws.onmessage = function(event) {
                try {
                    const data = JSON.parse(event.data);
                    if (data.alpha !== undefined) {
                        alphaEl.textContent = data.alpha.toFixed(2);
                        betaEl.textContent = data.beta.toFixed(2);
                        gammaEl.textContent = data.gamma.toFixed(2);
                        const heading = ((data.alpha % 360) + 360) % 360;
                        headingEl.textContent = heading.toFixed(1) + '°';
                        directionEl.textContent = getDirection(heading);
                        drawCompass(heading);
                        const aR = THREE.MathUtils.degToRad(data.alpha);
                        const bR = THREE.MathUtils.degToRad(data.beta);
                        const gR = THREE.MathUtils.degToRad(data.gamma);
                        headingGroup.rotation.y = aR;
                        tiltGroup.rotation.x = bR;
                        rollGroup.rotation.z = gR;
                    }
                } catch(e) { console.error(e); }
            };
            ws.onclose = function() { statusEl.innerHTML = '❌ Disconnected. Reconnecting in 3s...'; statusEl.className = 'disconnected'; setTimeout(connectWebSocket, 3000); };
            ws.onerror = function(error) { ws.close(); };
        }
        connectWebSocket();

        function animate() { requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }
        animate();
        window.addEventListener('resize', function() {
            camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
        drawCompass(0);
        console.log('3D Viewer started.');
    </script>
</body>
</html>
"""

class ViewerServer:
    def __init__(self):
        self.clients = set()
        self.last_mtime = 0
        self.last_data = None
        self.file_path = 'live_orientation.json'

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.clients.add(ws)
        print(f"✅ Client connected. Total: {len(self.clients)}")
        try:
            if self.last_data:
                await ws.send_str(self.last_data)
            async for msg in ws:
                if msg.type == WSMsgType.ERROR: break
        finally:
            self.clients.remove(ws)
            print(f"❌ Client disconnected. Total: {len(self.clients)}")
        return ws

    async def broadcast_loop(self):
        while True:
            if os.path.exists(self.file_path):
                try:
                    mtime = os.path.getmtime(self.file_path)
                    if mtime > self.last_mtime:
                        with open(self.file_path, 'r') as f: data = f.read().strip()
                        if data and data != self.last_data:
                            json.loads(data)
                            self.last_data = data
                            self.last_mtime = mtime
                            print(f"📤 Broadcasting: {data[:50]}...")
                            if self.clients:
                                await asyncio.gather(*[client.send_str(data) for client in self.clients], return_exceptions=True)
                except Exception as e: print(f"⚠️ Error reading file: {e}")
            await asyncio.sleep(0.1)

    async def index_handler(self, request):
        return web.Response(text=HTML, content_type='text/html')

    def start(self):
        app = web.Application()
        app.router.add_get('/', self.index_handler)
        app.router.add_get('/ws', self.websocket_handler)
        async def on_startup(app): asyncio.create_task(self.broadcast_loop()); print("✅ Broadcast loop started.")
        app.on_startup.append(on_startup)
        print("="*50)
        print("✅ Python 3D Viewer Server Started (Compass & Heading)")
        print("📡 Open in browser: http://localhost:8082")
        print("="*50)
        webbrowser.open("http://localhost:8082")
        web.run_app(app, host='0.0.0.0', port=8082)

if __name__ == '__main__':
    server = ViewerServer()
    server.start()