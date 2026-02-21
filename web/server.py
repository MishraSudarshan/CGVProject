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
    # Ensure we're running from the folder that contains server.py (works after zip extract on any device)
    if not os.path.isdir(WEB_DIR):
        print(f"Error: web directory not found: {WEB_DIR}")
        sys.exit(1)
    index_path = os.path.join(WEB_DIR, "index.html")
    if not os.path.isfile(index_path):
        print(f"Error: index.html not found in {WEB_DIR}")
        print("Make sure you extracted the full project (e.g. CGVProject folder with web/ inside it).")
        sys.exit(1)
    # Create leaderboard.txt if missing (e.g. after fresh extract on another device)
    if not os.path.isfile(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                f.write("{}")
            print(f"Created {LEADERBOARD_FILE}")
        except Exception as e:
            print(f"Warning: could not create leaderboard file: {e}")
    for name in ("app.js", "styles.css"):
        if not os.path.isfile(os.path.join(WEB_DIR, name)):
            print(f"Warning: {name} not found in {WEB_DIR}. Game may not work. Re-extract the full zip.")
    os.chdir(WEB_DIR)
    handler = partial(Handler, directory=WEB_DIR)
    # 127.0.0.1 = only this machine. Use --network to allow other devices on your LAN.
    host = "127.0.0.1"
    if len(sys.argv) > 1 and sys.argv[1] == "--network":
        host = "0.0.0.0"
        sys.argv = [sys.argv[0]] + sys.argv[2:]
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except Exception:
            pass
    try:
        server = ThreadingHTTPServer((host, port), handler)
    except OSError as e:
        if port == 8000:
            port = 8765
            try:
                server = ThreadingHTTPServer((host, port), handler)
                print(f"Port 8000 was in use. Using port {port} instead. Open http://127.0.0.1:{port}/")
            except OSError:
                print(f"Error: could not start server. Ports 8000 and 8765 may be in use or blocked.\n{e}")
                sys.exit(1)
        else:
            print(f"Error: could not start server on port {port}.\n{e}")
            sys.exit(1)
    try:
        url = f"http://127.0.0.1:{port}/"
        print(f"Working folder: {WEB_DIR}")
        print(f"Serving on {url}")
        if host == "0.0.0.0":
            print("Other devices: http://<this-computer-IP>:{}/".format(port))
        print("Open the URL above in your browser. Press Ctrl+C to stop.")
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)
