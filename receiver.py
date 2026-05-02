#!/usr/bin/env python3
"""Simple HTTP receiver for environment variable payloads."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


class EnvReceiverHandler(BaseHTTPRequestHandler):
    def _write_json(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/env":
            self._write_json(404, {"error": "path not found", "expected_path": "/env"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)

        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._write_json(400, {"error": "invalid json body"})
            return

        env_vars = payload.get("env_vars", {})
        if not isinstance(env_vars, dict):
            self._write_json(400, {"error": "env_vars must be an object"})
            return

        response = {
            "status": "ok",
            "received_at": datetime.now(timezone.utc).isoformat(),
            "received_keys": sorted(env_vars.keys()),
            "received_count": len(env_vars),
            "missing_keys": payload.get("missing_keys", []),
            "source": {
                "hostname": payload.get("hostname"),
                "sent_at": payload.get("sent_at"),
            },
        }
        self._write_json(200, response)

    def log_message(self, format: str, *args) -> None:
        # Keep output minimal and readable.
        print(f"[{self.log_date_time_string()}] {format % args}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Receive environment variables through HTTP")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="Bind port (default: 8080)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = HTTPServer((args.host, args.port), EnvReceiverHandler)
    print(f"Receiver listening on http://{args.host}:{args.port}/env")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nReceiver stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
