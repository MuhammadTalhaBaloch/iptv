# Self-hosted EPG (TV guide)

A scheduled GitHub Action ([`.github/workflows/epg.yml`](.github/workflows/epg.yml))
regenerates an XMLTV guide daily from [iptv-org/epg](https://github.com/iptv-org/epg)
and publishes it to the `gh-pages` branch. **Free** — GitHub Actions has no minute
limit on public repositories.

## Guide URL (paste into the app → Settings → TV Guide)

```
https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide.xml.gz
```

The guide covers **all iptv-org/epg channels** (~13k). Only the **gzip** (`.xml.gz`,
~20 MB) is published — the plain XML is >100 MB (GitHub's per-file limit). The app
decompresses `.xml.gz` and stream-parses it. The channel ids (`GeoNews.pk@SD`,
`AajTak.in@SD`, …) match the app's playlist tvg-ids, so programmes attach automatically.

## First run

1. Push this repo to GitHub (`git push`).
2. GitHub → **Actions** tab → **Generate EPG** → **Run workflow** (or wait for the
   01:30 UTC schedule). Scheduled workflows only start once the file is on `main`.
3. After it finishes, the URL above is live. No GitHub Pages configuration required.

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
