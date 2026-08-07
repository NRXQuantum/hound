<?php
function getIP() {
    $ipaddress = '';
    if (isset($_SERVER['HTTP_CLIENT_IP'])) $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
    else if(isset($_SERVER['HTTP_X_FORWARDED_FOR'])) $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
    else if(isset($_SERVER['HTTP_X_FORWARDED'])) $ipaddress = $_SERVER['HTTP_X_FORWARDED'];
    else if(isset($_SERVER['HTTP_FORWARDED_FOR'])) $ipaddress = $_SERVER['HTTP_FORWARDED_FOR'];
    else if(isset($_SERVER['HTTP_FORWARDED'])) $ipaddress = $_SERVER['HTTP_FORWARDED'];
    else if(isset($_SERVER['REMOTE_ADDR'])) $ipaddress = $_SERVER['REMOTE_ADDR'];
    else $ipaddress = 'UNKNOWN';
    return $ipaddress;
}

$ip = getIP();
$useragent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';
$referer = $_SERVER['HTTP_REFERER'] ?? 'Direct';
$method = $_SERVER['REQUEST_METHOD'] ?? 'Unknown';
$protocol = $_SERVER['SERVER_PROTOCOL'] ?? 'Unknown';

$log = "IP: $ip | User-Agent: $useragent | Referer: $referer | Method: $method | Protocol: $protocol | Time: " . date('Y-m-d H:i:s') . "\n";

file_put_contents('ip.txt', $log, FILE_APPEND | LOCK_EX);
file_put_contents('visitors.log', $log, FILE_APPEND | LOCK_EX);
?>