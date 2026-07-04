# Self-hosted EPG (TV guide)

A scheduled GitHub Action ([`.github/workflows/epg.yml`](.github/workflows/epg.yml))
regenerates an XMLTV guide daily from [iptv-org/epg](https://github.com/iptv-org/epg)
and publishes it to the `gh-pages` branch. **Free** — GitHub Actions has no minute
limit on public repositories.

## Guide URL (paste into the app → Settings → TV Guide)

```
https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide.xml
```

Gzip version (smaller; use once the app supports gzip EPG):

```
https://raw.githubusercontent.com/MuhammadTalhaBaloch/iptv/gh-pages/guide.xml.gz
```

The channel ids in this guide (`GeoNews.pk@SD`, `AajTak.in@SD`, …) match the app's
playlist tvg-ids, so programmes attach automatically.

## First run

1. Push this repo to GitHub (`git push`).
2. GitHub → **Actions** tab → **Generate EPG** → **Run workflow** (or wait for the
   01:30 UTC schedule). Scheduled workflows only start once the file is on `main`.
3. After it finishes, the URL above is live. No GitHub Pages configuration required.

## Coverage / scope

Scoped to **India** (tataplay, dishtv, airtelxstream, zee5 ≈ 1,700+ channels) plus
**Pakistan/UK** (epg.iptvx.one, mytelly, tvireland, sky). Pakistani EPG is thin at the
source (~11 channels exist across all of iptv-org/epg). To broaden coverage, add site
names to the `--sites=` list in the workflow (see
[SITES.md](https://github.com/iptv-org/epg/blob/master/SITES.md)); more sites = longer
runs and a larger file.
