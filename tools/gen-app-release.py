#!/usr/bin/env python3
"""Generate app-release.json — the app's remote version gate / kill switch.

The Android app fetches this (ETag-cached, fail-open) on startup and compares its own versionCode:
  * versionCode in blockedVersionCodes OR < minSupportedVersionCode -> blocking "update required"
  * versionCode < latestVersionCode                                 -> optional "update available"
  * otherwise                                                       -> up to date

Driven by the release-app.yml workflow_dispatch inputs (passed as env vars). Keeping old versions
working is the default (leave minSupportedVersionCode low); force everyone off by setting it to the
new versionCode. This script validates the inputs and warns on a non-monotonic versionCode.
"""
import json
import os
import sys

OUT = "app-release.json"
RELEASES_PAGE = "https://github.com/MuhammadTalhaBaloch/iptv/releases"


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
    version_code = _int("VERSION_CODE")
    min_supported = _int("MIN_SUPPORTED")
    version_name = (os.environ.get("VERSION_NAME") or "").strip() or str(version_code)
    download_url = (os.environ.get("DOWNLOAD_URL") or "").strip() or RELEASES_PAGE
    blocked = _blocked(os.environ.get("BLOCKED"))
    update_msg = (os.environ.get("UPDATE_MSG") or "").strip() or "A new version of the app is available."
    mandatory_msg = (os.environ.get("MANDATORY_MSG") or "").strip() or \
        "This version is no longer supported. Please update to continue."

    if min_supported > version_code:
        sys.exit(f"ERROR: minSupportedVersionCode ({min_supported}) cannot exceed the new "
                 f"latestVersionCode ({version_code}) — that would block the very version you publish.")

    if version_code in blocked:
        sys.exit(f"ERROR: blockedVersionCodes {blocked} includes the new latestVersionCode "
                 f"({version_code}) — that would soft-brick every user on the version you just "
                 f"published (they'd be blocked with no newer version to move to).")

    # Warn (don't fail) if the versionCode isn't higher than what's already published — sideload
    # can't downgrade, so this is almost always a mistake.
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as fh:
                prev = json.load(fh).get("latestVersionCode")
            if isinstance(prev, int) and version_code < prev:
                print(f"WARNING: latestVersionCode {version_code} is LOWER than the current {prev} "
                      f"(sideload can't downgrade — is this intentional?)")
        except Exception as e:  # noqa: BLE001 — best-effort sanity check only
            print(f"WARNING: couldn't read previous {OUT}: {e}")

    manifest = {
        "latestVersionCode": version_code,
        "latestVersionName": version_name,
        "minSupportedVersionCode": min_supported,
        "downloadUrl": download_url,
        "blockedVersionCodes": blocked,
        "updateMessage": update_msg,
        "mandatoryMessage": mandatory_msg,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"Wrote {OUT}: latest={version_code} ({version_name}), minSupported={min_supported}, "
          f"blocked={blocked}, downloadUrl={download_url}")


if __name__ == "__main__":
    main()
