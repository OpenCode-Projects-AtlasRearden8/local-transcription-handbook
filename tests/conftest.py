import http.server
import json
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def std_response(content: str = "MOCK SUMMARY OUTPUT") -> bytes:
    return json.dumps(
        {"choices": [{"message": {"content": content}}]}
    ).encode()


class OpenAICompatHandler(http.server.BaseHTTPRequestHandler):
    received: list[dict] = []
    response: bytes = std_response()

    def do_POST(self):
        if not self.path.endswith("/chat/completions"):
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        type(self).received.append(body)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(type(self).response)

    def log_message(self, *args):  # silence test noise
        pass


def make_server(handler_cls):
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", 0), handler_cls)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


@pytest.fixture
def mock_api():
    OpenAICompatHandler.received = []
    server = make_server(OpenAICompatHandler)
    yield OpenAICompatHandler, f"http://127.0.0.1:{server.server_address[1]}/v1"
    server.shutdown()
    server.server_close()


def run_script(*args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "summarize_transcript.py"), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
