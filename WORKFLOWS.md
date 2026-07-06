# Workflows — technical reference & data flow

This repo is the **runtime data backend** for the private IPTV Android app. It contains **no app
code** — only two scheduled GitHub Actions that regenerate the data the app fetches at runtime, plus
the files they publish. Everything runs **free** (public repos have no Actions minute limit).

Two independent workflows produce two independent artifacts:

| Workflow | Produces | Published to | App reads it from |
|---|---|---|---|
| [`epg.yml`](.github/workflows/epg.yml) — *Generate EPG* | Per-country XMLTV guides `guide/<cc>.xml.gz` + `guide/index.json` | **`gh-pages`** branch | `raw.githubusercontent.com/…/gh-pages/guide/` |
| [`sources.yml`](.github/workflows/sources.yml) — *Refresh sources.json* | `sources.json` (the browse-menu registry, ~1296 groups) | **`main`** branch | `raw.githubusercontent.com/…/main/sources.json` |

Both are **decoupled**: EPG runs for hours; sources runs in ~1 minute. Neither blocks the other.

---

## 1. Serving model & the two-repo contract

Files are served straight off the branch via **`raw.githubusercontent.com`** — *not* GitHub Pages:

```
sources.json → https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/main/sources.json
EPG guides   → https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide/<cc>.xml.gz
             + https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide/index.json
```

These exact URLs are compiled into the app as `BuildConfig.DEFAULT_SOURCES_URL` and
`BuildConfig.DEFAULT_EPG_BASE_URL`. **The app never hard-depends on them** — every fetch falls back
to a cached copy and then to a bundled asset, so a failed workflow run or an unreachable CDN never
breaks the app (it just serves slightly staler data). See the app repo's
`docs/DATA_SOURCES.md` for the consumer side.

### Raw serving vs GitHub Pages (the "pages build and deployment" job)

`raw.githubusercontent.com` serves any file from any branch directly — no site root, no build step.
This is **different** from the GitHub Pages (`*.github.io`) site:

- If GitHub **Pages is enabled** on this repo with `gh-pages` as its source, GitHub auto-injects a
  built-in workflow named **"pages build and deployment"** (`pages-build-deployment`) that runs on
  **every push to `gh-pages`** (i.e. every EPG publish) to deploy the branch to the `github.io` site.
- **That job is not one of ours** (it isn't in `.github/workflows/`) and **the app does not use it** —
  the app reads the `guide/` files over `raw.githubusercontent.com`, which works regardless of Pages.
- So the Pages job is **harmless but redundant**. If a Pages build fails, the app is unaffected. To
  silence it, disable Pages (repo **Settings → Pages → Source: None**); the app keeps working.

> Because `epg.yml` publishes with `force_orphan: true` (see below), each run replaces the whole
> `gh-pages` branch — every daily publish therefore re-triggers the built-in Pages job if Pages is on.

---

## 2. `epg.yml` — Generate EPG

### What & why sharded

Regenerates a TV guide from **[iptv-org/epg](https://github.com/iptv-org/epg)** (all ~248 "sites";
scraped guides for ~157k channels / ~2.5M programmes) and publishes it split into **per-country
gzip files**.

The iptv-org grabber **buffers the entire result in memory** and writes its output file only once at
the very end (no streaming). One process grabbing all sites **OOMs** (~7 GB at ~14% of the channel
grabs, exit 134) and would blow GitHub's **6-hour per-job** limit. Two-level parallelism solves both:

- **20 parallel matrix shards** → throughput (each shard well under 6 h; free tier allows 20
  concurrent jobs).
- **one site per process within a shard** → peak memory is bounded by the *single largest site*, not
  the sum of a shard's sites (each site's buffer is freed when its process exits).

A site that OOMs/errors loses **only that site** (logged as a warning), never the shard.

### Triggers, concurrency, permissions

```yaml
on:
  schedule: [{ cron: '0 21 * * *' }]   # daily 21:00 UTC = 02:00 PKT
  workflow_dispatch: {}                # manual "Run workflow" button
permissions: { contents: write }       # publish to gh-pages
concurrency: { group: epg, cancel-in-progress: true }
```

`concurrency: cancel-in-progress` means a manual run supersedes an in-flight scheduled run.

### Job A — `grab` (20-way matrix)

```
runs-on: ubuntu-latest   timeout-minutes: 350   strategy.fail-fast: false   max-parallel: 20
matrix.shard: [0..19]
```

Per shard:
1. **Fresh clone** `iptv-org/epg@master` (`actions/checkout@v7`, `fetch-depth: 1`) — runners are
   ephemeral, so every run picks up upstream site/channel changes.
2. **Node 22** (`actions/setup-node@v6`, `cache: npm`) → `npm install`.
3. **Grab this shard's sites, one process each**, with `NODE_OPTIONS=--max-old-space-size=13312`
   (~13 GB headroom for the largest single site on the 16 GB runner):
   ```bash
   sites=$(ls sites | awk -v n=20 -v s=${{ matrix.shard }} 'NR % n == s')   # round-robin by sorted position
   for site in $sites; do
     npm run grab --- --sites="$site" --maxConnections=20 --days=1 --timeout=20000 --output="out/$site.xml"
     # runs inside `if …` so `set -e` can't abort the loop; grabber writes a file only on success,
     # so a crash leaves no file and we skip just that site.
   done
   ```
   > Note the **triple dash** `npm run grab ---` (npm strips one `--`, leaving `-- …` for the script).
4. **Upload** `out/` as artifact `guide-<shard>` (`actions/upload-artifact@v7`, `retention-days: 1`,
   `if-no-files-found: ignore` — a fully-failed shard uploads nothing and merge tolerates it).

Round-robin (`NR % 20`) balances the **number of sites** per shard; the per-site process bounds
memory, so an uneven channel distribution can't OOM a shard. **The matrix length and the awk modulus
(`n=20`) must stay in sync.**

### Job B — `merge` (download → split → validate → publish)

```yaml
needs: grab
if: ${{ !cancelled() }}   # run even if some shards failed → partial coverage still publishes
timeout-minutes: 30
```

1. **Download** all `guide-*` artifacts (`actions/download-artifact@v8`) into `parts/guide-<n>/<site>.xml`.
2. **Split-merge** (inline Python, streaming `xml.etree.iterparse` so memory stays flat):
   - **Global channel-id dedup** — a channel id maps to exactly one country; duplicates across sites
     are dropped.
   - **Country bucketing** via `cc_of(id)`: text after the last `.` (before any `@feed` suffix),
     lowercased, alphanumerics only; no dotted suffix → the **`other`** bucket. **This must match the
     app's `epgCountryCode()`** or guides won't attach. (e.g. `GeoNews.pk@SD` → `pk`.)
   - Each country is streamed into its own `public/guide/<cc>.xml.gz` as it's parsed.
3. **Carry-forward** (protects coverage against partial shard failure): fetch the previously-published
   `guide/index.json`; for any country present last run (channels > 0) but **missing this run**,
   re-download its last-good `<cc>.xml.gz` from `gh-pages` and keep it. Needed because `force_orphan`
   replaces the *whole* branch — without this, a country a shard failed to produce would vanish.
4. **Write `index.json`**: `{ totalChannels, totalProgrammes, countries: { <cc>: {channels, programmes, file} } }`.
5. **Safety floors** — refuse to publish (exit 1, keeps the last good guide) if:
   - `total_channels < ABS_FLOOR` (**1000**) → catastrophic failure, or
   - `total_channels < REL_FLOOR × previous_total` (**0.5**) → likely a partial shard failure.
6. **Publish** to `gh-pages` (`peaceiris/actions-gh-pages@v4`):
   ```yaml
   personal_token: ${{ secrets.IPTVPAT }}   # NOT GITHUB_TOKEN — see §5
   publish_dir: ./public
   force_orphan: true                       # single clean commit, no history bloat
   ```

### Why per-country split

The old design published one ~120 MB all-sites `guide.xml.gz` as a **GitHub Release asset** (Release
assets allow ≤ 2 GB). It was moved to **per-country files on `gh-pages`** so the app fetches only the
countries a user actually watches (on demand, TTL-cached). `gh-pages` uses `git push`, which has a
**hard 100 MB per-file limit** — each per-country `.gz` is far under that, so branch publishing works.
The app requests `guide/<cc>.xml.gz` lazily per country (12 h TTL) instead of one giant download.

### Coverage caveats

Even grabbing all sites, many **geo-block / rate-limit GitHub's US-based runner (HTTP 403)**, so
their channels return nothing. Coverage is "whatever the sites give a US IP." India comes through
well; **Pakistani EPG is thin at the source** (~11 channels across all of iptv-org/epg). For a
leaner/faster guide, replace the round-robin `ls sites | awk …` with a fixed
`--sites=tataplay.com,dishtv.in,…` list (site names: iptv-org/epg `SITES.md`).

### Failure modes (why a bad run never clobbers the good guide)

- `fail-fast: false` → one shard failing doesn't cancel the others.
- `merge` runs `if: !cancelled()` → publishes partial coverage rather than nothing.
- `ABS_FLOOR` / `REL_FLOOR` → a degraded merge **exits 1 and publishes nothing**, leaving the
  previous `gh-pages` guide intact.
- Carry-forward → a country a shard missed keeps its last-good file.

---

## 3. `sources.yml` — Refresh sources.json

Regenerates **`sources.json`** — the app's browse-menu registry (iptv-org countries / categories /
languages / regions / subdivisions / cities + index playlists) — and commits it to `main` only when
it changes. The app fetches it via conditional GET (ETag) and falls back to its bundled copy, so the
menu stays current without an app update.

```yaml
on:
  schedule: [{ cron: '15 21 * * *' }]   # daily 21:15 UTC = 02:15 PKT (just after EPG)
  workflow_dispatch: {}
permissions: { contents: write }
concurrency: { group: sources, cancel-in-progress: true }
```

Steps (`runs-on: ubuntu-latest`, `timeout-minutes: 15`):
1. **Checkout with `token: ${{ secrets.IPTVPAT }}`** (not `GITHUB_TOKEN` — keep-alive, see §5).
2. `python3 tools/gen-sources.py` → regenerates `sources.json`.
3. **Conditional commit**: `git diff --quiet -- sources.json`; if changed, commit as
   `MuhammadTalhaBaloch <…@users.noreply.github.com>` with message
   `chore: refresh sources.json (iptv-org browse registry)` and `git push`. No change → no commit.

### `tools/gen-sources.py`

Builds `sources.json` from iptv-org's current data using **two hosts**:

- **Playlist tree** — `https://api.github.com/repos/iptv-org/iptv/git/trees/gh-pages?recursive=1`
  (GitHub tree API). Extracts every `.m3u` path; **aborts if the tree is `truncated`** (guards
  against a partial API response).
- **Display-name maps** — `https://iptv-org.github.io/api/{categories,countries,languages,regions,subdivisions,cities}.json`
  (iptv-org API host). Turns a code (`animation`) into a display name (`Animation`), falling back to
  `code.upper()`.

Output structure:
```json
{
  "baseUrl": "https://iptv-org.github.io/iptv",
  "note": "auto-generated header",
  "counts": { "index": 4, "category": 31, "country": 187, "language": 203,
              "region": 42, "subdivision": 353, "city": 476 },
  "sources": [ { "type": "...", "name": "...", "code": "...", "url": "..." }, … ]
}
```

- **4 fixed index entries** (All Channels / Category / Language / Country index playlists) + one
  entry per `.m3u`. Current total = **1296** (4 + 31 + 187 + 203 + 42 + 353 + 476).
- **Validation guard**: aborts if it would emit **< 500** sources (protects against an upstream fetch
  failure producing a near-empty registry — the app also independently re-validates `>= 500` before
  accepting a fetched registry).

---

## 4. End-to-end flow

```
                          iptv-org/epg (master)                 iptv-org tree API + iptv-org/api
                                  │                                        │
        ┌──── epg.yml (daily 21:00 UTC) ────┐            ┌── sources.yml (daily 21:15 UTC) ──┐
        │                                    │            │                                   │
   grab: 20 shards × (1 site/process)        │        python3 tools/gen-sources.py            │
        │  fail-fast:false, skip bad sites   │            │  (abort if tree truncated / <500) │
        ▼                                    │            ▼                                   │
   merge: dedup ids → cc_of() buckets ───────┘        sources.json changed? ──no──▶ (nothing) │
        │  carry-forward last-good                        │ yes                               │
        │  floors: ABS_FLOOR=1000, REL_FLOOR=0.5          ▼                                   │
        ▼  (exit 1 = keep last good guide)          git commit + push (IPTVPAT) ──────────────┘
   peaceiris force_orphan → gh-pages/guide/*.xml.gz + index.json     → main/sources.json
        │                                                                    │
        ▼ raw.githubusercontent.com/.../gh-pages/guide/<cc>.xml.gz           ▼ raw.githubusercontent.com/.../main/sources.json
                                   ▼                                         ▼
                         PRIVATE IPTV APP  (on-demand, TTL-cached, bundled-asset fallback)
```

---

## 5. Secrets, keep-alive & requirements

| Requirement | Why |
|---|---|
| Repo is **public** | Free unlimited Actions **and** public `raw.githubusercontent.com` serving. |
| Secret **`IPTVPAT`** | A Personal Access Token with **Contents: write**. Used by **both** workflows (EPG publish + sources checkout). **Deliberately a PAT, not `GITHUB_TOKEN`:** commits authored by `GITHUB_TOKEN` **don't count as repository activity**, so GitHub would auto-disable a scheduled workflow after **60 days** of no other activity. A PAT-authored push **does** count, so the daily runs keep the scheduler alive indefinitely. **If the PAT expires, regenerate it and update the secret** or both workflows silently stop running. |

No GitHub Pages configuration is required for the app to work (raw serving is independent).

---

## 6. Tuning knobs (all in the workflow files)

- **Shard count** — `matrix.shard` length **and** the awk `n=` modulus in `epg.yml` (must match). More
  shards = faster wall-clock.
- **Guide breadth** — replace the round-robin `ls sites | awk …` with a fixed `--sites=` list for a
  smaller/faster guide.
- **Days of guide** — `--days=1` in the grab command.
- **Per-site memory** — `NODE_OPTIONS=--max-old-space-size` (caps one site's buffer).
- **Publish safety** — `ABS_FLOOR` / `REL_FLOOR` in the merge script.
- **Schedules** — the two `cron:` lines (UTC).

---

## 7. Repo contents

- [`.github/workflows/epg.yml`](.github/workflows/epg.yml) — daily per-country EPG generator (§2).
- [`.github/workflows/sources.yml`](.github/workflows/sources.yml) — daily `sources.json` refresh (§3).
- [`tools/gen-sources.py`](tools/gen-sources.py) — the registry generator (§3).
- `sources.json` — generated browse registry (on `main`).
- `guide/<cc>.xml.gz` + `guide/index.json` — generated EPG (on the `gh-pages` branch).
- [`README.md`](README.md) / [`EPG.md`](EPG.md) — overviews.
- Other `*.md` — unrelated IPTV source-research notes.
