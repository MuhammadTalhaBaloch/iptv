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

[`.github/workflows/epg.yml`](.github/workflows/epg.yml) grabs **all ~248 sites**. Because the
grabber buffers the whole guide in memory and writes it only at the end, one process doing all
sites OOMs (~7 GB at ~14%) **and** would exceed GitHub's 6-hour per-job limit. So it's split:

1. **`grab`** — a **20-way parallel matrix**. Each shard freshly clones the latest
   `iptv-org/epg` at `master`, then grabs its round-robin slice of the site list **one site per
   process** (so peak memory is bounded by the single largest site, not the whole shard). A site
   that errors/OOMs only loses that site (logged), never the shard. Each shard uploads its
   per-site XMLTV files as an artifact.
2. **`merge`** — downloads every shard's artifact, stitches them into one `guide.xml`
   (deduping channels by id), **refuses to publish** if the result is empty or lost >50% of the
   currently-published guide's channels (so a partial failure can't clobber the good guide), then
   gzips and publishes `guide.xml.gz` to **`gh-pages`**.

**Triggers:** daily cron `30 1 * * *` + manual **Run workflow** (Actions tab). Wall-clock ≈ the
slowest shard (~2–3 h); shards run in parallel.
**Publish:** [`peaceiris/actions-gh-pages`](https://github.com/peaceiris/actions-gh-pages)
with `force_orphan` (keeps `gh-pages` a single clean commit — no history bloat).

### Requirements (one-time)

| Requirement | Why |
|---|---|
| Repo is **public** | Free unlimited Actions **and** public `raw.githubusercontent.com` serving (private repos 404 on raw + have Action minute caps). |
| Repo **secret `IPTVPAT`** | A Personal Access Token with **Contents: write** on this repo — used to push to `gh-pages`. Settings → Secrets and variables → Actions → Secrets. |

---

## 🔧 Configuration / customizing

Everything is in [`.github/workflows/epg.yml`](.github/workflows/epg.yml):

- **Fewer/faster:** for a leaner, ~2-minute guide, replace the round-robin `ls sites | awk …`
  in the grab step with a fixed `--sites=` list, e.g.
  `--sites=tataplay.com,dishtv.in,airtelxstream.in,zee5.com` (India ≈ 1,800 channels). Site names:
  [SITES.md](https://github.com/iptv-org/epg/blob/master/SITES.md).
- **Shard count:** the `matrix.shard` list length **and** the awk modulus (`n=20`) must match. More
  shards = more parallelism = faster wall-clock (free tier allows 20 concurrent jobs).
- **How many days:** `--days=1` (today). More days = a larger guide.
- **Memory:** `NODE_OPTIONS=--max-old-space-size` caps **one site's** buffer (each site is its own
  process); raise it only if a single very large site OOMs.
- **Publish safety floor:** `ABS_FLOOR` / `REL_FLOOR` in the merge step — tune how aggressively a
  degraded run is blocked from overwriting the live guide.
- **Schedule:** the `cron:` line.

### Coverage caveats

Even grabbing all sites, many **geo-block / rate-limit GitHub's US-based runner (HTTP 403)**, so
their channels return nothing — coverage is "everything the sites give a US IP." Regions like
**India** come through well; **Pakistani** EPG is thin *at the source* (~11 channels exist across
all of iptv-org/epg). A focused `--sites=` list is faster and just as useful for the channels you
actually watch.

---

## 💸 Cost

**$0.** Public repo → GitHub Actions runs and GitHub Pages/raw hosting are free.

---

## 📄 Repo contents

- [`.github/workflows/epg.yml`](.github/workflows/epg.yml) — the daily EPG generator.
- [`EPG.md`](EPG.md) — EPG quick reference.
- `*.md`, `*.csv` — IPTV playlist / source research notes.
