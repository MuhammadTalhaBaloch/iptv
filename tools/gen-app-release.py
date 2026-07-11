#!/usr/bin/env python3
"""Generate app-release.json — the app's remote version KILL SWITCH (no auto-update).

The Android app fetches this (ETag-cached, fail-open) on startup and blocks itself iff its own
versionCode is in blockedVersionCodes OR below minSupportedVersionCode; otherwise it runs. There is
no auto-update prompt and no APK download URL — a blocked user gets a newer build out-of-band
(whatever the blockedMessage says).

Driven by the release-app.yml workflow_dispatch inputs (passed as env vars). Keeping versions working
is the default (leave minSupportedVersionCode low, blockedVersionCodes empty); raise the floor or add
codes to kill old builds.

NOTE: the gate is code inside the app, so it only affects builds that already contain it — never a
version distributed before this feature shipped.
"""
import json
import os
import sys

OUT = "app-release.json"
DEFAULT_MSG = "This version is no longer supported. Please install the latest version to continue."


def _int(name, required=True, default=0):
    raw = (os.environ.get(name) or "").strip()
    if not raw:
        if required:
            sys.exit(f"ERROR: {name} is required")
        return default
    try:
        return int(raw)
    except ValueError:
        sys.exit(f"ERROR: {name} must be an integer, got {raw!r}")


def _blocked(raw):
    out = []
    for part in (raw or "").split(","):
        part = part.strip()
        if part:
            try:
                out.append(int(part))
            except ValueError:
                sys.exit(f"ERROR: blockedVersionCodes must be integers, got {part!r}")
    return sorted(set(out))


def main():
    min_supported = _int("MIN_SUPPORTED")
    blocked = _blocked(os.environ.get("BLOCKED"))
    message = (os.environ.get("BLOCKED_MSG") or "").strip() or DEFAULT_MSG

    if min_supported < 0:
        sys.exit(f"ERROR: minSupportedVersionCode ({min_supported}) must be >= 0")

    manifest = {
        "minSupportedVersionCode": min_supported,
        "blockedVersionCodes": blocked,
        "blockedMessage": message,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"Wrote {OUT}: minSupported={min_supported}, blocked={blocked}")


if __name__ == "__main__":
    main()
