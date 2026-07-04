# IPTV — self-hosted EPG + research

This repo hosts a **self-updating TV guide (EPG)** for the IPTV app, plus IPTV
research notes. A scheduled GitHub Action regenerates an XMLTV guide daily from
[iptv-org/epg](https://github.com/iptv-org/epg) and publishes it to a public URL —
**free**, because GitHub Actions has no minute limit on public repositories.

---

## 📺 Public guide URL

Paste this into the app → **Settings → TV Guide**, then **Save & Refresh EPG**:

```
https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide.xml.gz
```

- It's the **gzip** (`.xml.gz`, ~a few–20 MB). The app decompresses and stream-parses it.
- Only the `.gz` is published — the uncompressed guide can exceed **GitHub's 100 MB
  per-file limit**.
- Channel ids carry the iptv-org `@SD`/`@HD` feed suffix (`GeoNews.pk@SD`, `AajTak.in@SD`);
  the app normalizes ids (drops `@feed`, punctuation, case) so guide data attaches to your
  playlist channels automatically.

Updated **daily (~01:30 UTC)**; the app's daily refresh keeps it current.

---

## ⚙️ How it works

[`.github/workflows/epg.yml`](.github/workflows/epg.yml), on every run:

1. **Freshly clones the latest `iptv-org/epg` at `master`** (ephemeral runner → always the
   newest tool + channel/site definitions; logs the exact upstream commit used).
2. `npm install`, then **`npm run grab`** to download the guide.
3. **Publishes** `guide.xml.gz` to the **`gh-pages`** branch (served at the raw URL above).

**Triggers:** daily cron `30 1 * * *` + manual **Run workflow** (Actions tab).
**Publish:** [`peaceiris/actions-gh-pages`](https://github.com/peaceiris/actions-gh-pages)
with `force_orphan` (keeps `gh-pages` a single clean commit — no history bloat).

### Requirements (one-time)

| Requirement | Why |
|---|---|
| Repo is **public** | Free unlimited Actions **and** public `raw.githubusercontent.com` serving (private repos 404 on raw + have Action minute caps). |
| Repo **secret `IPTVPAT`** | A Personal Access Token with **Contents: write** on this repo — used to push to `gh-pages`. Settings → Secrets and variables → Actions → Secrets. |

---

## 🔧 Configuration / customizing

Everything is in the **`Grab guide`** step of [`.github/workflows/epg.yml`](.github/workflows/epg.yml):

- **Which channels:** the `--sites=` list. Currently grabs **all sites** (`ls sites`). For a
  faster, leaner, more reliable job, replace it with a specific list, e.g.
  `--sites=tataplay.com,dishtv.in,airtelxstream.in,zee5.com` (India ≈ 1,800 channels, ~2-min run).
  Site names: [SITES.md](https://github.com/iptv-org/epg/blob/master/SITES.md).
- **How many days:** `--days=1` (today). More days = larger guide (watch the 100 MB `.gz`… and
  the plain-file limit).
- **Schedule:** the `cron:` line.
- **Memory:** `NODE_OPTIONS=--max-old-space-size` (raise if the grabber OOMs on large site sets).

### Coverage caveats

Grabbing "all sites" is a **long job (30–60 min)** and many sites **geo-block / rate-limit
GitHub's US-based runner (HTTP 403)**, so their channels return nothing — coverage is
"everything the sites give a US IP." Regions like **India** come through well; **Pakistani**
EPG is thin *at the source* (~11 channels exist across all of iptv-org/epg). A focused
`--sites=` list is faster and just as useful for the channels you actually watch.

---

## 💸 Cost

**$0.** Public repo → GitHub Actions runs and GitHub Pages/raw hosting are free.

---

## 📄 Repo contents

- [`.github/workflows/epg.yml`](.github/workflows/epg.yml) — the daily EPG generator.
- [`EPG.md`](EPG.md) — EPG quick reference.
- `*.md`, `*.csv` — IPTV playlist / source research notes.
