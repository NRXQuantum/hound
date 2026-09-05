import sys
import re
import time
import subprocess
from urllib.parse import urlparse, urljoin
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):
    target_url = ""

    # Open Graph মেটা ডেটা (আপনার দেওয়া তথ্য অনুযায়ী)
    OG_DATA = {
        "type": "video.other",
        "title": "Body Language Analysis কি? মিথ্যা বোঝার বৈজ্ঞানিক উপায় কি? কিভাবে Human Lie Detector হওয়া যায়?",
        "description": "YouTube",
        "site_name": "YouTube",
        "image": "https://i.ytimg.com/vi/d_NKqZCuozI/hq720.jpg?sqp=-oaymwEcCK4FEIIDSEbyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLCXkvMmLbQP-EJH05NhiE6LZulZuA"
    }

    def do_GET(self):
        self.handle_request()

    def do_HEAD(self):
        self.handle_request(is_head=True)

    def do_POST(self):
        self.handle_request()

    def handle_request(self, is_head=False):
        destination = urljoin(self.target_url, self.path) if self.path and self.path != "/" else self.target_url

        # সোশ্যাল মিডিয়া বট ও প্রিভিউ ক্রলার চেনার কিওয়ার্ড
        user_agent = self.headers.get('User-Agent', '').lower()
        crawler_keywords = [
            'facebookexternalhit', 'whatsapp', 'telegrambot', 
            'twitterbot', 'discordbot', 'slackbot', 'linkedinbot', 
            'meta-externalagent', 'googlebot', 'bingbot'
        ]
        is_crawler = any(bot in user_agent for bot in crawler_keywords)

        # বট হলে অথবা সরাসরি পেজ লোড হলে Open Graph সহ HTML পেজ সার্ভ করা
        html_content = f"""<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <title>{self.OG_DATA['title']}</title>
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:type" content="{self.OG_DATA['type']}" />
    <meta property="og:title" content="{self.OG_DATA['title']}" />
    <meta property="og:description" content="{self.OG_DATA['description']}" />
    <meta property="og:site_name" content="{self.OG_DATA['site_name']}" />
    <meta property="og:image" content="{self.OG_DATA['image']}" />

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{self.OG_DATA['title']}" />
    <meta name="twitter:description" content="{self.OG_DATA['description']}" />
    <meta name="twitter:image" content="{self.OG_DATA['image']}" />

    <!-- আসল ইউজারদের জন্য ফাস্ট অটো-রিডাইরেক্ট -->
    <meta http-equiv="refresh" content="0; url={destination}" />
    <script type="text/javascript">
        window.location.replace("{destination}");
    </script>
</head>
<body style="background:#0f0f0f; color:#fff; font-family:sans-serif; text-align:center; padding-top:50px;">
    <p>Redirecting to destination...</p>
    <p>If you are not redirected automatically, <a href="{destination}" style="color:#3ea6ff;">click here</a>.</p>
</body>
</html>"""

        encoded_html = html_content.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded_html)))
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()

        if not is_head:
            self.wfile.write(encoded_html)

    def log_message(self, format, *args):
        pass


def start_cloudflared(port):
    """Starts cloudflared as a subprocess and captures the generated URL."""
    print("[*] Starting Cloudflare tunnel...")
    cmd = ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    except FileNotFoundError:
        print("[!] Error: 'cloudflared' command not found. Ensure it is installed and in your PATH.")
        return None, None

    tunnel_url = None
    # api.trycloudflare বাদ দিয়ে আসল টানেল লিঙ্ক ক্যাচ করা
    url_pattern = re.compile(r'https://(?!api\.)[a-zA-Z0-9-]+\.trycloudflare\.com')

    start_time = time.time()
    while time.time() - start_time < 30:
        line = proc.stderr.readline()
        if not line and proc.poll() is not None:
            break
        match = url_pattern.search(line)
        if match:
            tunnel_url = match.group(0)
            break

    if not tunnel_url:
        print("[!] Could not retrieve tunnel URL. Tunnel startup failed or timed out.")
        proc.terminate()
        return None, None

    return proc, tunnel_url


def main():
    while True:
        target = input("Enter destination URL (e.g., https://example.com): ").strip()
        if not target:
            print("[!] Error: Destination URL cannot be empty.\n")
            continue

        if not target.startswith(("http://", "https://")):
            target = "https://" + target

        parsed = urlparse(target)
        if not parsed.netloc:
            print("[!] Error: Invalid URL. Please provide a valid domain.\n")
            continue
        break

    port_input = input("Enter local port (Default 8080): ").strip()
    port = int(port_input) if port_input.isdigit() else 8080

    use_tunnel = input("Enable Cloudflare Tunnel? (y/n, Default 'n'): ").strip().lower()

    RedirectHandler.target_url = target
    server_address = ('127.0.0.1', port)

    try:
        httpd = ThreadingHTTPServer(server_address, RedirectHandler)
    except OSError as e:
        print(f"[!] Error starting local server on port {port}: {e}")
        return

    tunnel_proc = None
    tunnel_url = None

    if use_tunnel == 'y':
        tunnel_proc, tunnel_url = start_cloudflared(port)

    print("\n" + "=" * 60)
    print(f"Target URL : {target}")
    print(f"Local URL  : http://localhost:{port}")
    if tunnel_url:
        print(f"Public URL : {tunnel_url}")
    print("=" * 60)
    print("[*] Server is running with Open Graph Previews enabled.")
    print("[*] Press Ctrl+C to stop.\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping server...")
    finally:
        httpd.shutdown()
        httpd.server_close()
        if tunnel_proc:
            print("[*] Terminating tunnel process...")
            tunnel_proc.terminate()
            tunnel_proc.wait()
        print("[+] Everything shut down cleanly.")

if __name__ == "__main__":
    main()