# Self-hosted EPG (TV guide) — quick reference

A scheduled GitHub Action ([`.github/workflows/epg.yml`](.github/workflows/epg.yml)) regenerates a TV
guide **daily** from [iptv-org/epg](https://github.com/iptv-org/epg) and publishes it as
**per-country XMLTV gzip files** to the **`gh-pages`** branch. **Free** — public repos have no Actions
minute limit. For the full technical breakdown see [`WORKFLOWS.md`](WORKFLOWS.md).

## Base URL (app → Settings → TV Guide)

Leave the field **blank** to use the built-in default, or paste it explicitly:

```
https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide/
```

This is a **folder base URL**, not a single file. The app appends `<cc>.xml.gz` per country
(`…/guide/pk.xml.gz`, `…/guide/in.xml.gz`) and reads `…/guide/index.json` for the country list —
fetching **only the countries you watch, on demand** (12 h TTL, 1 h on failure). Each per-country
`.gz` is small (well under `gh-pages`' 100 MB `git push` limit).

> You can also point Settings → TV Guide at **any single XMLTV file** instead (`.xml`, `.xml.gz`, or a
> server-gzipped `.gz` — the app sniffs the gzip magic bytes). It streams and batches a single big
> file so it won't blow up the write transaction.

Channel ids carry the iptv-org `@SD`/`@HD` feed suffix (`GeoNews.pk@SD`, `AajTak.in@SD`); the app
normalizes ids (drops `@feed`, punctuation, case) so programmes attach to your playlist channels
automatically.

## First run

1. Push this repo to GitHub and add the **`IPTVPAT`** secret (PAT with *Contents: write*).
2. GitHub → **Actions** → **Generate EPG** → **Run workflow** (or wait for the 21:00 UTC / 02:00 PKT
   schedule — scheduled workflows only start once the file is on `main`).
3. After it finishes (≈ the slowest of 20 parallel shards), `guide/<cc>.xml.gz` + `guide/index.json`
   are live on `gh-pages` and served at the base URL above.

## Coverage / scope

Grabs **all ~248 iptv-org/epg sites** as **20 parallel shards, one site per process** (the grabber
buffers everything in memory; a single all-sites process OOMs and blows the 6-hour job limit — see
[`WORKFLOWS.md`](WORKFLOWS.md#2-epgyml--generate-epg)). A `merge` job dedupes channels, splits them
per country, and **refuses to publish** an empty/degraded guide (`ABS_FLOOR` / `REL_FLOOR`), so a bad
run never overwrites the last good guide. Shards are balanced by **channel count** (a greedy bin-pack,
so no shard inherits a giant site's whole load) and **each site is time-capped** (`timeout 90m`), so a
slow/hung site is skipped rather than grinding for hours. Actual coverage is whatever the sites return
to GitHub's US-based runner — many geo-block non-local IPs (403), so India comes through well while
**Pakistani EPG is thin at the source itself** (~11 channels across all of iptv-org/epg). For a
smaller/faster guide, replace the site list in the grab step with a specific `--sites=` list (see
iptv-org/epg `SITES.md`).
