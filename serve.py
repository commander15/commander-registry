#!/usr/bin/env python3
import http.server
import socketserver
import sys
import os

from update import main as update

PORT = 8000

if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port: {sys.argv[1]}. Using default port {PORT}.")

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local testing and client tool verification
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        # Prevent local caching during development/testing
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def run(port=PORT):
    # Change working directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    handler = CORSRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"==================================================")
        print(f" Serving commander-registry locally")
        print(f" URL: http://localhost:{port}")
        print(f" Root: {script_dir}")
        print(f" Press Ctrl+C to stop")
        print(f"==================================================")
        try:
            update()
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run()