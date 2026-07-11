# Workflows — technical reference & data flow

This repo is the **runtime data backend** for the private IPTV Android app. It contains **no app
code** — only scheduled GitHub Actions that regenerate the data the app fetches at runtime, plus the
files they publish. Everything runs **free** (public repos have no Actions minute limit).

**Six workflows** — three produce data the app consumes on a schedule, two are manual/on-demand (a
source-diff experiment and the app-release publisher), one maintains the README dashboard:

| Workflow | Produces | Published to | App reads it from |
|---|---|---|---|
| [`epg.yml`](.github/workflows/epg.yml) — *Generate EPG* | Per-country XMLTV guides `guide/<cc>.xml.gz` + `guide/index.json` | **`gh-pages`** | `raw…/gh-pages/guide/` |
| [`sources.yml`](.github/workflows/sources.yml) — *Refresh browse registry* | `sources.json` (browse menu, ~1299 groups) **and** `country_regions.json` (country→region map) | **`main`** | `raw…/main/sources.json`, `raw…/main/country_regions.json` |
| [`probe-availability.yml`](.github/workflows/probe-availability.yml) — *Publish channel availability* | `availability.json` (reachable stream URLs) | **`main`** | `raw…/main/availability.json` |
| [`release-app.yml`](.github/workflows/release-app.yml) — *Publish app release manifest* | `app-release.json` (version gate / kill switch) | **`main`** | `raw…/main/app-release.json` |
| [`compare-sources.yml`](.github/workflows/compare-sources.yml) — *Compare sources vs index* | `sources-vs-index.json` (diff report) — **run artifact only** (manual experiment) | run artifact | — |
| [`dashboard.yml`](.github/workflows/dashboard.yml) — *Update dashboard* | The "Workflow Dashboard" block in [`README.md`](README.md) | **`main`** | (humans) |

The three data workflows are **decoupled**: EPG runs for hours; sources runs in ~1 min; availability
runs ~30–40 min after sources. `dashboard.yml` runs after any of them finishes.

---

## 1. Serving model & the two-repo contract

Files are served straight off the branch via **`raw.githubusercontent.com`** — *not* GitHub Pages:

```
sources.json         → https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/main/sources.json
country_regions.json → https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/main/country_regions.json
availability.json    → https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/main/availability.json
EPG guides           → https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide/<cc>.xml.gz
                     + https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide/index.json
```

These URLs are compiled into the app as `BuildConfig.DEFAULT_SOURCES_URL`, `DEFAULT_REGIONS_URL`,
`DEFAULT_AVAILABILITY_URL`, and `DEFAULT_EPG_BASE_URL`. **The app never hard-depends on them** — every
fetch is ETag-cached and falls back to a bundled asset, so a failed run or an unreachable CDN never
breaks the app (it just serves slightly staler data). See the app repo's `docs/DATA_SOURCES.md`.

### Raw serving vs GitHub Pages (the "pages build and deployment" job)

`raw.githubusercontent.com` serves any file from any branch directly — no site root, no build step.
This is **different** from the GitHub Pages (`*.github.io`) site:

- If Pages is **enabled** with `gh-pages` as its source, GitHub auto-injects a built-in workflow
  **"pages build and deployment"** (`pages-build-deployment`) that runs on **every push to `gh-pages`**
  (every EPG publish) to deploy the branch to the `github.io` site.
- **That job is not one of ours** and **the app doesn't use it** — the app reads `guide/` over
  `raw.githubusercontent.com`, which works regardless of Pages. It's **harmless but redundant**; to
  silence it, disable Pages (**Settings → Pages → Source: None**).

> `epg.yml` publishes with `force_orphan: true`, so each run replaces the whole `gh-pages` branch —
> every daily publish re-triggers the built-in Pages job if Pages is on.

---

## 2. `epg.yml` — Generate EPG

### What & why sharded

Regenerates a TV guide from **[iptv-org/epg](https://github.com/iptv-org/epg)** (all ~248 "sites";
scraped guides for ~150k channels / ~2.4M programmes) and publishes it split into **per-country gzip
files**.

The iptv-org grabber **buffers the entire result in memory** and writes its file only at the very end
(no streaming). One process grabbing all sites **OOMs** and would blow GitHub's **6-hour per-job**
limit. Two-level parallelism solves both:

- **20 parallel matrix shards** → throughput (each shard well under 6 h).
- **one site per process within a shard** → peak memory is bounded by the *single largest site*.

A site that OOMs/errors/times-out loses **only that site** (logged), never the shard.

### Triggers, concurrency, permissions

```yaml
on:
  schedule: [{ cron: '0 21 * * *' }]   # daily 21:00 UTC = 02:00 PKT
  workflow_dispatch: {}
permissions: { contents: write }
concurrency: { group: epg, cancel-in-progress: true }
```

### Job A — `grab` (20-way matrix)

`runs-on: ubuntu-latest`, `timeout-minutes: 350`, `fail-fast: false`, `max-parallel: 20`,
`matrix.shard: [0..19]`. Per shard:

1. **Fresh clone** `iptv-org/epg@master` (ephemeral runners always pick up upstream changes).
2. **Node 22** → `npm install`.
3. **Assign sites by CHANNEL COUNT, then grab each in its own process**, with
   `NODE_OPTIONS=--max-old-space-size=13312` (~13 GB for the largest single site):
   ```bash
   # Greedy longest-processing-time bin-pack over channel counts (embedded Python), NOT round-robin.
   # A giant site (e.g. dstv.com ~3k channels / 48 feeds, plex.tv ~1.3k) must not pile onto one shard.
   SHARD=${{ matrix.shard }} python3 - <<'PY' > shard_sites.txt … PY
   sites=$(cat shard_sites.txt)
   for site in $sites; do
     timeout -k 60s 90m npm run grab --- --sites="$site" --maxConnections=20 --days=1 --timeout=20000 --output="out/$site.xml"
     # inside `if …` so `set -e` can't abort the loop; grabber writes a file only on success.
   done
   ```
   - **Channel-count bin-pack** (not `NR % 20`): balances *channel load* across shards so no shard
     inherits a giant site's whole load. Deterministic — every shard runs the same pack and picks its
     own bin. **Keep the matrix length and `N` in the pack script in sync.**
   - **Per-site `timeout -k 60s 90m`**: a slow/hung/giant site is SIGTERM'd (SIGKILL 60 s later) and
     skipped like any other failure — so one site can never monopolise a shard for hours or get the
     runner OOM-killed. (This replaced an earlier round-robin scheme where a single shard once ground
     for 5 h+ on dstv.com and was cancelled.)
   - **Triple dash** `npm run grab ---` (npm strips one `--`, leaving `-- …` for the script).
4. **Upload** `out/` as artifact `guide-<shard>` (`retention-days: 1`, `if-no-files-found: ignore`).

### Job B — `merge` (download → split → validate → publish)

`needs: grab`, `if: !cancelled()` (partial coverage still publishes), `timeout-minutes: 30`.

1. **Download** all `guide-*` artifacts into `parts/guide-<n>/<site>.xml`.
2. **Split-merge** (streaming `xml.etree.iterparse`, memory flat): global channel-id **dedup**;
   **country bucketing** via `cc_of(id)` = text after the last `.` (before any `@feed`), lowercased,
   alphanumerics only; no dotted suffix → **`other`**. **This must match the app's `epgCountryCode()`**
   (e.g. `GeoNews.pk@SD` → `pk`). Each country streams into `public/guide/<cc>.xml.gz`.
3. **Carry-forward**: fetch the previous `guide/index.json`; for any country present last run but
   **missing this run**, re-download its last-good `<cc>.xml.gz` and keep it (because `force_orphan`
   replaces the whole branch).
4. **Write `index.json`**: `{ totalChannels, totalProgrammes, countries: { <cc>: {channels, programmes, file} } }`.
5. **Safety floors** — refuse to publish (exit 1, keep last good guide) if `total_channels < ABS_FLOOR`
   (**1000**) or `< REL_FLOOR × previous` (**0.5**).
6. **Publish** to `gh-pages` (`peaceiris/actions-gh-pages@v4`, `personal_token: IPTVPAT`,
   `force_orphan: true`).

### Coverage caveats

Many sites **geo-block/rate-limit GitHub's US runner (403)**, so coverage is "whatever the sites give
a US IP." India comes through well; **Pakistani EPG is thin at the source** (~11 channels).

---

## 3. `sources.yml` — Refresh browse registry

Regenerates the app's browse-registry data and commits it to `main` **only when it changes**. Two
files, two generators, one commit:

- **`sources.json`** ← `python3 tools/gen-sources.py` — the browse menu (countries / categories /
  languages / regions / subdivisions / cities + index playlists, ~1299 groups).
- **`country_regions.json`** ← `python3 tools/gen-country-regions.py` — country name → the iptv-org
  region names it belongs to (a country is in several). Powers the app's **"Play all Regions"**
  ordering (the catalog index has no region column, so the app maps a channel's country → its regions
  → the best-priority one). Built from iptv-org's `regions.json` + `countries.json`.

```yaml
on:
  schedule: [{ cron: '15 21 * * *' }]   # daily 21:15 UTC = 02:15 PKT (just after EPG)
  workflow_dispatch: {}
permissions: { contents: write }
concurrency: { group: sources, cancel-in-progress: true }
```

Steps (`ubuntu-latest`, `timeout-minutes: 15`): checkout with **`IPTVPAT`** → run both generators →
**conditional commit** of `sources.json` + `country_regions.json` if either changed
(`chore: refresh browse registry (…)`).

### `tools/gen-sources.py`

Builds `sources.json` from iptv-org via **two hosts**: the **playlist tree**
(`api.github.com/.../iptv/git/trees/gh-pages?recursive=1` — aborts if `truncated`) and the
**display-name maps** (`iptv-org.github.io/api/{categories,countries,…}.json`). Output:
`{ baseUrl, note, counts:{index,category,country,language,region,subdivision,city}, excluded, sources:[…] }`.
**Validation guard**: aborts if it would emit **< 500** sources (the app also re-validates `>= 500`).

### `tools/gen-country-regions.py`

Fetches iptv-org `api/regions.json` + `api/countries.json`, inverts to `{ "<country name lower>":
["<region>", …] }` (compact, sorted). Format **must match** the app's bundled
`assets/country_regions.json` fallback.

### Global exclusions (`exclusions.json`)

Hide browse items **globally**. [`exclusions.json`](exclusions.json) is committed → preserved across
runs; keyed by type → iptv-org codes (`{ "category": ["xxx"], … }`). `gen-sources.py` **omits** them
from `sources.json` **and** emits an `"excluded": ["type:code", …]` array (new installs never see
them; existing installs hide them on next refresh). Keep the output **≥ 500** or the guard fails.

---

## 4. `probe-availability.yml` — Publish channel availability

Runs the app's **Deep-Refresh reachability probe** (faithfully replicated in
[`tools/probe-availability.py`](tools/probe-availability.py)) over the whole catalog index and commits
**`availability.json`** = `{ updatedAt, geo, universe, counts:{REACHABLE,DEAD,UNREACHABLE}, count,
reachable:[<stream url>, …] }`.

**Why:** the app fetches this (ETag-cached) and marks a channel available iff its stream URL is in the
set — an instant **"Hide unavailable"** baseline so users get a working, filtered catalog **without
each running a slow on-device Deep Refresh or downloading the whole catalog**. On-device recheck stays
as an on-demand per-user refinement.

```yaml
on:
  workflow_run: { workflows: ["Refresh browse registry"], types: [completed] }   # right after sources
  workflow_dispatch: {}
permissions: { contents: write }
concurrency: { group: availability, cancel-in-progress: true }
```

Steps (`ubuntu-latest`, `timeout-minutes: 90`): checkout with **`IPTVPAT`** →
`python3 tools/probe-availability.py` (probes ~13k index links, 64 workers, VLC UA + per-channel
`#EXTVLCOPT` headers, ~6–8 s timeouts, HLS master→variant chain requiring real `#EXTINF`) →
conditional commit of `availability.json`.

**Probe outcomes** mirror the app's `StreamProbe`: `REACHABLE` / `DEAD` (404/410 or 2xx-not-a-playlist)
/ `UNREACHABLE` (timeout/refused/403/5xx — *not* counted as dead). Only `REACHABLE` goes in `reachable`.

> **GEO CAVEAT:** probed from the GitHub runner (**US**), so it reflects US reachability. ~3 % of
> channels differ for other geos (e.g. Pakistan) — the app's on-device recheck corrects that per user,
> and the baseline never downgrades (it can only add reachable). Snapshot only — streams flap, so the
> set shifts run-to-run.

---

## 5. `compare-sources.yml` — Compare sources vs index (manual experiment)

**Manual only** (`workflow_dispatch`). [`tools/compare-sources.py`](tools/compare-sources.py) fetches
every source playlist in `sources.json`, dedups the stream links, and diffs the two channel paths:
the flat catalog **index** (`index.m3u`, what Search/Play-all use) vs the union of the **per-dimension
browse playlists**. Reports which links are in one path but not the other; uploads
`out/sources-vs-index.json` as the run artifact **`sources-vs-index`** (not committed). A data-integrity
check — expected result is near-identical sets.

---

## 6. `release-app.yml` — Publish app release manifest (manual)

**Manual only** (`workflow_dispatch`). Regenerates [`app-release.json`](app-release.json) — the app's
**version gate / kill switch**. The Android app fetches it on startup (ETag-cached, **fail-open**) and
compares its own `versionCode`:

- in `blockedVersionCodes` **or** `< minSupportedVersionCode` → blocking **"update required"** screen (shown before the login gate);
- `< latestVersionCode` → dismissible **"update available"** nudge on Home;
- otherwise → up to date. Unreachable/unparseable manifest never blocks a working app.

**Release runbook**: build the signed APK locally → upload it to this repo's **Releases** → run this
workflow. Inputs: `versionCode`, `versionName`, `minSupportedVersionCode` (the force knob),
`downloadUrl` (blank = Releases page), `blockedVersionCodes`, and the two messages.
[`tools/gen-app-release.py`](tools/gen-app-release.py) validates them (rejects `min > version`, warns on
a non-monotonic `versionCode`) and writes the file; the commit step uses the same rebase-and-retry push
guard as the data workflows.

**Control matrix** — all just inputs to this workflow, no app rebuild:

| Goal | Set |
|---|---|
| Ship an update, keep old versions working | bump `versionCode`/`versionName` + `downloadUrl`; leave `minSupportedVersionCode` low |
| Force everyone off old versions | set `minSupportedVersionCode` = the new `versionCode` |
| Kill one bad build | add its code to `blockedVersionCodes` |

Not tracked by the dashboard (it's manual + rare; `build-dashboard.py` covers the scheduled data
workflows).

---

## 7. `dashboard.yml` — Update dashboard

Keeps the **"📊 Workflow Dashboard"** block in [`README.md`](README.md) current.

```yaml
on:
  workflow_run: { workflows: ["Generate EPG", "Refresh browse registry", "Publish channel availability"], types: [completed] }
  workflow_dispatch: {}
permissions: { contents: write, actions: read }
concurrency: { group: dashboard, cancel-in-progress: false }
```

After **any** data workflow finishes, [`tools/build-dashboard.py`](tools/build-dashboard.py) reads each
workflow's last run (Actions API — conclusion + time + link) and its metrics (from the committed data
files + the published `guide/index.json`), and regenerates the dashboard block between the
`<!-- DASHBOARD:START/END -->` markers, then commits `README.md` if it changed.

**Single writer** — no other workflow touches `README.md`, so there are no push races. (Having each
workflow self-edit the README was rejected: the EPG job doesn't even check out *this* repo, and
concurrent edits would race.) `cancel-in-progress: false` lets each trigger's update apply; the commit
step `git pull --rebase` before push in case a data workflow committed meanwhile (different files).

---

## 8. End-to-end flow

```
   iptv-org/epg (master)         iptv-org tree API + api/*.json           iptv-org/iptv index.m3u
          │                                │                                       │
  epg.yml (21:00 UTC)          sources.yml (21:15 UTC)              probe-availability.yml
  grab: 20 shards, bin-packed  gen-sources.py  → sources.json       (workflow_run after sources)
  by channel count, per-site   gen-country-regions.py               probe ~13k links (US runner)
  `timeout 90m`, skip bad      → country_regions.json                     │
          │                          │ commit if changed                  ▼  commit availability.json
  merge: dedup → cc_of()             ▼  (IPTVPAT → main)             ┌──────┘
  carry-forward, floors        main/sources.json                    │
  (exit 1 = keep last good)    main/country_regions.json            │
          ▼ peaceiris force_orphan                                  │
  gh-pages/guide/*.xml.gz + index.json                              │
          │                          │                              │
          └──────────────┬───────────┴──────────────┬──────────────┘
                         │ (any completes)           │
                  dashboard.yml (workflow_run) → README.md dashboard
                         │
          raw.githubusercontent.com  ─────────────────────────────────▶  PRIVATE IPTV APP
          (all ETag-cached, bundled-asset fallback, heavy work on-demand)
```

---

## 9. Secrets, keep-alive & requirements

| Requirement | Why |
|---|---|
| Repo is **public** | Free unlimited Actions **and** public `raw.githubusercontent.com` serving. |
| Secret **`IPTVPAT`** | A Personal Access Token with **Contents: write**. Used by **every** workflow that commits/publishes (EPG publish, sources, availability, dashboard) and for the dashboard's Actions-API reads. **Deliberately a PAT, not `GITHUB_TOKEN`:** `GITHUB_TOKEN` commits **don't count as repo activity**, so a scheduled workflow would be auto-disabled after **60 days** of inactivity. A PAT-authored push **does** count, keeping the schedulers alive. **If the PAT expires, regenerate it and update the secret** or the workflows silently stop. |

No GitHub Pages configuration is required (raw serving is independent).

---

## 10. Tuning knobs (all in the workflow files)

- **Shard count** — `matrix.shard` length **and** `N` in the bin-pack script in `epg.yml` (must match).
- **Per-site cap** — `timeout -k 60s 90m` in the grab loop (bounds one site; raise for a huge site).
- **Guide breadth / days** — the grab command (`--days=1`), or a fixed `--sites=` list.
- **Per-site memory** — `NODE_OPTIONS=--max-old-space-size`.
- **Publish safety** — `ABS_FLOOR` / `REL_FLOOR` in the merge script.
- **Availability probe** — `PROBE_WORKERS`, the timeouts in `tools/probe-availability.py`.
- **Schedules** — the `cron:` lines (UTC); availability + dashboard chain off `workflow_run`.

---

## 10. Repo contents

- [`.github/workflows/epg.yml`](.github/workflows/epg.yml) — daily per-country EPG generator (§2).
- [`.github/workflows/sources.yml`](.github/workflows/sources.yml) — daily registry refresh (§3).
- [`.github/workflows/probe-availability.yml`](.github/workflows/probe-availability.yml) — daily availability list (§4).
- [`.github/workflows/compare-sources.yml`](.github/workflows/compare-sources.yml) — manual diff experiment (§5).
- [`.github/workflows/dashboard.yml`](.github/workflows/dashboard.yml) — README dashboard updater (§6).
- [`tools/gen-sources.py`](tools/gen-sources.py) · [`tools/gen-country-regions.py`](tools/gen-country-regions.py) — registry generators (§3).
- [`tools/probe-availability.py`](tools/probe-availability.py) — availability probe (§4).
- [`tools/compare-sources.py`](tools/compare-sources.py) — sources-vs-index diff (§5).
- [`tools/build-dashboard.py`](tools/build-dashboard.py) — dashboard generator (§6).
- `sources.json` · `country_regions.json` · `availability.json` — generated data (on `main`).
- `guide/<cc>.xml.gz` + `guide/index.json` — generated EPG (on `gh-pages`).
- [`exclusions.json`](exclusions.json) — global browse-item hide list (§3).
- [`README.md`](README.md) / [`EPG.md`](EPG.md) — overviews.
- Other `*.md` — unrelated IPTV source-research notes.
