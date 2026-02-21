import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import sys
from functools import partial

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.txt")

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
    web_dir = os.path.join(BASE_DIR, "web")
    os.chdir(web_dir)
    handler = partial(Handler, directory=web_dir)
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except Exception:
            pass
    try:
        server = ThreadingHTTPServer(("0.0.0.0", port), handler)
    except OSError:
        port = 8765
        server = ThreadingHTTPServer(("0.0.0.0", port), handler)
    try:
        print(f"Serving on http://localhost:{port}/")
        server.serve_forever()
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
