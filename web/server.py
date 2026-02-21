import json
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Resolve paths from this script's location (works no matter how server.py is run)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SCRIPT_DIR)
WEB_DIR = _SCRIPT_DIR
LEADERBOARD_FILE = os.path.join(WEB_DIR, "leaderboard.txt")

class Handler(SimpleHTTPRequestHandler):
    def _send_json(self, data, code=200):
        b = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/api/leaderboard":
            if not os.path.isfile(LEADERBOARD_FILE):
                self._send_json({})
                return
            try:
                with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    data = json.loads(content) if content else {}
            except Exception:
                data = {}
            self._send_json(data)
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/leaderboard":
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                incoming = json.loads(body.decode("utf-8"))
                if not isinstance(incoming, dict):
                    self._send_json({"error": "invalid payload"}, 400)
                    return
            except Exception:
                self._send_json({"error": "invalid json"}, 400)
                return
            existing = {}
            if os.path.isfile(LEADERBOARD_FILE):
                try:
                    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        existing = json.loads(content) if content else {}
                except Exception:
                    existing = {}
            merged = existing.copy()
            for k, v in incoming.items():
                merged[str(k)] = v
            try:
                with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                    f.write(json.dumps(merged))
                self._send_json({"ok": True})
            except Exception:
                self._send_json({"error": "write failed"}, 500)
            return
        self.send_response(404)
        self.end_headers()

def main():
    if not os.path.isdir(WEB_DIR):
        print(f"Error: web directory not found: {WEB_DIR}")
        sys.exit(1)
    index_path = os.path.join(WEB_DIR, "index.html")
    if not os.path.isfile(index_path):
        print(f"Error: index.html not found in {WEB_DIR}")
        sys.exit(1)
    os.chdir(WEB_DIR)
    handler = partial(Handler, directory=WEB_DIR)
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except Exception:
            pass
    host = "127.0.0.1"
    try:
        server = ThreadingHTTPServer((host, port), handler)
    except OSError:
        port = 8765
        server = ThreadingHTTPServer((host, port), handler)
    try:
        url = f"http://127.0.0.1:{port}/"
        print(f"Serving on {url}")
        print("Open that URL in your browser. If it fails, allow Python in Windows Firewall.")
        server.serve_forever()
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
