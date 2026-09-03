from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class DeviceInfo(BaseModel):
    userAgent: Optional[str] = None
    platform: Optional[str] = None
    language: Optional[str] = None
    languages: Optional[List[str]] = None
    cookieEnabled: Optional[bool] = None
    hardwareConcurrency: Optional[Any] = None
    deviceMemory: Optional[Any] = None
    maxTouchPoints: Optional[int] = None
    screenWidth: Optional[int] = None
    screenHeight: Optional[int] = None
    availWidth: Optional[int] = None
    availHeight: Optional[int] = None
    timezone: Optional[str] = None
    timezoneOffset: Optional[int] = None
    localTime: Optional[str] = None

class BatteryInfo(BaseModel):
    charging: Optional[bool] = None
    level: Optional[str] = None
    chargingTime: Optional[Any] = None
    dischargingTime: Optional[Any] = None

class IpInfo(BaseModel):
    ip: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    loc: Optional[str] = None
    org: Optional[str] = None
    timezone: Optional[str] = None

class NetworkInfo(BaseModel):
    connectionType: Optional[str] = None
    effectiveType: Optional[str] = None
    downlink: Optional[Any] = None
    rtt: Optional[Any] = None
    saveData: Optional[bool] = None

class Orientation(BaseModel):
    alpha: Optional[float] = None
    beta: Optional[float] = None
    gamma: Optional[float] = None
    timestamp: Optional[str] = None

class WebhookPayload(BaseModel):
    userId: Optional[str] = None
    timestamp: Optional[str] = None
    deviceInfo: Optional[DeviceInfo] = None
    batteryInfo: Optional[BatteryInfo] = None
    networkInfo: Optional[NetworkInfo] = None
    clientHints: Optional[Dict[str, Any]] = None
    lieDetection: Optional[Dict[str, Any]] = None
    cpuBenchmark: Optional[Dict[str, Any]] = None
    mediaCapabilities: Optional[Dict[str, Any]] = None
    v8MemoryHeap: Optional[Dict[str, Any]] = None
    interactionModes: Optional[Dict[str, Any]] = None
    intlSystem: Optional[Dict[str, Any]] = None
    gamepadIntel: Optional[Dict[str, Any]] = None
    screenDetails: Optional[Dict[str, Any]] = None
    navigationTiming: Optional[Dict[str, Any]] = None
    audioContextIntel: Optional[Dict[str, Any]] = None
    storageIntel: Optional[Dict[str, Any]] = None
    permissionIntel: Optional[Dict[str, Any]] = None
    mathQuirks: Optional[Dict[str, Any]] = None
    emojiMetrics: Optional[Dict[str, Any]] = None
    displayIntel: Optional[Dict[str, Any]] = None
    webgpuFingerprint: Optional[Dict[str, Any]] = None
    antiDetectFlags: Optional[Dict[str, Any]] = None
    systemVoices: Optional[List[str]] = None
    ipInfo: Optional[IpInfo] = None
    gps: Optional[Dict[str, Any]] = None
    localIP: Optional[str] = None
    webrtcPublicIP: Optional[str] = None
    orientation: Optional[Orientation] = None
    canvasFingerprint: Optional[str] = None
    webglFingerprint: Optional[Any] = None
    audioFingerprint: Optional[str] = None
    fontsSignature: Optional[str] = None
    clientRects: Optional[Dict[str, Any]] = None
    mediaDevices: Optional[List[Dict[str, Any]]] = None
    usbDevices: Optional[List[Dict[str, Any]]] = None