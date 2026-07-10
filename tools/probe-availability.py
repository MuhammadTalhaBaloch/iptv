#!/usr/bin/env python3
"""Faithful replica of the app's Deep-Refresh reachability probe (data/remote/StreamProbe.kt),
run standalone so the SAME logic can be executed from different geos and the results diffed.

Per the app:
  * UA = VLC/3.0.20 LibVLC/3.0.20 (+ per-channel #EXTVLCOPT user-agent/referrer when present),
    follow redirects, ~6-8s timeouts, validate TLS (the probe uses the plain client, not the
    insecure-TLS playback opt-in).
  * Non-.m3u8 (raw/progressive): GET Range 0-1 → 2xx REACHABLE / 404,410 DEAD / else UNREACHABLE.
  * .m3u8 (HLS): GET, need 2xx + '#EXTM3U'; '#EXTINF' => REACHABLE (media);
    no '#EXT-X-STREAM-INF' => DEAD; else follow the first variant and require '#EXTINF'.
  * UNREACHABLE = couldn't determine (timeout/refused/403/5xx) — NOT counted as valid or dead.

"Valid link" = REACHABLE (reachable == 1, what "Hide unavailable" keeps). Probes the full catalog
index (index.m3u). Output: out/valid-<GEO_LABEL>.json  {label, universe, counts, reachable[]}.
"""
import concurrent.futures as cf
import json
import os
import ssl
import urllib.error
import urllib.request
from urllib.parse import urljoin

UA = "VLC/3.0.20 LibVLC/3.0.20"
INDEX_URL = "https://iptv-org.github.io/iptv/index.m3u"
LABEL = os.environ.get("GEO_LABEL", "run")
WORKERS = int(os.environ.get("PROBE_WORKERS", "64"))
TIMEOUT = 8
MAX_BODY = 512 * 1024
CTX = ssl.create_default_context()


def _open(url, ua, ref, range_=False):
    req = urllib.request.Request(url, headers={"User-Agent": ua or UA})
    if range_:
        req.add_header("Range", "bytes=0-1")
    if ref:
        req.add_header("Referer", ref)
    return urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX)


def _status(url, ua, ref):
    try:
        with _open(url, ua, ref, range_=True) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def _fetch(url, ua, ref):
    try:
        with _open(url, ua, ref, range_=False) as r:
            code = r.status
            body = r.read(MAX_BODY).decode("utf-8", "ignore") if 200 <= code < 300 else None
            return code, body
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return None, None


def _first_variant(manifest, manifest_url):
    for ln in manifest.splitlines():
        s = ln.strip()
        if s and not s.startswith("#"):
            return urljoin(manifest_url, s)
    return None


def _classify(code):
    if code is None:
        return "UNREACHABLE"
    if 200 <= code < 300:
        return "REACHABLE"
    if code in (404, 410):
        return "DEAD"
    return "UNREACHABLE"


def probe(url, ua, ref):
    try:
        if not url.split("?", 1)[0].lower().endswith(".m3u8"):
            return _classify(_status(url, ua, ref))
        code, body = _fetch(url, ua, ref)
        if code is None:
            return "UNREACHABLE"
        if code in (404, 410):
            return "DEAD"
        if not (200 <= code < 300):
            return "UNREACHABLE"
        if body is None or "#EXTM3U" not in body:
            return "DEAD"
        if "#EXTINF" in body:
            return "REACHABLE"
        if "#EXT-X-STREAM-INF" not in body:
            return "DEAD"
        variant = _first_variant(body, url)
        if not variant:
            return "DEAD"
        vcode, vbody = _fetch(variant, ua, ref)
        if vcode is None:
            return "UNREACHABLE"
        if vcode in (404, 410):
            return "DEAD"
        if not (200 <= vcode < 300):
            return "UNREACHABLE"
        return "REACHABLE" if (vbody and "#EXTINF" in vbody) else "DEAD"
    except Exception:
        return "UNREACHABLE"


def parse_m3u(text):
    ua = ref = None
    seen = set()
    items = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#EXTINF"):
            ua = ref = None
        elif s.startswith("#EXTVLCOPT:http-user-agent="):
            ua = s.split("=", 1)[1]
        elif s.startswith("#EXTVLCOPT:http-referrer="):
            ref = s.split("=", 1)[1]
        elif not s.startswith("#"):
            if s not in seen:
                seen.add(s)
                items.append((s, ua, ref))
            ua = ref = None
    return items


def main():
    os.makedirs("out", exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(INDEX_URL, headers={"User-Agent": UA}), timeout=60) as r:
        items = parse_m3u(r.read().decode("utf-8", "ignore"))
    print(f"[{LABEL}] universe: {len(items)} unique links; probing with {WORKERS} workers...")

    counts = {"REACHABLE": 0, "DEAD": 0, "UNREACHABLE": 0}
    reachable = []
    done = 0
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(probe, u, ua, ref): u for (u, ua, ref) in items}
        for fut in cf.as_completed(futs):
            u = futs[fut]
            out = fut.result()
            counts[out] += 1
            if out == "REACHABLE":
                reachable.append(u)
            done += 1
            if done % 1000 == 0:
                print(f"[{LABEL}] {done}/{len(items)}  {counts}")

    report = {"label": LABEL, "universe": len(items), "counts": counts, "reachable": sorted(reachable)}
    path = f"out/valid-{LABEL}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False)
    print(f"[{LABEL}] DONE {counts} -> {path}")


if __name__ == "__main__":
    main()
