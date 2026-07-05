# Self-hosted EPG (TV guide)

A scheduled GitHub Action ([`.github/workflows/epg.yml`](.github/workflows/epg.yml))
regenerates an XMLTV guide daily from [iptv-org/epg](https://github.com/iptv-org/epg)
and publishes it as a **GitHub Release asset**. **Free** — GitHub Actions has no minute
limit on public repositories.

## Guide URL (paste into the app → Settings → TV Guide)

```
https://github.com/MuhammadTalhaBaloch/iptv/releases/download/epg-latest/guide.xml.gz
```

The guide covers **all iptv-org/epg sites** — ~157k channels / ~2.5M programmes, **~120 MB
gzipped**. It's published as a **Release asset** (≤ 2 GB limit), not gh-pages, because a 120 MB
file exceeds gh-pages' 100 MB `git push` limit. The URL is stable (fixed `epg-latest` tag, asset
replaced in place each run). The app decompresses `.xml.gz` and stream-parses it. The channel ids
(`GeoNews.pk@SD`, `AajTak.in@SD`, …) match the app's playlist tvg-ids, so programmes attach
automatically. Note: it's a large download and produces a large on-device EPG database.

## First run

1. Push this repo to GitHub (`git push`).
2. GitHub → **Actions** tab → **Generate EPG** → **Run workflow** (or wait for the
   02:00 PKT / 21:00 UTC schedule). Scheduled workflows only start once the file is on `main`.
3. After it finishes (~2–3 h; it grabs all sites), the `epg-latest` release asset is live at the
   URL above. No GitHub Pages configuration or secret required — publishing uses `GITHUB_TOKEN`.

## Coverage / scope

Grabs **all ~248 iptv-org/epg sites**. The grab runs as **20 parallel shards, one site per
process** (the grabber buffers everything in memory and a single all-sites process OOMs / blows
the 6-hour job limit — see [README](README.md#️-how-it-works)); a `merge` job stitches the
shards and refuses to publish an empty/degraded guide. Actual coverage is whatever the sites
return from GitHub's US-based runner — many geo-block/anti-bot non-local IPs (403), so regions
like India come through well while others are partial. Pakistani EPG is thin at the source itself
(~11 channels across all of iptv-org/epg). To trade coverage for a smaller/faster guide, replace
the round-robin `ls sites | awk …` in the grab step with a specific `--sites=` list (see
[SITES.md](https://github.com/iptv-org/epg/blob/master/SITES.md)).
