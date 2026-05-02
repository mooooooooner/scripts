#!/usr/bin/env python3
"""Collect selected environment variables and send them to an HTTP endpoint."""

from __future__ import annotations

import argparse
import json
import os
import socket
from datetime import datetime, timezone
from urllib import request
from urllib.error import HTTPError, URLError

DEFAULT_ENV_KEYS = [
    "PATH",
    "USERNAME",
    "TEMP",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send selected environment variables")
    parser.add_argument(
        "--endpoint",
        required=True,
        help="Target endpoint, e.g. http://127.0.0.1:8080/env",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10,
        help="HTTP timeout in seconds (default: 10)",
    )
    return parser.parse_args()


def build_payload(keys: list[str]) -> dict:
    env_vars: dict[str, str] = {}
    missing_keys: list[str] = []

    for key in keys:
        value = os.getenv(key)
        if value is None:
            missing_keys.append(key)
        else:
            env_vars[key] = value

    return {
        "hostname": socket.gethostname(),
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "env_vars": env_vars,
        "missing_keys": missing_keys,
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
    payload = build_payload(DEFAULT_ENV_KEYS)

    print("Sending payload:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    try:
        status, body = send_payload(args.endpoint, payload, args.timeout)
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
