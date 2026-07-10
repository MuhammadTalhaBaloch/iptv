#!/usr/bin/env python3
"""Experiment: reconcile the app's two channel-provisioning paths.

The app reaches channels two ways, both listed in sources.json:
  * the flat catalog **index** (index.m3u) — what Search / Play-all use, and
  * the **per-dimension** playlists (category / country / language / region / subdivision / city)
    — what the browse menu drills into on demand.

Every channel should appear in both. This fetches every source playlist, dedups the stream links,
and reports the difference:
  * browseOnly — links in a per-dimension playlist but MISSING from the flat index
  * indexOnly  — links in the flat index but in NO per-dimension playlist (not browseable)

"Link" = a stream URL as it appears in the M3U (no liveness probe). Reads the committed sources.json
so it reflects exactly the registry the app ships/fetches. Writes out/sources-vs-index.json.
"""
import json
import os
import urllib.request
import concurrent.futures as cf

UA = {"User-Agent": "iptv-compare-experiment"}
SOURCES = "sources.json"
OUT_DIR = "out"
OUT = os.path.join(OUT_DIR, "sources-vs-index.json")


def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return url, r.read().decode("utf-8", "ignore")
    except Exception as e:  # noqa: BLE001 — a dead playlist just contributes nothing
        return url, None


def links(text):
    return {ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sources = json.load(open(SOURCES, encoding="utf-8"))["sources"]
    index_url = next(s["url"] for s in sources if s["url"].endswith("/index.m3u"))
    dim = [s for s in sources if s["type"] != "index"]
    print(f"index: {index_url}")
    print(f"per-dimension source playlists: {len(dim)}")

    # List B — flat catalog index
    _, idx_txt = fetch(index_url)
    B = links(idx_txt) if idx_txt else set()
    print(f"List B (index) links: {len(B)}")

    # List A — union of all per-dimension source playlists (+ provenance for the diff)
    A = set()
    origin = {}  # link -> set(source names) that contained it
    ok = fail = 0
    with cf.ThreadPoolExecutor(max_workers=48) as ex:
        futs = {ex.submit(fetch, s["url"]): s for s in dim}
        for fut in cf.as_completed(futs):
            s = futs[fut]
            _, txt = fut.result()
            if txt is None:
                fail += 1
                continue
            ok += 1
            for u in links(txt):
                A.add(u)
                origin.setdefault(u, set()).add(f"{s['type']}:{s.get('name') or s.get('code')}")
    print(f"List A (browse sources) ok={ok} failed={fail}; unique links: {len(A)}")

    browse_only = sorted(A - B)
    index_only = sorted(B - A)
    report = {
        "indexUrl": index_url,
        "counts": {
            "index": len(B),
            "browse": len(A),
            "both": len(A & B),
            "browseOnly": len(browse_only),
            "indexOnly": len(index_only),
            "sourcePlaylists": len(dim),
            "fetchOk": ok,
            "fetchFailed": fail,
        },
        "browseOnly": [{"url": u, "foundIn": sorted(origin.get(u, []))} for u in browse_only],
        "indexOnly": index_only,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n=== RESULT ===")
    for k, v in report["counts"].items():
        print(f"  {k:16} {v}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
