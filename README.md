# IPTV — runtime data backend (EPG + source registry)

This is the **public data backend** for the private IPTV Android app. It holds no app code — just
scheduled GitHub Actions that regenerate the data the app fetches at runtime, and the files they
publish. It stays public so Actions run **free** (no minute limit on public repos) and files are
served over `raw.githubusercontent.com`.

Self-updating datasets:

| Dataset | Workflow | Lives on | Served at |
|---|---|---|---|
| **EPG** — per-country TV guides `guide/<cc>.xml.gz` + `guide/index.json` | [`epg.yml`](.github/workflows/epg.yml) | `gh-pages` | `raw…/gh-pages/guide/` |
| **Source registry** — `sources.json` (~1299 browse groups) | [`sources.yml`](.github/workflows/sources.yml) | `main` | `raw…/main/sources.json` |
| **Region map** — `country_regions.json` (country→region, for "Play all Regions") | [`sources.yml`](.github/workflows/sources.yml) | `main` | `raw…/main/country_regions.json` |
| **Availability** — `availability.json` (reachable stream URLs, the "Hide unavailable" baseline) | [`probe-availability.yml`](.github/workflows/probe-availability.yml) | `main` | `raw…/main/availability.json` |

Plus two support workflows: [`compare-sources.yml`](.github/workflows/compare-sources.yml) (manual
sources-vs-index diff experiment) and [`dashboard.yml`](.github/workflows/dashboard.yml) (regenerates
the dashboard below after any run).

Those URLs are compiled into the app (`DEFAULT_EPG_BASE_URL`, `DEFAULT_SOURCES_URL`,
`DEFAULT_REGIONS_URL`, `DEFAULT_AVAILABILITY_URL`). **The app never hard-depends on them** — it
ETag-caches every fetch and ships bundled fallbacks, so a failed run or CDN blip only means slightly
staler data, never a broken app.

> 📖 **Full technical reference + data-flow diagrams:** [`WORKFLOWS.md`](WORKFLOWS.md).
> EPG-specific quick reference: [`EPG.md`](EPG.md).

---

<!-- DASHBOARD:START -->
## 📊 Workflow Dashboard

_Auto-updated after each workflow run — regenerated 2026-07-13 22:15 UTC._

### 📺 EPG — `Generate EPG`

• **in_progress** · last run [#19](https://github.com/MuhammadTalhaBaloch/iptv/actions/runs/29288058992) at 2026-07-13 21:54 UTC

| Metric | Value |
|---|---|
| Channels | 148,893 |
| Programmes | 2,363,942 |
| Countries | 259 |

### 🗂 Source registry — `Refresh browse registry`

✅ **success** · last run [#10](https://github.com/MuhammadTalhaBaloch/iptv/actions/runs/29288960933) at 2026-07-13 22:09 UTC

| Metric | Value |
|---|---|
| Total browse groups | 1,305 |
| Category | 30 |
| Country | 188 |
| Language | 205 |
| Region | 42 |
| Subdivision | 354 |
| City | 482 |
| Index | 4 |
| Country→region map | 250 countries |

### 📶 Availability — `Publish channel availability`

✅ **success** · last run [#9](https://github.com/MuhammadTalhaBaloch/iptv/actions/runs/29288970133) at 2026-07-13 22:10 UTC

| Metric | Value |
|---|---|
| Catalog probed | 13,450 |
| ✅ Available (reachable) | 7,385 |
| ❌ Dead | 1,798 |
| ⚠️ Unreachable / couldn't reach | 4,267 |
| Snapshot | 2026-07-13 22:15 UTC · us probe |

### 🧪 Compare sources vs index — `(manual experiment)`

✅ **success** · last run [#1](https://github.com/MuhammadTalhaBaloch/iptv/actions/runs/29115773920) at 2026-07-10 18:47 UTC

_Full diff uploaded as the run artifact `sources-vs-index`._
<!-- DASHBOARD:END -->

## 📺 EPG (TV guide)

Regenerated **daily (21:00 UTC / 02:00 PKT)** from [iptv-org/epg](https://github.com/iptv-org/epg)
(all ~248 sites) and published as **per-country gzip files** to the `gh-pages` branch.

- The app uses the default base URL below and fetches only the countries you watch, on demand
  (12 h TTL). Leave **Settings → TV Guide** blank to use it, or paste the base URL explicitly:
  ```
  https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide/
  ```
- Channel ids carry the iptv-org `@SD`/`@HD` feed suffix (`GeoNews.pk@SD`); the app normalizes ids
  (drops `@feed`, punctuation, case) so guide data attaches to your channels automatically.
- **Coverage** = whatever the sites return to GitHub's US-based runner; many geo-block non-local IPs
  (403), so e.g. India comes through well while Pakistani EPG is thin *at the source* (~11 channels).

> **Why per-country, not one file?** An earlier design published a single ~120 MB `guide.xml.gz` as a
> GitHub Release asset. It was split into per-country files on `gh-pages` so the app downloads only
> what it needs — and each `.gz` stays well under `gh-pages`' 100 MB `git push` limit.

## 🗂 Source registry (`sources.json`) + region map (`country_regions.json`)

Regenerated daily (21:15 UTC) by [`sources.yml`](.github/workflows/sources.yml), committed to `main`
only when changed (the app ETag-refreshes both, with bundled fallbacks):

- **`sources.json`** ([`tools/gen-sources.py`](tools/gen-sources.py)) — the browse menu (countries,
  categories, languages, regions, subdivisions, cities + index playlists, ~**1299** groups).
- **`country_regions.json`** ([`tools/gen-country-regions.py`](tools/gen-country-regions.py)) —
  country → iptv-org region membership, for the app's **"Play all Regions"** ordering.

## 📶 Availability (`availability.json`)

Regenerated after each sources run by [`probe-availability.yml`](.github/workflows/probe-availability.yml)
([`tools/probe-availability.py`](tools/probe-availability.py)) — a faithful replica of the app's
Deep-Refresh probe run over the whole catalog. Publishes the set of **reachable** stream URLs so the
app's **"Hide unavailable"** works instantly, with **no full catalog download and no per-user probe**;
the on-device recheck stays as an on-demand per-user (geo) refinement.

> Probed from GitHub's **US** runner, so it reflects US reachability (~3 % differs by geo — corrected
> per-user on device). Snapshot only; streams flap between runs.

---

## 🔑 Requirements (one-time)

| Requirement | Why |
|---|---|
| Repo is **public** | Free unlimited Actions + public `raw.githubusercontent.com` serving. |
| Secret **`IPTVPAT`** | Personal Access Token, **Contents: write**. Used by every workflow that commits/publishes (EPG, sources, availability, dashboard). Deliberately a PAT, not `GITHUB_TOKEN`: a PAT-authored push counts as repo activity, keeping the scheduled workflows alive past GitHub's 60-day inactivity auto-disable. **If it expires, regenerate it and update the secret.** |

No GitHub Pages setup is needed — the app reads over `raw.githubusercontent.com`, independent of
Pages. (If Pages happens to be enabled on `gh-pages`, GitHub's built-in *"pages build and
deployment"* job runs on each publish but the app ignores it — see [`WORKFLOWS.md`](WORKFLOWS.md#raw-serving-vs-github-pages-the-pages-build-and-deployment-job).)

## 💸 Cost

**$0** — public repo → free Actions and free raw hosting.

## 📄 Repo contents

- [`.github/workflows/epg.yml`](.github/workflows/epg.yml) — daily per-country EPG generator.
- [`.github/workflows/sources.yml`](.github/workflows/sources.yml) — daily `sources.json` + `country_regions.json` refresh.
- [`.github/workflows/probe-availability.yml`](.github/workflows/probe-availability.yml) — daily `availability.json` (reachable list).
- [`.github/workflows/compare-sources.yml`](.github/workflows/compare-sources.yml) — manual sources-vs-index diff experiment.
- [`.github/workflows/dashboard.yml`](.github/workflows/dashboard.yml) — regenerates the dashboard above.
- [`tools/`](tools/) — `gen-sources.py`, `gen-country-regions.py`, `probe-availability.py`, `compare-sources.py`, `build-dashboard.py`.
- [`WORKFLOWS.md`](WORKFLOWS.md) — detailed technical reference + flow diagrams.
- [`EPG.md`](EPG.md) — EPG quick reference.
- Other `*.md` — unrelated IPTV source-research notes.
