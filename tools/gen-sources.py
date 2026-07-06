#!/usr/bin/env python3
"""Generate sources.json (the app's browse-menu registry) from iptv-org's current
playlists + API display names. Run in CI daily; the app refreshes from it (falling back
to the bundled asset if it's missing/broken)."""
import json, re, sys, urllib.request
BASE = "https://iptv-org.github.io/iptv"
API  = "https://iptv-org.github.io/api"
TREE = "https://api.github.com/repos/iptv-org/iptv/git/trees/gh-pages?recursive=1"

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "sources-gen"}), timeout=90).read()

# Global exclusions (committed → preserved across daily runs). {type: [codes]}; keys other than the
# known dimension types (e.g. "note") are ignored. Excluded items are omitted from sources.json and
# also listed under "excluded" so already-installed apps hide them on their next refresh.
def load_exclusions():
    try:
        with open("exclusions.json", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    return {k: {str(c).lower() for c in v} for k, v in data.items() if isinstance(v, list)}
EXCLUDE = load_exclusions()

tree = json.loads(get(TREE))
if tree.get("truncated"):
    print("ERROR: iptv-org tree truncated", file=sys.stderr); sys.exit(1)
paths = [t["path"] for t in tree["tree"] if t["path"].endswith(".m3u")]

maps = {
    "categories":   {x["id"]: x["name"] for x in json.loads(get(f"{API}/categories.json"))},
    "countries":    {x["code"].lower(): x["name"] for x in json.loads(get(f"{API}/countries.json"))},
    "languages":    {x["code"].lower(): x["name"] for x in json.loads(get(f"{API}/languages.json"))},
    "regions":      {x["code"].lower(): x["name"] for x in json.loads(get(f"{API}/regions.json"))},
    "subdivisions": {x["code"].lower(): x["name"] for x in json.loads(get(f"{API}/subdivisions.json"))},
    "cities":       {x["code"].lower(): x["name"] for x in json.loads(get(f"{API}/cities.json"))},
}
DIM = {"categories": "category", "countries": "country", "languages": "language",
       "regions": "region", "subdivisions": "subdivision", "cities": "city"}
INDEX = [("All Channels Index", "index.m3u"), ("Category Index", "index.category.m3u"),
         ("Language Index", "index.language.m3u"), ("Country Index", "index.country.m3u")]

sources = []
present = set(paths)
for nm, p in INDEX:
    if p in present:
        sources.append({"type": "index", "name": nm, "code": None, "url": f"{BASE}/{p}"})
for p in sorted(paths):
    m = re.match(r"([a-z]+)/(.+)\.m3u$", p)
    if not m:
        continue
    dim, code = m.group(1), m.group(2)
    if dim not in DIM:
        continue
    if code.lower() in EXCLUDE.get(DIM[dim], set()):
        continue   # globally hidden (see exclusions.json)
    name = maps[dim].get(code.lower()) or code.upper()
    sources.append({"type": DIM[dim], "name": name, "code": code, "url": f"{BASE}/{p}"})

from collections import Counter
counts = dict(Counter(s["type"] for s in sources))
# "type:code" keys the app matches to hide already-seeded items too (see exclusions.json).
excluded_keys = sorted(f"{typ}:{code}" for typ, codes in EXCLUDE.items() for code in codes)
out = {"baseUrl": BASE,
       "note": "Auto-generated from iptv-org playlists + API names. Do not edit by hand.",
       "counts": counts, "excluded": excluded_keys, "sources": sources}
if len(sources) < 500:
    print(f"ERROR: only {len(sources)} sources — refusing", file=sys.stderr); sys.exit(1)
with open("sources.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("sources.json:", counts, "| total", len(sources))
