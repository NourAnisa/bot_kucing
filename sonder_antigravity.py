#!/usr/bin/env python3
"""
sonder_antigravity.py — Connect Google Antigravity to SondeR cat desktop pet.

Features:
  - Notifies your desktop cat (Michan) when Antigravity starts working ("working")
    and finishes ("done"), causing the cat to think along and celebrate!
  - Sends speech bubble messages to the cat via the local HTTP Webhook server.
  - Can be used as a CLI tool, process wrapper, or imported as a Python context manager.

Usage (CLI):
  python sonder_antigravity.py working [label]
  python sonder_antigravity.py done [label]
  python sonder_antigravity.py say "Hello from Antigravity!"
  python sonder_antigravity.py run [label] -- <command> [args...]

Usage (Python):
  from sonder_antigravity import cat_task, notify_working, notify_done, notify_say

  with cat_task("Antigravity: Building project"):
      run_long_task()
"""

import sys
import os
import subprocess
import json
import urllib.request
import urllib.error
from contextlib import contextmanager

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AGENT_FILE = os.path.join(os.path.expanduser("~"), ".sondercat_agent")
HTTP_URL = "http://127.0.0.1:19842"


def _send_http(endpoint, payload):
    """Attempt sending to local HTTP webhook server; returns True if successful."""
    try:
        url = f"{HTTP_URL}{endpoint}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            return resp.status == 200
    except Exception:
        return False


def notify_working(label="Antigravity"):
    """Signal that an agent started working."""
    _send_http("/agent", {"state": "working", "label": label})
    try:
        with open(AGENT_FILE, "w", encoding="utf-8") as f:
            f.write(f"working|{label}")
    except Exception:
        pass


def notify_done(label="Antigravity"):
    """Signal that an agent completed its work."""
    _send_http("/agent", {"state": "done", "label": label})
    try:
        with open(AGENT_FILE, "w", encoding="utf-8") as f:
            f.write(f"done|{label}")
    except Exception:
        pass


def notify_clear():
    """Clear agent state."""
    _send_http("/agent", {"state": "clear"})
    try:
        with open(AGENT_FILE, "w", encoding="utf-8") as f:
            f.write("")
    except Exception:
        pass


def notify_say(text, duration=4.0):
    """Make the cat say something in a floating speech bubble."""
    return _send_http("/say", {"text": text, "duration": duration})


@contextmanager
def cat_task(label="Antigravity"):
    """Context manager for tracking a task with SondeR cat."""
    notify_working(label)
    try:
        yield
    finally:
        notify_done(label)


def main(argv):
    if len(argv) < 1:
        print(__doc__)
        return 1

    cmd = argv[0].lower()

    if cmd == "working":
        label = argv[1] if len(argv) > 1 else "Antigravity"
        notify_working(label)
        print(f"[SondeR Cat] Michan is now thinking along with: {label}")
        return 0

    if cmd == "done":
        label = argv[1] if len(argv) > 1 else "Antigravity"
        notify_done(label)
        print(f"[SondeR Cat] Michan celebrated completion of: {label}")
        return 0

    if cmd == "clear":
        notify_clear()
        print("[SondeR Cat] Agent status cleared.")
        return 0

    if cmd == "say":
        if len(argv) < 2:
            print("Usage: python sonder_antigravity.py say \"<text>\"")
            return 1
        text = argv[1]
        notify_say(text)
        print(f"[SondeR Cat] Said: {text}")
        return 0

    if cmd == "run":
        rest = argv[1:]
        label = "Antigravity"
        if rest and rest[0] != "--":
            label = rest.pop(0)
        if rest and rest[0] == "--":
            rest.pop(0)
        if not rest:
            print("run: no command given after --")
            return 1

        notify_working(label)
        try:
            return subprocess.call(rest)
        finally:
            notify_done(label)

    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
