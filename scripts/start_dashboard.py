#!/usr/bin/env python3
"""
Simple HTTP server for the MDL Benchmark Dashboard
"""

import http.server
import socketserver
import webbrowser
import os
from threading import Timer

PORT = 8080
DIRECTORY = "/Users/praveen/Praveen/frontend"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def open_browser():
    """Open the browser after a short delay"""
    webbrowser.open(f'http://localhost:{PORT}')

print("="*80)
print("MDL BENCHMARK DASHBOARD - LOCAL SERVER")
print("="*80)
print(f"Starting server on port {PORT}...")
print(f"Serving files from: {DIRECTORY}")
print(f"\nOpen your browser to: http://localhost:{PORT}")
print("\nPress Ctrl+C to stop the server")
print("="*80)

# Open browser after 1 second
Timer(1, open_browser).start()

# Start server
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        print("="*80)
