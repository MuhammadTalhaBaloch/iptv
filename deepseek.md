# The Open IPTV Source Handbook

**Manual discovery, verification, and use of free, legal live TV and radio streams for Jellyfin, Threadfin, xTeVe, Kodi, VLC, and more.**

---

> **Disclaimer**  
> This guide is intended for **educational and personal archival purposes only**.  
> Always verify that you have the right to access and use any stream according to your local laws, the provider’s terms of service, and applicable copyright regulations.  
> The tools and techniques described here must only be applied to **publicly available, freely distributed, and DRM‑free content**.  
> The author does not condone piracy or unauthorized access to paid/encrypted services.

---

## Table of Contents

1. [Key Terminology – What Are These Sources Called Exactly?](#1-key-terminology)
2. [Differences Between All the Acronyms and File Types](#2-differences)
3. [Manual Discovery Methods](#3-manual-discovery-methods)
   - [3.1 Search Engine Queries](#31-search-engine-queries)
   - [3.2 Code Forge Discovery (GitHub, GitLab, Codeberg, etc.)](#32-code-forge-discovery)
   - [3.3 Browser Developer Tools & Page‑Source Inspection](#33-browser-developer-tools--page-source-inspection)
   - [3.4 Official Broadcaster Websites](#34-official-broadcaster-websites)
   - [3.5 Government, Public Access, Education & University Streams](#35-government-public-access-education--university-streams)
   - [3.6 FAST Providers (Free Ad‑Supported TV)](#36-fast-providers)
   - [3.7 EPG / XMLTV Discovery](#37-epg--xmltv-discovery)
   - [3.8 Public APIs & JSON Feeds](#38-public-apis--json-feeds)
   - [3.9 Kodi Addon & PVR Source Discovery](#39-kodi-addon--pvr-source-discovery)
   - [3.10 Tvheadend, xTeVe, Threadfin, Telly Community Methods](#310-tvheadend-xteve-threadfin-telly-community-methods)
   - [3.11 YouTube Live (Streamlink, yt-dlp)](#311-youtube-live-streamlink-yt-dlp)
   - [3.12 Radio & Visual‑Radio Sources](#312-radio--visual-radio-sources)
   - [3.13 CDN Pattern Searching](#313-cdn-pattern-searching)
   - [3.14 Playlist Generators](#314-playlist-generators)
   - [3.15 Docker / Package‑Manager Discovery](#315-docker--package-manager-discovery)
   - [3.16 GitHub Pages & Generated Static Playlists](#316-github-pages--generated-static-playlists)
   - [3.17 Raw Content CDN Discovery](#317-raw-content-cdn-discovery)
   - [3.18 Playlist Mirrors](#318-playlist-mirrors)
   - [3.19 Internet Archive & Historical Discovery](#319-internet-archive--historical-discovery)
   - [3.20 Forum & Community Discovery](#320-forum--community-discovery)
   - [3.21 Safe Inspection of Official Apps & Websites](#321-safe-inspection-of-official-apps--websites)
   - [3.22 Local Tuner Methods (HDHomeRun, OTA, DVB, ATSC, SAT>IP)](#322-local-tuner-methods)
   - [3.23 Building Your Own M3U File](#323-building-your-own-m3u-file)
   - [3.24 Converting JSON/CSV/HTML/API Lists to M3U](#324-converting-jsoncsvhtmlapi-lists-to-m3u)
   - [3.25 Monitoring Repository Updates](#325-monitoring-repository-updates)
   - [3.26 Logo & Channel Metadata Discovery](#326-logo--channel-metadata-discovery)
   - [3.27 Public Channel Databases](#327-public-channel-databases)
4. [Verification & Validation](#4-verification--validation)
   - [4.1 Playlist Syntax Validation](#41-playlist-syntax-validation)
   - [4.2 VLC Validation](#42-vlc-validation)
   - [4.3 ffmpeg / ffprobe Validation](#43-ffmpeg--ffprobe-validation)
   - [4.4 Header Requirement Checks](#44-header-requirement-checks)
   - [4.5 Region / Geo Availability Checks](#45-region--geo-availability-checks)
   - [4.6 Detection of Tokenized Streams](#46-detection-of-tokenized-streams)
   - [4.7 Detection of DRM‑Protected Streams](#47-detection-of-drm-protected-streams)
   - [4.8 Legal Validation Checklist](#48-legal-validation-checklist)
5. [Using Your Sources in Tools](#5-using-your-sources-in-tools)
   - [5.1 Jellyfin – Live TV Setup Summary](#51-jellyfin--live-tv-setup-summary)
   - [5.2 Threadfin / xTeVe / Tvheadend](#52-threadfin--xteve--tvheadend)
   - [5.3 Kodi (IPTV Simple Client)](#53-kodi-iptv-simple-client)
   - [5.4 VLC & Other Desktop Players](#54-vlc--other-desktop-players)
6. [Tracking & Reliability Management](#6-tracking--reliability-management)
   - [6.1 Spreadsheet Tracking Columns](#61-spreadsheet-tracking-columns)
   - [6.2 Scheduled Link‑Health‑Check Routine](#62-scheduled-link-health-check-routine)
   - [6.3 Checking Update Frequency & Reliability](#63-checking-update-frequency--reliability)
7. [Search Query Master List](#7-search-query-master-list)
8. [Example M3U & XMLTV Snippets](#8-example-m3u--xmltv-snippets)
9. [Threadfin / xTeVe Cleanup Workflow](#9-threadfin--xteve-cleanup-workflow)
10. [Glossary (Quick Reference)](#10-glossary-quick-reference)

---

## 1. Key Terminology

| Term | Meaning |
|------|---------|
| **IPTV playlist** | A list of TV/radio streams, usually in M3U format. |
| **M3U** | A plain‑text playlist file that contains stream URLs and optional metadata (e.g., `#EXTINF` tags). |
| **M3U8** | 1) An M3U file encoded in UTF‑8. 2) The playlist file format used by HLS, containing a list of media segment URLs. |
| **HLS stream** | HTTP Live Streaming – a video stream delivered as a sequence of small `.ts` or `.fmp4` segments, described by an `.m3u8` playlist. |
| **XMLTV** | An XML schema for TV listings (channel schedules). |
| **EPG** | Electronic Program Guide – the actual schedule data, often distributed as XMLTV files. |
| **FAST channels** | Free Ad‑Supported Streaming TV channels (e.g., Pluto TV, Samsung TV Plus). |
| **OTT streams** | Over‑The‑Top streams – video delivered over the internet, bypassing traditional cable/satellite. |
| **M3U tuner source** | An M3U playlist used as a virtual tuner in software like Jellyfin, xTeVe, or Threadfin. |
| **Live TV source** | Any input that provides live television to a media centre – can be an M3U, HDHomeRun, XMLTV, etc. |
| **Xtream Codes API** | A proprietary API used by many IPTV providers for authentication, channel lists, and EPG. |
| **DASH** | Dynamic Adaptive Streaming over HTTP – similar to HLS but uses `.mpd` manifests and fragmented MP4 segments. |
| **RTMP** | Real‑Time Messaging Protocol – an older streaming protocol (often Flash‑based). |
| **RTSP** | Real‑Time Streaming Protocol – used for live streaming from IP cameras and some legacy servers. |

---

## 2. Differences

| Concept | Type / Role | Typical File Extension | Notes |
|---------|-------------|------------------------|-------|
| **IPTV playlist** | Generic term | .m3u, .m3u8 | Can contain HLS, MPEG‑TS, RTMP, etc. |
| **M3U** | Playlist format | .m3u | ASCII or ANSI encoding, often with `#EXTINF` |
| **M3U8** | Playlist (UTF‑8) or HLS manifest | .m3u8 | Always UTF‑8; if used by HLS, it lists segments |
| **HLS stream** | Delivery protocol | .m3u8 (master/variant) | Adaptive bitrate, works in browsers |
| **XMLTV** | Data format | .xml, .xmltv | Contains `<programme>` entries |
| **EPG** | Guide data | .xml (XMLTV), .json | The actual schedule |
| **FAST channels** | Business model | – | Free, ad‑supported linear streams |
| **OTT streams** | Delivery method | – | Any internet‑delivered video |
| **M3U tuner source** | Functional role | .m3u/.m3u8 | Used as a “virtual tuner” |
| **Xtream Codes API** | Authentication/listing | – | Requires server URL, username, password |
| **DASH** | Streaming protocol | .mpd | Often DRM‑protected |
| **RTMP** | Protocol | rtmp:// | Declining, often Flash‑based |
| **RTSP** | Protocol | rtsp:// | Common in IP cameras, low latency |

---

## 3. Manual Discovery Methods

### 3.1 Search Engine Queries

Use advanced operators to find publicly posted playlists.

**Google / Bing / DuckDuckGo examples:**

```
"#EXTM3U" filetype:m3u
"#EXTM3U" filetype:m3u8
"#EXTINF:-1" "group-title" "http" filetype:m3u
"EXTINF" "tvg-id" "tvg-name" filetype:m3u
intitle:"playlist.m3u" "hls"
site:github.com "#EXTM3U" "tvg-logo"
"#EXTINF" "CCTV" "m3u8" -inurl:(jsp|php|html)
"xmltv" filetype:xml "channel id"
"tvg-shift" "m3u" intitle:"index of"
"udp://" OR "rtp://" "m3u"
"catchup" "m3u8" "EXTINF"
"FAST" "m3u" "Pluto TV"
"pluto" "master.m3u8" "plutotv"
```

**Useful search operators:**

| Operator | Function |
|----------|----------|
| `filetype:m3u` | Only M3U files |
| `intitle:"index of"` | Directory listings |
| `site:github.com` | Restrict to GitHub |
| `-inurl:html` | Exclude HTML pages |
| `"exact phrase"` | Exact match |
| `related:example.com` | Similar sites |
| `after:2024-01-01` | Time filter (Google) |

### 3.2 Code Forge Discovery

Search public repositories for M3U/XMLTV files and tools.

**GitHub:**

```
https://github.com/search?q=%22%23EXTM3U%22+language%3AM3U
https://github.com/search?q=%22tvg-id%22+m3u&type=code
https://github.com/search?q=iptv+playlist+stars%3A%3E50&type=repositories
https://github.com/topics/iptv
https://github.com/topics/m3u
https://github.com/topics/xmltv
https://github.com/topics/epg
https://github.com/topics/iptv-playlist
```

**GitLab:**

```
https://gitlab.com/search?search=%23EXTM3U
https://gitlab.com/explore/projects/topics/iptv
```

**Codeberg, Gitea, Forgejo:**

```
https://codeberg.org/explore/repos?q=%23EXTM3U
https://gitea.com/explore/repos?q=%23EXTM3U
(For other Gitea/Forgejo instances, adjust the domain)
```

**Bitbucket:**

```
https://bitbucket.org/repo/all?name=%23EXTM3U
```

**SourceForge:**

```
https://sourceforge.net/directory/?q=m3u+iptv
```

**Pro tip:** Look for repositories that auto‑generate playlists (e.g., using GitHub Actions to scrape and validate channels). They often have high update frequency.

### 3.3 Browser Developer Tools & Page‑Source Inspection

Many streaming sites load their video sources dynamically.

**Workflow:**

1. Open the webpage (e.g., a FAST provider’s live TV page).
2. Press `F12` → **Network** tab.
3. Filter for `m3u8`, `mpd`, `master`, `playlist`, `.ts`, `chunklist`.
4. Refresh the page and start a stream.
5. Copy the first `.m3u8` or `.mpd` URL.
6. Sometimes you need to look for an API call (e.g., `channel?slug=...`) that returns the stream URL.
7. Check the **Page Source** (`Ctrl+U`) for embedded URLs or JavaScript variables containing `"url": "https://..."` or `"streamUrl"`.

**Example pattern to search in source:**

```
m3u8
master.m3u8
manifest
hlsUrl
streamUrl
source:
"url":
```

### 3.4 Official Broadcaster Websites

Many national broadcasters offer free live streams directly.

**Approach:**

1. Visit the broadcaster’s site (e.g., `bbc.co.uk`, `zdf.de`, `raiplay.it`).
2. Use the Developer Tools method above.
3. In some cases, the stream URL is stable and doesn’t require tokens (if it’s DRM‑free).
4. Create an M3U entry.

**Examples (free, may be geo‑restricted):**

- Deutsche Welle: `https://dwamdstream102.akamaized.net/.../master.m3u8`
- NASA TV: `https://ntv1.akamaized.net/hls/live/.../master.m3u8`
- C‑SPAN: `https://cspan-live.akamaized.net/.../master.m3u8`

### 3.5 Government, Public Access, Education & University Streams

- **Municipal/legislative streams:** Many city councils and parliaments provide live streams (e.g., `parliamentlive.tv`).
- **Public access channels:** Community media centres often stream HLS feeds.
- **University/college TV:** Campus stations (e.g., `https://video.ucsd.edu/...`).
- **Educational networks:** Annenberg Learner, research institution live feeds.

**Search queries:**

```
"live stream" site:.gov "m3u8"
"public access" "m3u8" live
"university" "live" "hls" intitle:"channel"
```

### 3.6 FAST Providers

Free Ad‑Supported TV services offer linear channels. Many of their streams are discoverable via app traffic inspection or public APIs.

| Provider | Method / Notes |
|----------|----------------|
| **Pluto TV** | Use browser DevTools on `pluto.tv/live-tv`. Look for `stitcher` API calls returning `.m3u8`. |
| **Plex Live TV** | Plex’s FAST channels are often listed in repositories that extract them. |
| **Samsung TV Plus** | Some channels accessible via CDN patterns (e.g., `samsungtvplus.com`). |
| **LG Channels** | Similar to Samsung, often integrated in webOS. |
| **Rakuten TV** | Some live channels are free; inspect network. |
| **Stirr** | (Now defunct in some regions) – legacy playlists may still circulate. |
| **Xumo** | Inspect `xumo.com`; often uses static CDN URLs. |
| **Tubi Live** | Tubi offers live news/sports; check `tubitv.com/live`. |
| **Freevee (Amazon)** | Amazon Freevee has live channels; may require Prime token. |
| **Roku Channel** | `therokuchannel.roku.com` – inspect network for HLS. |
| **Local Now** | Weather/news FAST channels. |
| **DistroTV** | Independent FAST channels; website player inspection. |
| **Haystack News** | News‑only FAST. |
| **Sling Freestream** | Sling’s free tier; check `sling.com`. |
| **TCL Channel** | TCL smart TV platform; often regional. |
| **Vizio WatchFree+** | `watchfree.vizio.com`. |
| **Crackle** | `crackle.com` has free movies & some live channels. |
| **Runtime** | Free movies & live. |
| **FilmRise** | Free movies & live channels; website inspection. |

**Note:** Stream URLs from FAST providers may change frequently or require geographic access. Extracted URLs should not be distributed widely; use them only for personal, non‑commercial purposes.

### 3.7 EPG / XMLTV Discovery

**Search queries:**

```
"tv" "xmltv" filetype:xml
"<tv generator-info-name="
"<programme" "channel" filetype:xml
site:github.com "xmltv.xml"
"xmltv" "iptv" "epg"
```

**Common public EPG sources (for free‑to‑air channels):**

- `http://epg.51zmt.top:8000/` (China region)
- `https://iptv-org.github.io/epg/` (IPTV‑org’s generated EPG)
- `https://www.xmltv.co.uk/feed/` (various countries)
- `https://i.mjh.nz/` (Australia/NZ)
- `https://epgshare01.online/` (multi‑region)

**Generating your own XMLTV:**

- Use **WebGrab+Plus** with site‑specific `.ini` files.
- Use **tv_grab_zz_sdjson** (Schedules Direct) – requires a (low‑cost) membership.

### 3.8 Public APIs & JSON Feeds

Many services provide channel lists in JSON format that you can convert to M3U.

**Examples:**

- **IPTV‑org API:** `https://iptv-org.github.io/api/channels.json`
- **MoveOnJoy’s free channel list:** `https://raw.githubusercontent.com/moveonjoy/M3U/main/iptv.m3u`
- **NASA TV API:** `https://www.nasa.gov/api/2/` (for asset URLs)

**How to use:** Fetch the JSON, parse it, extract `url`, `name`, `logo`, and generate M3U entries (see section 3.24).

### 3.9 Kodi Addon & PVR Source Discovery

**Approach:**

1. Install a Kodi addon that provides live TV (e.g., **PVR IPTV Simple Client**, **Pluto.TV**, **Samsung TV Plus**, **iPlayer WWW**, etc.).
2. Enable **debug logging** in Kodi.
3. Play a channel and examine the log file (`kodi.log`) for the stream URL.
4. Extract URLs and build your own M3U.

**Kodi repository inspection:**

- Look at addon source code on GitHub (e.g., `plugin.video.plutotv`, `plugin.video.samsungtvplus`). They often contain direct API endpoints or playlist generators.

**PVR sources:**

- **IPTV Simple Client** can use M3U/XMLTV URLs; you can share those URLs with Jellyfin.

### 3.10 Tvheadend, xTeVe, Threadfin, Telly Community Methods

- **Tvheadend:** Users often post their channel lists (using the `tvheadend` format) on forums. Convert them to M3U.
- **xTeVe/Threadfin:** The communities maintain “xTeVe provider” files (XML that simulates an IPTV provider). You can import these.
- **Telly:** A lightweight IPTV proxy that can expose an HDHomeRun‑emulated interface. Its configuration often contains M3U URLs.

**Search for shared configurations:**

```
"xTeVe" "m3u" filetype:xml
site:github.com "Threadfin" "provider"
"telly" "playlist" "m3u"
```

### 3.11 YouTube Live (Streamlink, yt-dlp)

**Caution:** Only use tools that respect YouTube’s terms (e.g., Streamlink for personal viewing, not commercial redistribution).

**Method:**

1. Find a YouTube channel that live‑streams (e.g., news, music, weather).
2. Use **Streamlink** to extract the HLS stream:  
   `streamlink https://www.youtube.com/watch?v=VIDEO_ID best --stream-url`
3. The output is an HLS URL (often with temporary tokens). It may expire.
4. **yt-dlp** can also list formats:  
   `yt-dlp -g https://www.youtube.com/watch?v=VIDEO_ID`

**Note:** YouTube Live streams require regular token refresh. Some tools (like **Streamlink Twitch GUI**) can act as a proxy.

### 3.12 Radio & Visual‑Radio Sources

- Many internet radio stations also broadcast video (visual radio) or have album art streams.
- Search for radio station M3U playlists: `"#EXTM3U" "radio" "mp3" OR "aac"`.
- Use directories like `radio-browser.info` which have an API returning stream URLs (`https://de1.api.radio-browser.info/json/stations/search?name=BBC`). Convert to M3U.

**Visual radio:** Some FM stations provide an HLS feed with a static image/video loop.

### 3.13 CDN Pattern Searching

Many large broadcasters use predictable CDN URLs.

**Common CDN patterns:**

- Akamai: `*.akamaized.net/*/master.m3u8`
- Cloudfront: `*.cloudfront.net/*.m3u8`
- Fastly: `*.fastly.net/*.m3u8`
- Edgecast: `*.edgecastcdn.net/*.m3u8`

**Search for them:**

```
site:akamaized.net "master.m3u8"
"cloudfront.net" "m3u8" live
"fastly" "hls" "index.m3u8"
```

**Pro tip:** Combine with a known channel name: `"CNN" "akamaized.net" "m3u8"`.

### 3.14 Playlist Generators

Some projects auto‑generate M3U files from various sources.

- **iptv‑org/iptv** – generates country‑specific playlists.
- **Free-TV/IPTV** – curated public channels.
- **moveonjoy/M3U** – daily updated playlists.
- **LinuxServer.io’s `docker-iptv`** – can generate playlists from custom rules.

**How to find them:**

```
site:github.com "generate playlist" iptv
"auto-update" "m3u" "github actions"
```

### 3.15 Docker / Package‑Manager Discovery

Docker images sometimes bundle playlists.

- Search Docker Hub: `https://hub.docker.com/search?q=iptv`
- Look at `docker-compose.yml` files that include volume mounts for `.m3u` files.
- Example: `linuxserver/iptv` or `tellytv/telly`.

### 3.16 GitHub Pages & Generated Static Playlists

Many users publish M3U/XMLTV files directly via GitHub Pages.

**Search:**

```
site:github.io "EXTM3U"
site:github.io "tvg-id"
site:github.io "xmltv"
"https://*.github.io/iptv.m3u"
```

**Example:** `https://iptv-org.github.io/iptv/index.m3u` (a massive curated list).

### 3.17 Raw Content CDN Discovery

Use “Index of” searches to find open directories containing M3U files.

```
intitle:"index of" "m3u" -html -php -asp
"index of /" "playlist.m3u"
"parent directory" "m3u8"
```

### 3.18 Playlist Mirrors

Some communities mirror well‑known playlists on different hosting services.

**Search:**

```
site:pastebin.com "m3u" "EXTINF"
"mirror" "playlist.m3u" "github"
"raw.githubusercontent.com" "m3u" "iptv"
```

### 3.19 Internet Archive & Historical Discovery

The Wayback Machine and Archive.org collections may contain old playlists that still work.

- Search `archive.org`: `subject:"iptv"`, `m3u`, `xmltv`.
- Use Wayback Machine to view historical versions of sites that published playlists.

### 3.20 Forum & Community Discovery

Places to lurk (always respect forum rules):

- **Reddit:** r/IPTV, r/m3u, r/FreeTelevision (beware spam).
- **Discord servers** of open‑source projects (Threadfin, xTeVe, Jellyfin).
- **Matrix rooms / IRC:** `#iptv` on Libera.Chat.
- **Telegram channels** that post working playlists (search `t.me` with keywords).

### 3.21 Safe Inspection of Official Apps & Websites

**Procedure (for educational research only):**

1. Download the official app (Android APK) – do not decompile or reverse‑engineer.
2. Set up a **man‑in‑the‑middle proxy** (e.g., mitmproxy) to capture HTTPS traffic from your own device.
3. Filter for `.m3u8` or API responses containing stream URLs.
4. **Important:** This may violate the app’s terms of service. Only inspect apps you own and only for your personal, non‑commercial use.

### 3.22 Local Tuner Methods

Your own hardware can be the best source.

| Hardware | Protocol | Use with Jellyfin |
|----------|----------|-------------------|
| **HDHomeRun** | DLNA/HTTP | Jellyfin detects it natively via the HDHomeRun tuner. |
| **USB DVB‑T/T2/C** | DVB | Use **Tvheadend** as a backend, then add it to Jellyfin. |
| **ATSC 3.0 tuner** | ATSC | Works with HDHomeRun or Tvheadend. |
| **SAT>IP server** | SAT>IP | Jellyfin supports SAT>IP directly. |

These provide fully legal, high‑quality streams. Combine with XMLTV from over‑the‑air EPG or Schedules Direct.

### 3.23 Building Your Own M3U File

You can manually create a plain‑text file.

**Minimal M3U:**

```
#EXTM3U
#EXTINF:-1,My Channel
http://example.com/stream.m3u8
```

**Full with attributes:**

```
#EXTM3U x-tvg-url="https://example.com/epg.xml"
#EXTINF:-1 tvg-id="bbc1.uk" tvg-name="BBC One" tvg-logo="https://logo.png" group-title="UK",BBC One HD
#EXTVLCOPT:http-user-agent=ExamplePlayer
http://cdn.bbc.co.uk/bbc1/master.m3u8
```

Save with `.m3u` extension (use UTF‑8 encoding for `.m3u8`).

### 3.24 Converting JSON/CSV/HTML/API Lists to M3U

**Example Python snippet (JSON → M3U):**

```python
import json
data = json.loads(open('channels.json').read())
with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    for ch in data:
        f.write(f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n')
        f.write(ch['url'] + '\n')
```

**CSV → M3U:** Use `awk` or Python. **HTML tables:** Use browser console JavaScript to extract `href` attributes and build M3U.

**Tools:** `tv_grab_file` (Tvheadend) can import custom scripts that output JSON.

### 3.25 Monitoring Repository Updates

- Use GitHub’s **Watch** → **Custom** → **Releases** on playlist repos.
- Add RSS feeds: `https://github.com/user/repo/releases.atom`.
- Use **changedetection.io** to monitor any URL for changes.
- Set up a cron job to `git pull` a local clone of a playlist repo.

### 3.26 Logo & Channel Metadata Discovery

**Logo finding:**

- Search `tvg-logo` in public playlists.
- Use `https://logo.iptv-pro.com/` or `https://iptv-org.github.io/iptv/` for channel logos.
- Scrape official broadcaster sites: often `https://example.com/images/channel-logo.png`.

**Metadata:**

- **Language codes:** Use ISO 639‑1 (`en`, `de`).
- **Group titles:** Organise by genre (News, Sports, Entertainment).
- **EPG pairing:** Ensure `tvg-id` matches your XMLTV `<channel id>`.

### 3.27 Public Channel Databases

- **IPTV‑org’s database:** `https://iptv-org.github.io/iptv/channels.json`
- **LyngSat:** Lists satellite transponders, can be used to find free‑to‑air feed URLs.
- **Radio‑Browser:** `https://www.radio-browser.info` for radio.

---

## 4. Verification & Validation

### 4.1 Playlist Syntax Validation

Manual check: Ensure no broken lines, missing `#EXTINF` tags, or invalid URLs.

**Tools:**

- `iptv-checker` (Node.js/Python) – validates all URLs in an M3U.
- Online validators: `https://m3u.validater.com` (upload with care).
- Command line: `grep -c "#EXTINF" playlist.m3u` vs `grep -c "http" playlist.m3u` – numbers should match.

### 4.2 VLC Validation

1. Open VLC → **Media** → **Open Network Stream** (Ctrl+N).
2. Paste the single stream URL. If it plays, it’s working.
3. To test a whole playlist: **Media** → **Open File** → select .m3u. VLC will populate a playlist; you can skip through channels.

**Check codec info:** `Ctrl+J` – look for bitrate, resolution, and whether it’s actually live.

### 4.3 ffmpeg / ffprobe Validation

**Check stream without playing:**

```bash
ffprobe -v quiet -print_format json -show_format -show_streams "http://example.com/stream.m3u8"
```

**Key output:** `"codec_name"`, `"width"`, `"height"`, `"duration"` (should be very short or “N/A” for live).

**Batch scan a playlist with a script:**

```bash
while IFS= read -r url; do
  if ffprobe -v quiet -timeout 5000000 -i "$url"; then
    echo "$url OK"
  else
    echo "$url FAIL"
  fi
done < <(grep -v "^#" playlist.m3u | grep -v "^$")
```

**Check for audio-only or no video:**

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_type -of csv=p=0 "$url"
```

If empty → audio only.

### 4.4 Header Requirement Checks

Some streams require a custom User‑Agent or Referer.

**Test with `curl`:**

```bash
curl -s -I -H "User-Agent: Mozilla/5.0" "http://example.com/stream.m3u8"
```

If you get 403, try common Referers or Origin headers.

In M3U, use:

```
#EXTVLCOPT:http-user-agent=CustomAgent/1.0
#EXTVLCOPT:http-referrer=https://thesourcepage.com/
```

For Jellyfin/xTeVe, you may need to configure the user‑agent in the tuner settings.

### 4.5 Region / Geo Availability Checks

Use a VPN or proxy to test from different locations.

**Quick test:**

```bash
curl --socks5 localhost:1080 -I "http://geo-locked-stream.m3u8"
```

Note in your spreadsheet if a stream is geo‑restricted.

### 4.6 Detection of Tokenized Streams

If a stream URL contains `?token=...` or `?auth=...`, it’s likely temporary.

- Check the HTTP response for `X-Token-Expiry`.
- See if the token is generated from a predictable API (you may be able to script a refresh).
- **Jellyfin/Threadfin cannot handle dynamic tokens natively** – you’ll need a proxy (e.g., a simple Python script that renews the token and exposes a static URL).

### 4.7 Detection of DRM‑Protected Streams

**Indicators:**

- Manifest contains `#EXT-X-KEY:METHOD=AES-128` with a key server URL.
- Widevine/PlayReady license URLs in DASH `.mpd` manifests.
- `ffprobe` shows encrypted streams (e.g., `"encryption": "cenc"`).
- Attempt to play in VLC – if it asks for a key or shows a DRM error, it’s protected.

**These streams are NOT usable** in Jellyfin/Threadfin without a decryption module (which is often illegal to implement). Avoid them.

### 4.8 Legal Validation Checklist

Before adding a stream to your setup, confirm:

- [ ] The content is **intended for free public distribution** (e.g., official broadcaster site has a “Watch Live” button).
- [ ] No **geo‑blocking** terms forbid your access (check the website’s terms).
- [ ] The stream is **not behind a paywall** and does not require a subscription you don’t have.
- [ ] You are **not circumventing any technical protection measures** (DRM).
- [ ] Your use is **purely personal, non‑commercial**, and does not involve re‑broadcasting.
- [ ] The source does **not contain pirated content** (e.g., premium sports, movies).

When in doubt, use only streams from official, well‑known sources like NASA TV, public broadcasters, and local OTA tuners.

---

## 5. Using Your Sources in Tools

### 5.1 Jellyfin – Live TV Setup Summary

1. **Add Tuner Device** (Admin Dashboard → Live TV).
   - **M3U Tuner:** Provide the URL or file path of your `.m3u` playlist.
   - **HDHomeRun:** Detected automatically.
   - **Tvheadend:** Enter server IP and credentials.
2. **Add XMLTV EPG data:**
   - In the same tuner setup, provide an XMLTV URL or file path.
   - Jellyfin will map channels using `tvg-id` or name matching.
3. **Refresh Guide Data** manually.
4. **Map channels** if the auto‑mapping fails.
5. **Enjoy Live TV** on any Jellyfin client.

**Jellyfin supports:** M3U, M3U8, HLS, MPEG‑TS, DASH (without DRM), and HDHomeRun streams.

### 5.2 Threadfin / xTeVe / Tvheadend

**Threadfin/xTeVe (proxy for Plex/Jellyfin/Emby):**

1. Launch the web UI.
2. Add a **new playlist** (M3U URL) and an **XMLTV file**.
3. Let it map channels, filter out unwanted ones, and assign EPG IDs.
4. In Jellyfin/Plex, add a **M3U Tuner** pointing to Threadfin’s output URL:  
   `http://threadfin-ip:34400/playlist.m3u`
5. Similarly, add the EPG URL:  
   `http://threadfin-ip:34400/xmltv.xml`

**Tvheadend:**

- Can import M3U via the “IPTV Automatic Network” feature.
- Use `tv_grab_file` to ingest XMLTV.

### 5.3 Kodi (IPTV Simple Client)

1. Install **PVR IPTV Simple Client** from the Kodi repository.
2. Configure → General → Location = Remote Path.
3. M3U Playlist URL = your playlist.
4. XMLTV URL = your EPG.
5. Enable and restart Kodi.

### 5.4 VLC & Other Desktop Players

- **VLC:** Drag and drop the `.m3u` file.
- **SMPlayer, MPV:** They can play M3U playlists directly.
- **IINA (macOS):** File → Open URL → paste M3U playlist URL.

---

## 6. Tracking & Reliability Management

### 6.1 Spreadsheet Tracking Columns

Use a spreadsheet (Google Sheets, Excel) with these columns:

| Column | Description |
|--------|-------------|
| `Channel Name` | Display name |
| `Group` | Category (News, Sports) |
| `Stream URL` | The direct HLS/RTMP link |
| `M3U File` | Which playlist file it belongs to |
| `tvg-id` | XMLTV ID for EPG |
| `Logo URL` | Channel logo |
| `Status` | OK / FAIL / GEO‑LOCKED / TOKENIZED / DRM |
| `Last Checked` | Date of last validation |
| `HTTP Code` | e.g., 200, 403 |
| `Bitrate/Resolution` | From ffprobe |
| `Notes` | Any special headers, user‑agent, token |
| `Source Type` | FAST, Public Broadcaster, OTA, etc. |
| `Geo Region` | US, UK, etc. |
| `Update Frequency` | How often the stream URL changes (if known) |

### 6.2 Scheduled Link‑Health‑Check Routine

Create a script (Bash/Python) that:

1. Reads your master M3U.
2. For each URL, runs `ffprobe` or `curl` with a timeout.
3. Logs results and updates a status file.
4. Runs via cron daily.

**Example cron job:**

```
0 3 * * * /home/user/check_streams.sh > /var/log/stream_check.log
```

You can use tools like **Uptime Kuma** to monitor HTTP endpoints and alert you if a stream goes down.

### 6.3 Checking Update Frequency & Reliability

- **Monitor the playlist’s last‑modified header:** `curl -s -I https://example.com/playlist.m3u | grep last-modified`
- **Use GitHub Actions** in your own fork to periodically test all streams and automatically disable broken ones (many open‑source projects do this).
- **Check the repository’s commit history** to see how often the playlist is updated.
- **Reliability score:** Over a month, what percentage of days was the stream online? Mark in spreadsheet.

---

## 7. Search Query Master List

Copy‑paste these directly into your preferred search engine.

```
# M3U playlists
"#EXTM3U" filetype:m3u
"#EXTINF:-1" "tvg-name" filetype:m3u8
intitle:"playlist.m3u" "group-title"
"#EXTINF" "m3u8" "http" -php -html
"index of" "m3u8" "parent directory"

# GitHub
site:github.com "#EXTM3U" "tvg-logo"
site:github.com "iptv" "playlist" "stars:>100"

# FAST providers
"pluto" "master.m3u8"
"samsungtvplus" "hls"
"tubitv" "live" "m3u8"
"plex" "live" "m3u8"
"xumo" "playlist.m3u8"

# XMLTV / EPG
"<tv generator-info-name=" filetype:xml
"xmltv" "iptv" "epg" "free"
site:github.com "xmltv.xml"

# CDN patterns
site:akamaized.net "master.m3u8" "live"
"cloudfront.net" "hls" "index.m3u8"
"edgecast" "m3u8" "tv"

# Radio
"radio" "#EXTM3U" "aac" filetype:m3u
site:radio-browser.info "url" "codec"

# IPTV tools
site:github.com "xteve" "m3u"
"threadfin" "config" "xml"
"telly" "playlist" "m3u"

# Public access / education
"public access tv" "m3u8" live
"university" "live stream" "m3u8"
site:.gov "live" "hls"

# Historical / archive
site:archive.org "m3u" "iptv"
"wayback machine" "playlist.m3u"

# Tokenized / DRM detection
"widevine" "mpd" "live"
"#EXT-X-KEY" "AES-128" "m3u8"

# Country specific
"germany" "m3u" "iptv" "public"
"brazil" "tv" "m3u8" "aberto"
```

---

## 8. Example M3U & XMLTV Snippets

**Minimal M3U:**

```m3u
#EXTM3U
#EXTINF:-1,NASA TV Public
https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8
#EXTINF:-1,BBC World Service
http://stream.live.vc.bbcmedia.co.uk/bbc_world_service
```

**Full M3U with EPG:**

```m3u
#EXTM3U x-tvg-url="https://example.com/epg.xml"
#EXTINF:-1 tvg-id="NasaTV.us" tvg-name="NASA TV" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/NASA_TV.svg/1200px-NASA_TV.svg.png" group-title="Science",NASA TV
#EXTVLCOPT:http-user-agent=Mozilla/5.0
https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8
```

**XMLTV example:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE tv SYSTEM "xmltv.dtd">
<tv generator-info-name="manual" generator-info-url="https://example.org">
  <channel id="NasaTV.us">
    <display-name>NASA TV</display-name>
    <icon src="https://logo.png" />
  </channel>
  <programme start="20260401000000 +0000" stop="20260401010000 +0000" channel="NasaTV.us">
    <title>ISS Live Stream</title>
    <desc>Live view from the International Space Station.</desc>
  </programme>
</tv>
```

---

## 9. Threadfin / xTeVe Cleanup Workflow

Both tools include filtering and mapping features. Use this workflow to maintain a clean list.

1. **Import** your M3U playlist.
2. **Filter** unwanted channels by group or name (e.g., remove “XXX”, “Adult”, or non‑working streams).
3. **Map** XMLTV IDs:
   - Choose an existing EPG source and map each channel’s `tvg-id` to the correct EPG entry.
4. **Reorder** channels using drag‑and‑drop.
5. **Replace logos** if missing or broken.
6. **Duplicate handling:** Remove duplicate channels by stream URL.
7. **Export** the sanitized M3U and XMLTV URLs – these will be fed to Jellyfin/Plex.

**Automate with scripts:** Threadfin has an API. You can script channel disabling based on external health checks.

---

## 10. Glossary (Quick Reference)

| Term | Short Definition |
|------|------------------|
| **M3U** | Playlist file containing stream URLs. |
| **M3U8** | UTF‑8 M3U or HLS playlist file. |
| **HLS** | HTTP Live Streaming – segmented video. |
| **FAST** | Free Ad‑Supported TV. |
| **EPG** | Electronic Program Guide. |
| **XMLTV** | XML format for EPG data. |
| **DASH** | Dynamic Adaptive Streaming over HTTP. |
| **OTT** | Over‑the‑top internet streaming. |
| **xTeVe / Threadfin** | M3U proxy/tuner that emulates an HDHomeRun. |
| **Tvheadend** | TV streaming server and recorder. |
| **HDHomeRun** | Network‑attached OTA tuner. |
| **Tokenized stream** | Stream URL with a temporary authentication token. |
| **DRM** | Digital Rights Management – encryption that restricts playback. |
| **tvg‑id** | An attribute in M3U linking a channel to EPG data. |
| **Catchup** | Time‑shifted playback of live TV. |

---

*End of Handbook – Knowledge is for everyone. Use it wisely.*
