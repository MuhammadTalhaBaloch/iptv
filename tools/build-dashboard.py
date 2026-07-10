#!/usr/bin/env python3
"""Regenerate the "Workflow Dashboard" block in README.md.

Run by dashboard.yml after ANY workflow completes (single writer — no push races). For each
workflow it shows the last run's time + conclusion (from the GitHub Actions API) and that
workflow's key metrics (from the committed data files / published guide index):
  * Generate EPG              -> channels / programmes / countries (gh-pages guide/index.json)
  * Refresh browse registry   -> group counts (sources.json) + country->region map size
  * Publish channel availability -> catalog probed / available / dead / unreachable (availability.json)
  * Compare sources vs index  -> last-run status (diff is a run artifact)
"""
import datetime
import json
import os
import re
import urllib.request

REPO = "MuhammadTalhaBaloch/iptv"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
RAW = f"https://raw.githubusercontent.com/{REPO}"
EMOJI = {"success": "✅", "failure": "❌", "cancelled": "⚪", "startup_failure": "❌", "timed_out": "⏱"}


def _api(path):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}{path}",
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json", "User-Agent": "dashboard"},
    )
    return json.load(urllib.request.urlopen(req, timeout=30))


def _raw_json(path):
    try:
        with urllib.request.urlopen(f"{RAW}/{path}", timeout=30) as r:
            return json.load(r)
    except Exception:
        return None


def _local(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _fmt(iso):
    if not iso:
        return "—"
    try:
        return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return iso


def _n(x):
    return f"{x:,}" if isinstance(x, int) else (str(x) if x is not None else "—")


def last_run(workflow_file):
    try:
        runs = _api(f"/actions/workflows/{workflow_file}/runs?per_page=1").get("workflow_runs", [])
        if not runs:
            return None
        r = runs[0]
        return {
            "conclusion": r.get("conclusion") or r.get("status"),
            "started": r.get("run_started_at"),
            "url": r.get("html_url"),
            "number": r.get("run_number"),
        }
    except Exception:
        return None


def status_line(run):
    if not run:
        return "_never run_"
    e = EMOJI.get(run["conclusion"], "•")
    return f"{e} **{run['conclusion']}** · last run [#{run['number']}]({run['url']}) at {_fmt(run['started'])}"


def table(rows):
    rows = [r for r in rows if r]
    if not rows:
        return "_no data yet_"
    return "| Metric | Value |\n|---|---|\n" + "\n".join(f"| {k} | {v} |" for k, v in rows)


def build():
    blocks = []

    # EPG
    idx = _raw_json("gh-pages/guide/index.json")
    epg_rows = []
    if idx:
        epg_rows = [
            ("Channels", _n(idx.get("totalChannels"))),
            ("Programmes", _n(idx.get("totalProgrammes"))),
            ("Countries", _n(len(idx.get("countries", {})))),
        ]
    blocks.append(f"### 📺 EPG — `Generate EPG`\n\n{status_line(last_run('epg.yml'))}\n\n{table(epg_rows)}")

    # Source registry
    sj, cr = _local("sources.json"), _local("country_regions.json")
    src_rows = []
    if sj:
        counts = sj.get("counts", {})
        src_rows.append(("Total browse groups", _n(sum(counts.values()) if counts else None)))
        for k in ("category", "country", "language", "region", "subdivision", "city", "index"):
            if k in counts:
                src_rows.append((k.capitalize(), _n(counts[k])))
    if cr is not None:
        src_rows.append(("Country→region map", f"{len(cr)} countries"))
    blocks.append(f"### 🗂 Source registry — `Refresh browse registry`\n\n{status_line(last_run('sources.yml'))}\n\n{table(src_rows)}")

    # Availability
    av = _local("availability.json")
    av_rows = []
    if av:
        c = av.get("counts", {})
        av_rows = [
            ("Catalog probed", _n(av.get("universe"))),
            ("✅ Available (reachable)", _n(av.get("count"))),
            ("❌ Dead", _n(c.get("DEAD"))),
            ("⚠️ Unreachable / couldn't reach", _n(c.get("UNREACHABLE"))),
            ("Snapshot", f"{_fmt(av.get('updatedAt'))} · {av.get('geo', '?')} probe"),
        ]
    blocks.append(f"### 📶 Availability — `Publish channel availability`\n\n{status_line(last_run('probe-availability.yml'))}\n\n{table(av_rows)}")

    # Compare (manual experiment)
    blocks.append(
        f"### 🧪 Compare sources vs index — `(manual experiment)`\n\n"
        f"{status_line(last_run('compare-sources.yml'))}\n\n_Full diff uploaded as the run artifact `sources-vs-index`._"
    )

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return (
        "## 📊 Workflow Dashboard\n\n"
        f"_Auto-updated after each workflow run — regenerated {now}._\n\n"
        + "\n\n".join(blocks)
        + "\n"
    )


def main():
    dashboard = build()
    readme = open("README.md", encoding="utf-8").read()
    start, end = "<!-- DASHBOARD:START -->", "<!-- DASHBOARD:END -->"
    wrapped = f"{start}\n{dashboard}{end}"
    if start in readme and end in readme:
        readme = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: wrapped, readme, flags=re.S)
    else:
        sep = "\n---\n"
        if sep in readme:  # insert right after the intro's first horizontal rule
            i = readme.index(sep) + len(sep)
            readme = readme[:i] + "\n" + wrapped + "\n" + readme[i:]
        else:
            readme = wrapped + "\n\n" + readme
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("dashboard block written")


if __name__ == "__main__":
    main()
