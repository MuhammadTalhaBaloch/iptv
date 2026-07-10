#!/usr/bin/env python3
"""Generate country_regions.json — country name (lowercased) -> the iptv-org region names it
belongs to (a country is in several: continents + geopolitical groupings).

The app's RegionResolver uses this so "Play all Regions" can order the catalog by region priority
(it maps a channel's country -> its regions -> the best-priority one). The app fetches this from
raw.githubusercontent (ETag-cached) and falls back to its bundled copy, so region membership stays
current without an app update. Source: iptv-org's public API (same origin as sources.json's data).

Format MUST match the app's bundled asset (compact, sorted, {name_lower: [region, ...]}).
"""
import json
import urllib.request

REGIONS_URL = "https://iptv-org.github.io/api/regions.json"
COUNTRIES_URL = "https://iptv-org.github.io/api/countries.json"
OUT = "country_regions.json"


def _get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def main():
    regions = _get(REGIONS_URL)
    countries = _get(COUNTRIES_URL)
    code_to_name = {c["code"]: c["name"] for c in countries}

    by_country = {}
    for region in regions:
        name = region.get("name")
        if not name:
            continue
        for code in region.get("countries", []):
            cname = code_to_name.get(code)
            if cname:
                by_country.setdefault(cname.strip().lower(), set()).add(name)

    out = {k: sorted(v) for k, v in sorted(by_country.items())}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    print(f"wrote {OUT}: {len(out)} countries, {len(regions)} regions")


if __name__ == "__main__":
    main()
