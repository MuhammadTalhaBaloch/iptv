# Complete Manual Guide: Finding IPTV Playlists, M3U/M3U8 Streams, EPG/XMLTV Sources, and Jellyfin-Compatible Live TV Sources

## Scope and Principle

This guide explains what IPTV playlist sources are called, how they work, and how to manually discover public, free, legal, official, free-to-air, public-access, government, educational, and FAST TV sources for use with:

- Jellyfin
- Threadfin
- xTeVe
- Tvheadend
- Kodi IPTV Simple Client
- VLC
- MPV
- Streamlink
- Telly
- Other IPTV-compatible tools

This guide is written for knowledge and self-hosted media organization. It does **not** cover bypassing DRM, paywalls, private subscriptions, geo-restrictions, logins, encrypted apps, or paid IPTV provider systems.

---

# 1. What These Sources Are Called Exactly

## 1.1 Main names people use

| Name | Meaning | Usually Used In |
|---|---|---|
| IPTV playlist | A list of live TV/radio channels and stream URLs | Jellyfin, Kodi, VLC |
| M3U playlist | Plain-text playlist format | IPTV, music, radio |
| M3U8 playlist | UTF-8 M3U playlist; also the standard extension for many HLS playlists | HLS/IPTV |
| HLS stream | HTTP Live Streaming stream, commonly ending in `.m3u8` | Web TV, broadcasters |
| Live TV source | Generic name for a TV channel list | Jellyfin, Emby |
| Tuner source | Playlist/device source added as a TV tuner | Jellyfin |
| M3U tuner | Jellyfin tuner type that accepts an M3U playlist URL | Jellyfin |
| Channel list | Human-friendly name for an IPTV playlist | Players |
| Stream list | List of playable stream URLs | Tools/scripts |
| FAST playlist | Playlist of Free Ad-Supported Streaming TV channels | Pluto/Plex/Samsung/etc. |
| OTT stream | Over-the-top internet-delivered TV stream | Apps/websites |
| XMLTV file | XML file containing TV guide data | EPG systems |
| EPG source | Electronic Program Guide source | Jellyfin/Threadfin |
| TV guide URL | Human-friendly term for an EPG/XMLTV URL | Jellyfin |
| Playlist generator | Script/app that creates an M3U from APIs or data sources | FAST platforms |
| IPTV proxy | Tool that filters, maps, or republishes playlists | Threadfin/xTeVe |
| HLS master playlist | `.m3u8` file pointing to multiple qualities/variants | HLS |
| HLS media playlist | `.m3u8` file pointing to media segments | HLS |
| DASH stream | MPEG-DASH stream, usually `.mpd` | Web video |
| RTMP stream | Older live stream protocol | Legacy streams |
| RTSP stream | Real Time Streaming Protocol, common in cameras/local systems | Cameras/TV backends |
| Xtream Codes API | IPTV provider-style API format using server/user/pass | IPTV apps |
| HDHomeRun source | Network TV tuner source | Local/OTA TV |
| DVB/ATSC tuner | Physical TV tuner for antenna/cable/satellite depending on region | Tvheadend/Jellyfin |
| SAT>IP source | Network satellite tuner source | Tvheadend |

---

# 2. Core Formats You Must Recognize

## 2.1 M3U / M3U8

A normal IPTV playlist often looks like this:

```m3u
#EXTM3U
#EXTINF:-1 tvg-id="Channel.ID" tvg-name="Channel Name" tvg-logo="https://example.com/logo.png" group-title="News",Channel Name
https://example.com/live/master.m3u8
```

Important fields:

| Field | Meaning |
|---|---|
| `#EXTM3U` | Playlist header |
| `#EXTINF` | Channel/media metadata line |
| `tvg-id` | ID used to match EPG/XMLTV guide |
| `tvg-name` | Channel name |
| `tvg-logo` | Channel logo URL |
| `group-title` | Category/group |
| URL line | Actual stream URL |

## 2.2 HLS `.m3u8`

HLS streams usually include tags like:

```text
#EXTM3U
#EXT-X-STREAM-INF
#EXT-X-TARGETDURATION
#EXT-X-MEDIA-SEQUENCE
#EXT-X-KEY
#EXTINF
```

Common HLS URL names:

```text
master.m3u8
playlist.m3u8
index.m3u8
live.m3u8
chunklist.m3u8
variant.m3u8
```

## 2.3 XMLTV / EPG

XMLTV guide files often look like this:

```xml
<tv>
  <channel id="Channel.ID">
    <display-name>Channel Name</display-name>
  </channel>

  <programme start="20260601090000 +0000" stop="20260601100000 +0000" channel="Channel.ID">
    <title>Program Name</title>
  </programme>
</tv>
```

Common EPG file names:

```text
epg.xml
guide.xml
xmltv.xml
epg.xml.gz
guide.xml.gz
xmltv.xml.gz
```

---

# 3. What Jellyfin Usually Needs

For Jellyfin Live TV, you normally need:

1. **M3U tuner URL**
   - The channel playlist.
   - Example:
     ```text
     https://example.com/playlist.m3u
     ```

2. **XMLTV/EPG URL**
   - The guide/schedule file.
   - Example:
     ```text
     https://example.com/epg.xml.gz
     ```

3. Optional but recommended:
   - Threadfin or xTeVe between raw playlists and Jellyfin.

Recommended setup:

```text
Raw M3U/M3U8 playlists + XMLTV EPG
        ↓
Threadfin / xTeVe / Tvheadend
        ↓
Cleaned playlist and guide
        ↓
Jellyfin Live TV
```

---

# 4. Manual Discovery Method 1: GitHub Search

GitHub is one of the most important places to find public IPTV playlists and EPG projects.

## 4.1 Search terms

Search GitHub for:

```text
iptv playlist
m3u playlist
m3u8 playlist
live tv m3u
public iptv
legal iptv
free iptv
free to air iptv
EXTM3U
#EXTINF
tvg-id
tvg-logo
group-title
xmltv
epg xmltv
```

## 4.2 GitHub file extension searches

```text
extension:m3u iptv
extension:m3u8 iptv
extension:xml xmltv
extension:json streams m3u8
extension:txt m3u8
filename:playlist.m3u
filename:playlist.m3u8
filename:channels.m3u
filename:tv.m3u
filename:epg.xml
filename:guide.xml
filename:xmltv.xml
```

## 4.3 GitHub exact marker searches

```text
"EXTM3U"
"#EXTM3U"
"#EXTINF:-1"
"tvg-id="
"tvg-name="
"tvg-logo="
"group-title="
"#EXT-X-STREAM-INF"
"#EXT-X-TARGETDURATION"
```

## 4.4 GitHub topic pages

Open/search:

```text
https://github.com/topics/iptv
https://github.com/topics/m3u
https://github.com/topics/m3u8
https://github.com/topics/hls
https://github.com/topics/xmltv
https://github.com/topics/epg
https://github.com/topics/live-tv
https://github.com/topics/tvheadend
https://github.com/topics/jellyfin
https://github.com/topics/kodi
```

## 4.5 How to convert GitHub page links to raw links

GitHub file page:

```text
https://github.com/user/repo/blob/main/playlist.m3u
```

Raw URL:

```text
https://raw.githubusercontent.com/user/repo/main/playlist.m3u
```

Use raw URLs in Jellyfin/Threadfin, not GitHub web page URLs.

## 4.6 What to inspect in a GitHub repository

Check:

- Last commit date
- README legality statement
- License
- Number of stars/forks
- Issue reports about broken streams
- Pull request activity
- Whether streams point to official broadcaster domains
- Whether it includes country/category/language playlists
- Whether it includes EPG/XMLTV
- Whether it is generated automatically
- Whether it uses GitHub Pages for stable raw files

---

# 5. Manual Discovery Method 2: GitLab, Codeberg, Forgejo, Gitea, Bitbucket

Do not only search GitHub.

Search:

```text
site:gitlab.com "EXTM3U"
site:gitlab.com iptv m3u
site:gitlab.com xmltv epg
site:codeberg.org "EXTM3U"
site:codeberg.org iptv m3u
site:bitbucket.org iptv m3u
site:sourceforge.net xmltv
site:sourceforge.net iptv m3u
```

Other places:

```text
GitLab
Codeberg
Forgejo instances
Gitea instances
Bitbucket
SourceForge
Self-hosted Git servers
```

Look for raw file links, not rendered web pages.

---

# 6. Manual Discovery Method 3: Search Engine Operators

Use Google, Bing, DuckDuckGo, Brave Search, Yandex, Kagi, or other search engines.

## 6.1 Filetype searches

```text
filetype:m3u iptv
filetype:m3u8 iptv
filetype:m3u live tv
filetype:m3u8 live tv
filetype:xml xmltv
filetype:gz xmltv
filetype:json m3u8 channels
filetype:txt m3u8 live
```

## 6.2 URL searches

```text
inurl:playlist.m3u
inurl:playlist.m3u8
inurl:channels.m3u
inurl:tv.m3u
inurl:iptv.m3u
inurl:index.m3u8
inurl:master.m3u8
inurl:live.m3u8
inurl:epg.xml
inurl:guide.xml
inurl:xmltv.xml
```

## 6.3 Content searches

```text
"EXTM3U" "tvg-logo"
"EXTM3U" "group-title"
"EXTM3U" "tvg-id"
"#EXTINF:-1" "http"
"#EXT-X-STREAM-INF"
"#EXT-X-TARGETDURATION"
"programme start" "channel="
"xmltv" "display-name"
```

## 6.4 Combined searches

```text
"EXTM3U" "News" "group-title"
"EXTM3U" "Pakistan"
"EXTM3U" "India"
"EXTM3U" "USA"
"EXTM3U" "UK"
"master.m3u8" "live" "news"
"playlist.m3u8" "live" "official"
```

---

# 7. Manual Discovery Method 4: Browser Developer Tools

Many official broadcaster websites use HLS internally.

## 7.1 Steps

1. Open the official broadcaster live page.
2. Press `F12`.
3. Open the **Network** tab.
4. Start the live video.
5. Filter by:
   ```text
   m3u8
   ```
6. Look for:
   ```text
   master.m3u8
   index.m3u8
   playlist.m3u8
   live.m3u8
   ```
7. Copy the request URL.
8. Test it in VLC.
9. Test it with `ffprobe`.
10. If it works without login, cookies, DRM, or expiring tokens, it may be suitable for your private Jellyfin setup.

## 7.2 Other useful filters

```text
m3u8
mpd
hls
dash
playlist
master
chunklist
manifest
json
```

## 7.3 Do not bypass restrictions

Do not bypass:

- DRM
- Paywalls
- Login
- Subscription
- Geo-blocking
- Private tokens
- Encrypted app traffic
- Provider terms

---

# 8. Manual Discovery Method 5: Browser Page Source Search

Sometimes stream URLs are inside page source or JavaScript config.

Search inside the page source for:

```text
m3u8
mpd
hls
dash
stream
source
video
playlist
manifest
live
```

Also check:

```text
view-source:
robots.txt
sitemap.xml
JavaScript files
embedded JSON configs
player config objects
```

Common player config keywords:

```text
jwplayer
videojs
hls.js
shaka
dash.js
theoplayer
bitmovin
brightcove
kaltura
flowplayer
```

---

# 9. Manual Discovery Method 6: Official Broadcaster Websites

Official broadcaster sites are among the safest legal sources.

Search:

```text
official live stream
watch live
live tv
live channel
public live stream
24/7 live stream
```

Categories to search:

```text
News channels
Government TV
Parliament TV
Public broadcasters
Religious broadcasters
Educational channels
Weather channels
NASA/science channels
Local TV stations
University channels
Community TV
City council streams
Radio stations with video
```

Workflow:

```text
Official site
  → Live page
  → Browser Network tab
  → Find .m3u8
  → Test stream
  → Confirm legality
  → Add to personal M3U
```

---

# 10. Manual Discovery Method 7: Public Broadcaster and Government Streams

These are often stable and legal.

Search:

```text
site:*.gov live stream m3u8
site:*.gov "master.m3u8"
site:*.gov "playlist.m3u8"
site:*.edu live stream m3u8
parliament live stream m3u8
senate live stream m3u8
city council live stream m3u8
public access tv m3u8
government channel live stream
university tv live m3u8
```

Possible sources:

- City council channels
- Parliament channels
- State TV
- Public access TV
- University channels
- Court/public hearing streams
- Educational channels
- Science/NASA-style feeds

---

# 11. Manual Discovery Method 8: FAST Providers

FAST means **Free Ad-Supported Streaming TV**.

Common FAST services:

```text
Pluto TV
Plex Live TV
Samsung TV Plus
LG Channels
Rakuten TV
Stirr
Xumo Play
Tubi Live
Freevee
Roku Channel
Redbox Free Live TV
Local Now
DistroTV
Haystack News
Sling Freestream
Fubo Free
TCL Channel
Vizio WatchFree+
Crackle
Runtime
FilmRise
```

Search:

```text
Pluto TV m3u8 playlist
Plex live tv m3u8
Samsung TV Plus m3u8
LG Channels m3u8
Rakuten TV m3u8
FAST channels m3u
FAST playlist m3u8
FAST m3u generator
```

Notes:

- Many FAST playlists are community-generated.
- Some are region-specific.
- Some change APIs frequently.
- Some require generators instead of static files.
- Some may need EPG mapping.

---

# 12. Manual Discovery Method 9: Known Aggregator Projects

Search for public IPTV aggregator projects.

Search:

```text
IPTV aggregator
public IPTV list
legal IPTV playlist
free-to-air IPTV playlist
open IPTV playlist
awesome IPTV
iptv github list
iptv m3u collection
```

Aggregator types:

- GitHub repositories
- Public stream databases
- FAST playlist generators
- EPG databases
- Kodi source lists
- Tvheadend examples
- Country playlist indexes
- Community playlist mirrors

Always verify legal status and stream origin.

---

# 13. Manual Discovery Method 10: Country-Based Search

Search by country:

```text
[country] iptv m3u
[country] live tv m3u8
[country] free tv channels m3u
[country] public tv m3u
[country] official live stream m3u8
[country] public broadcaster live m3u8
```

Examples:

```text
pakistan iptv m3u
india iptv m3u
usa iptv m3u
uk iptv m3u
canada iptv m3u
arabic iptv m3u
turkey iptv m3u
spain iptv m3u
france iptv m3u
germany iptv m3u
japan iptv m3u
korea iptv m3u
```

Better legal-focused versions:

```text
pakistan official live stream m3u8
india public broadcaster live m3u8
uk parliament live m3u8
usa local tv live stream m3u8
canada public access tv m3u8
```

---

# 14. Manual Discovery Method 11: Language-Based Search

Search by language:

```text
urdu iptv m3u
hindi iptv m3u
arabic iptv m3u
turkish iptv m3u
spanish iptv m3u
french iptv m3u
german iptv m3u
persian iptv m3u
chinese iptv m3u
japanese iptv m3u
korean iptv m3u
```

Legal-focused:

```text
urdu official live tv m3u8
arabic public broadcaster m3u8
spanish public tv live m3u8
french news official m3u8
```

---

# 15. Manual Discovery Method 12: Category-Based Search

Search by category:

```text
news live m3u8
weather live m3u8
business news live m3u8
religious tv live m3u8
kids tv live m3u8
music tv live m3u8
education tv live m3u8
parliament tv live m3u8
government tv live m3u8
local tv live m3u8
science tv live m3u8
NASA live m3u8
```

Safer categories:

- News
- Weather
- Government
- Parliament
- Education
- Religion
- NASA/science
- Public access TV
- Local municipality TV
- University TV
- Radio/visual radio

High-risk categories to avoid unless clearly official/free:

- Premium sports
- Paid movie channels
- Pay-per-view
- Cable-only networks
- Adult/premium bundles
- “VIP IPTV” lists

---

# 16. Manual Discovery Method 13: EPG/XMLTV Search

An IPTV playlist gives channels. EPG/XMLTV gives program schedules.

Search:

```text
xmltv
epg
epg xmltv
guide.xml
xmltv.xml
epg.xml.gz
free epg xmltv
iptv epg source
electronic program guide xml
```

Search operators:

```text
filetype:xml xmltv
filetype:gz xmltv
inurl:epg.xml
inurl:xmltv.xml
inurl:guide.xml
"xmltv" "channel id"
"programme start" "programme stop" "channel="
```

Common source types:

- Public XMLTV projects
- Country-specific guide generators
- Community EPG repositories
- Provider-specific public guide data
- WebGrabPlus generated guides
- zap2xml generated guides
- xmltv grabbers

EPG matching rule:

```text
M3U tvg-id should match XMLTV channel id
```

---

# 17. Manual Discovery Method 14: Public APIs and JSON Feeds

Some services expose stream lists through JSON APIs.

Search:

```text
iptv api
channel json
live tv json
m3u generator json
FAST api m3u8
playlist api m3u
streams.json m3u8
channels.json iptv
```

GitHub searches:

```text
site:github.com streams.json iptv
site:github.com channels.json m3u8
"streams.json" "m3u8"
"channels.json" "tvg"
"m3u8" "json" "channels"
```

Workflow:

```text
JSON/API feed
  → Extract channel names and stream URLs
  → Convert to M3U
  → Match EPG
  → Test with VLC/ffprobe
  → Add to Threadfin/Jellyfin
```

---

# 18. Manual Discovery Method 15: Kodi Addons and PVR Sources

Kodi IPTV communities often reference legal/public M3U sources.

Search:

```text
Kodi IPTV Simple Client m3u
Kodi legal IPTV addon
Kodi public TV m3u
Kodi PVR IPTV source
Kodi IPTV Simple Client XMLTV
```

Inspect:

- Addon README
- Source XML files
- M3U URLs
- EPG URLs
- Plugin configs
- GitHub repos behind addons

Avoid piracy addons.

---

# 19. Manual Discovery Method 16: Tvheadend, xTeVe, Threadfin, Telly Communities

These communities often include examples and source references.

Search:

```text
Threadfin m3u playlist
Threadfin xmltv source
xTeVe m3u sources
xTeVe xmltv guide
Tvheadend IPTV automatic network m3u
Telly m3u xmltv
Jellyfin m3u tuner xmltv
```

Useful knowledge:

- Playlist cleanup
- Channel numbering
- EPG mapping
- Buffering
- Proxying
- Filtering by country/category
- Removing dead channels

---

# 20. Manual Discovery Method 17: YouTube Live Through Authorized Tools

Some official broadcasters stream on YouTube Live.

Search:

```text
official YouTube live news channel
official YouTube live TV
official 24/7 live stream
official live stream YouTube
```

Tools:

- Streamlink
- yt-dlp
- FFmpeg
- Local relay/proxy

Concept:

```text
Official YouTube Live URL
  → Streamlink resolves playable stream
  → Local relay/proxy
  → M3U entry for Jellyfin
```

Important:

- Extracted YouTube media URLs expire.
- Direct extracted URLs are not stable.
- A local authorized relay is more reliable.
- Respect broadcaster and platform terms.

---

# 21. Manual Discovery Method 18: Radio and Visual Radio

Some playlists include audio-only or visual radio streams.

Search:

```text
radio m3u playlist
internet radio m3u
visual radio m3u8
radio station live stream m3u
public radio m3u
```

Formats:

```text
.m3u
.pls
.mp3
.aac
.m3u8
```

Tools:

- VLC
- Kodi
- MPV
- Tvheadend
- Jellyfin music libraries
- Jellyfin Live TV depending on source

---

# 22. Manual Discovery Method 19: CDN Pattern Search

Many streams are served through CDNs.

Search:

```text
site:akamaized.net m3u8 live
site:akamaihd.net m3u8 live
site:cloudfront.net m3u8 live
site:fastly.net m3u8 live
site:llnwd.net m3u8 live
"master.m3u8" "news"
"playlist.m3u8" "live"
```

Common streaming/CDN clues:

```text
akamaihd.net
akamaized.net
cloudfront.net
fastly.net
llnwd.net
mux.com
jwplayer
brightcove
kaltura
theoplayer
bitmovin
```

Caution:

A CDN URL alone does not prove legality. Always trace it back to an official source.

---

# 23. Manual Discovery Method 20: Playlist Generators

Some services do not provide a fixed playlist. A generator creates it.

Search:

```text
iptv m3u generator
FAST m3u generator
Pluto TV m3u generator
Samsung TV Plus m3u generator
Plex m3u generator
xmltv generator
epg generator
```

Generator types:

- Web generator
- Docker generator
- GitHub Action generator
- Python script
- Node.js script
- API-to-M3U converter
- JSON-to-M3U converter
- XMLTV generator

Check:

- Is it open source?
- Does it require credentials?
- Does it generate EPG?
- Does it support region selection?
- Is it maintained?
- Does it respect provider terms?

---

# 24. Manual Discovery Method 21: Package Managers and Docker Images

Some tools are distributed as packages.

Search:

```text
Docker IPTV m3u generator
Docker FAST playlist
Docker xmltv grabber
npm iptv m3u
python iptv m3u
pip xmltv
github action iptv playlist
```

Places:

- Docker Hub
- GitHub Container Registry
- npm
- PyPI
- Homebrew
- Linux package repositories
- GitHub Releases

---

# 25. Manual Discovery Method 22: GitHub Pages and Generated Static Sites

Some projects publish playlists to GitHub Pages.

Search:

```text
site:github.io iptv m3u
site:github.io playlist.m3u
site:github.io epg.xml.gz
"generated" "playlist.m3u"
"github actions" "epg.xml"
```

Common patterns:

```text
https://username.github.io/project/playlist.m3u
https://username.github.io/project/index.m3u
https://username.github.io/project/epg.xml.gz
```

---

# 26. Manual Discovery Method 23: Raw Content CDNs

Search raw file hosting URLs.

```text
site:raw.githubusercontent.com "EXTM3U"
site:raw.githubusercontent.com "tvg-id"
site:cdn.jsdelivr.net "EXTM3U"
site:gitlab.com "raw" "EXTM3U"
site:codeberg.org "raw" "EXTM3U"
```

Common raw hosts:

```text
raw.githubusercontent.com
cdn.jsdelivr.net/gh/
github.io
gitlab.com/.../-/raw/
codeberg.org/.../raw/
raw.githack.com
gitcdn.link
```

---

# 27. Manual Discovery Method 24: Playlist Mirrors

Search:

```text
"playlist.m3u" "mirror"
"iptv m3u mirror"
"m3u8 mirror"
"backup playlist"
"playlist backup" "m3u"
```

Use mirrors carefully:

- Prefer original source
- Verify hashes if available
- Check for malicious or pirated additions
- Confirm update date

---

# 28. Manual Discovery Method 25: Internet Archive and Historical Discovery

Useful for discovering old project names or dead repos.

Search:

```text
site:archive.org iptv m3u
site:archive.org xmltv
"iptv playlist" "archive"
"m3u playlist" "archive"
```

Do not assume archived links still work or are legal.

---

# 29. Manual Discovery Method 26: Forums, Communities, and Discussions

Search:

```text
Jellyfin IPTV m3u
Threadfin playlist sources
xTeVe playlist sources
Tvheadend IPTV m3u
legal IPTV sources
public m3u playlist
```

Places:

- Jellyfin forum
- Jellyfin subreddit
- Kodi forum
- Tvheadend forum
- Home server communities
- GitHub Discussions
- Linux media server forums

Avoid piracy communities and reseller lists.

---

# 30. Manual Discovery Method 27: Inspect Official Mobile/Web Apps Safely

Only use this for public, authorized streams.

Do not:

- Reverse engineer encrypted apps
- Bypass DRM
- Extract credentials
- Bypass login
- Bypass geo-restriction
- Bypass paywall
- Abuse private APIs

Safe approach:

```text
Official website
  → Public live player
  → Browser Network tab
  → Public HLS URL
  → Test
  → Use if legally allowed
```

---

# 31. Manual Discovery Method 28: Local OTA, DVB, HDHomeRun, SAT>IP

IPTV does not have to come from the public internet.

Legal local sources:

- Antenna/OTA tuner
- HDHomeRun
- DVB-T/T2
- DVB-S/S2
- DVB-C
- ATSC
- ISDB
- SAT>IP
- Tvheadend tuner backend

Flow:

```text
Antenna / tuner
  → Tvheadend or HDHomeRun
  → M3U/network tuner output
  → Jellyfin
```

This is often the best legal option for local channels.

---

# 32. Manual Discovery Method 29: Convert Tuner Channels to IPTV

Tvheadend can turn tuner channels into stream URLs.

Flow:

```text
Physical TV tuner
  → Tvheadend scan/mapping
  → M3U output
  → Jellyfin M3U tuner
```

This lets you combine OTA and internet playlists.

---

# 33. Manual Discovery Method 30: Build Your Own M3U

If you find verified public streams, create your own playlist.

Example:

```m3u
#EXTM3U
#EXTINF:-1 tvg-id="Example.News" tvg-name="Example News" tvg-logo="https://example.com/logo.png" group-title="News",Example News
https://example.com/live/master.m3u8
```

Best fields to include:

```text
tvg-id
tvg-name
tvg-logo
group-title
channel name
stream URL
```

---

# 34. Manual Discovery Method 31: Convert JSON/CSV/HTML Lists to M3U

You may find streams in formats other than M3U.

Convert:

```text
JSON → M3U
CSV → M3U
HTML table → M3U
Plain URL list → M3U
API response → M3U
```

Basic M3U template:

```m3u
#EXTM3U
#EXTINF:-1,Channel Name
https://example.com/stream.m3u8
```

---

# 35. Manual Discovery Method 32: Use Existing Software Presets and Docs

Search docs for:

```text
m3u tuner
live tv
xmltv
playlist url
guide url
iptv source
```

Software to check:

- Jellyfin
- Emby
- Kodi IPTV Simple Client
- Tvheadend
- Threadfin
- xTeVe
- Telly
- Channels DVR
- Plex DVR
- VLC
- MPV
- Streamlink
- WebGrabPlus

---

# 36. Manual Discovery Method 33: Monitor Repository Updates

Search:

```text
"Generated at" "m3u"
"Last updated" "playlist.m3u"
"updated daily" "iptv"
"GitHub Actions" "iptv"
"auto update" "epg.xml"
```

Check:

- Last commit
- Last release
- GitHub Actions run
- Generated timestamp
- Open issues
- Pull request activity
- Broken stream reports

---

# 37. Manual Discovery Method 34: Search for Channel Logos and Metadata

Search:

```text
channel logos github
iptv logos
tvg-logo
channel database
iptv channel database
channels.json
logos.json
```

Metadata helps with:

- EPG matching
- Channel display
- Logo display
- Country filtering
- Language filtering
- Category filtering

---

# 38. Manual Discovery Method 35: Public Channel Databases

Search:

```text
iptv channel database
public channel database
channels.json iptv
streams.json iptv
logos.json iptv
epg database iptv
```

These may provide:

- Channel IDs
- EPG IDs
- Logo URLs
- Categories
- Countries
- Languages
- Official websites
- Alternative names

---

# 39. Manual Discovery Method 36: Search for Test Streams

Useful for validating your Jellyfin/Threadfin setup.

Search:

```text
public HLS test stream
m3u8 test stream
sample HLS stream
apple bipbop m3u8
video test m3u8
```

Use test streams to confirm:

- Jellyfin tuner works
- Threadfin proxy works
- VLC works
- ffprobe works
- Network/firewall works

---

# 40. Manual Discovery Method 37: Search for Header Requirements

Some legal streams require headers.

Search:

```text
m3u8 user-agent required
m3u8 referer required
iptv m3u user agent
hls referer header
```

Common headers:

```text
User-Agent
Referer
Origin
Cookie
Authorization
```

If a stream requires cookies, login, or authorization, do not treat it as a simple public IPTV source unless the provider allows that usage.

---

# 41. Manual Discovery Method 38: Check Regional Availability

Some legal streams only work in certain regions.

Test from:

- Home network
- Server network
- Mobile network
- VPS region
- Authorized region if provider terms allow

Status values:

```text
Working
Geo-blocked
Tokenized
Forbidden
Dead
Unstable
```

Do not bypass restrictions where not permitted.

---

# 42. Manual Discovery Method 39: Validate with VLC

Steps:

1. Open VLC.
2. Select:
   ```text
   Media → Open Network Stream
   ```
3. Paste playlist or stream URL.
4. Test playback.
5. Check:
   ```text
   Tools → Codec Information
   ```

A source that works in VLC is not guaranteed to work in Jellyfin, but VLC is a good first test.

---

# 43. Manual Discovery Method 40: Validate with ffprobe/ffmpeg

Test stream:

```bash
ffprobe "https://example.com/live/master.m3u8"
```

Test with timeout:

```bash
ffprobe -rw_timeout 10000000 "https://example.com/live/master.m3u8"
```

Test first 10 seconds:

```bash
ffmpeg -i "https://example.com/live/master.m3u8" -t 10 -f null -
```

Common results:

| Result | Meaning |
|---|---|
| 200 OK | Good response |
| 301/302 | Redirect, may still work |
| 403 | Forbidden/header/token/region problem |
| 404 | Dead link |
| 410 | Gone |
| 451 | Legal/region restriction |
| Timeout | Server/network issue |
| DRM/encryption error | Not suitable for normal IPTV |

---

# 44. Manual Discovery Method 41: Validate Playlist Structure

Checklist:

- Starts with `#EXTM3U`
- Has `#EXTINF` entries
- Each channel has a URL after metadata
- Stream URLs are absolute HTTP/HTTPS URLs
- Channel names are readable
- Groups/categories are sensible
- EPG IDs are present if guide is needed
- No credentials in URLs
- No obvious piracy branding
- No huge suspicious premium bundles
- Last update date is recent
- Works in VLC/ffprobe

---

# 45. Manual Discovery Method 42: Detect Tokenized Streams

Tokenized streams are usually unstable.

Signs:

```text
token=
expires=
expire=
signature=
sig=
hdnts=
Policy=
Key-Pair-Id=
X-Amz-Signature=
X-Amz-Expires=
jwt=
auth=
session=
```

These often expire quickly and may not work in Jellyfin long-term.

---

# 46. Manual Discovery Method 43: Detect DRM-Protected Streams

Avoid DRM bypass.

DRM signs:

```text
Widevine
FairPlay
PlayReady
license server
DRM
encrypted
SAMPLE-AES
EXT-X-KEY
.mpd with license URL
```

Normal IPTV tools generally cannot play DRM streams without authorized clients.

---

# 47. Manual Discovery Method 44: Validate Legal Status

## Safer signs

```text
Official broadcaster domain
Government/public broadcaster
Public access TV
Educational/university source
Free ad-supported TV platform
Free-to-air channel
Open public stream
Repository claims public/legal streams only
```

## Red flags

```text
Premium cable channels for free
Pay-per-view for free
Sports packages for free
Thousands of paid channels
Shared Xtream credentials
URLs with username/password
Telegram/Discord reseller dumps
"VIP IPTV"
"premium IPTV free"
"all world channels free"
Pirated movie/sports bundles
```

If you cannot confirm legality, do not use it.

---

# 48. Manual Discovery Method 45: Use Threadfin/xTeVe as a Cleaning Layer

Do not add massive raw playlists directly to Jellyfin.

Recommended:

```text
Raw source playlist
  → Threadfin/xTeVe
  → Filter unwanted channels
  → Map EPG
  → Remove dead channels
  → Export clean M3U/XMLTV
  → Jellyfin
```

Benefits:

- Cleaner guide
- Faster Jellyfin scans
- Fewer broken channels
- Better channel numbering
- Better EPG matching
- Easier maintenance

---

# 49. Manual Discovery Method 46: Maintain a Source Spreadsheet

Recommended columns:

```text
Source
Direct raw URL(s)
Type
Legality
Note
Last updated seen
Reliability and usage notes
Tags
Country
Language
Category
EPG URL
Channel count
Tested in VLC
Tested in ffprobe
Tested in Jellyfin
Status
Date tested
```

Status values:

```text
Working
Partially working
Dead
Geo-blocked
Tokenized
Requires headers
EPG only
Playlist only
Needs proxy
Unverified
```

---

# 50. Manual Discovery Method 47: Schedule Link Health Checks

Suggested routine:

```text
Daily: important playlists
Weekly: full playlist scan
Monthly: EPG mapping review
Monthly: dead channel cleanup
Quarterly: legal/source review
```

Track:

- HTTP status
- Playback result
- EPG match
- Last working date
- Replacement URL
- Notes

---

# 51. Manual Discovery Method 48: Search With Multiple Search Engines

Different engines index different files.

Use:

- Google
- Bing
- DuckDuckGo
- Brave Search
- Kagi
- Yandex
- GitHub search
- GitLab search
- Codeberg search

Search engines may hide or de-rank raw playlist files, so test multiple engines.

---

# 52. Manual Discovery Method 49: Use Search by File Host

Search specific host patterns:

```text
site:raw.githubusercontent.com "EXTM3U"
site:github.io "playlist.m3u"
site:gitlab.com "EXTM3U"
site:cdn.jsdelivr.net "playlist.m3u"
site:pastebin.com "EXTM3U"
site:gist.github.com "EXTM3U"
```

Caution:

Paste sites and gists may contain unauthorized lists. Validate carefully.

---

# 53. Manual Discovery Method 50: Check Gists and Snippets

Search:

```text
site:gist.github.com "EXTM3U"
site:gist.github.com "m3u8"
site:gist.github.com "xmltv"
```

Gists are often temporary and may be unmaintained.

---

# 54. Manual Discovery Method 51: Check Docs of Public Media Players

Some docs list sample streams and compatible source formats.

Search:

```text
VLC m3u8 network stream
mpv hls stream
Kodi IPTV Simple Client m3u xmltv
Jellyfin m3u tuner
Tvheadend IPTV network
```

This helps you understand compatibility, even if it does not provide source lists.

---

# 55. Manual Discovery Method 52: Look for Legal “Free Live TV” Pages

Search:

```text
free live tv official
watch live free official
official 24/7 stream
free ad supported live TV
```

Then inspect with browser developer tools.

---

# 56. Manual Discovery Method 53: Search Newsroom/Press/Developer Pages

Some broadcasters document live feeds for embed partners.

Search:

```text
site:example.com m3u8
site:example.com hls
site:example.com live stream api
site:example.com developer video
site:example.com player config
```

Replace `example.com` with broadcaster domains.

---

# 57. Manual Discovery Method 54: Use robots.txt and sitemaps

Check:

```text
https://example.com/robots.txt
https://example.com/sitemap.xml
```

Search in sitemap for:

```text
live
stream
tv
video
hls
```

---

# 58. Manual Discovery Method 55: Inspect JavaScript Bundles

On official live pages, JavaScript may contain player config URLs.

Search inside loaded `.js` files for:

```text
m3u8
mpd
hls
dash
streamUrl
videoUrl
playbackUrl
source
manifest
```

Stay within public client-side data and legal access.

---

# 59. Manual Discovery Method 56: Use Playlist Diffing

When a playlist changes frequently:

1. Download current version.
2. Download again later.
3. Compare.
4. Identify stable domains and channel naming patterns.

Useful commands:

```bash
diff old.m3u new.m3u
grep -i "m3u8" playlist.m3u
grep -i "tvg-id" playlist.m3u
```

---

# 60. Manual Discovery Method 57: Use Domain Backtracking

If you find a stream URL:

1. Identify the domain.
2. Search that domain with:
   ```text
   site:domain.com m3u8
   site:domain.com live stream
   ```
3. Check whether it belongs to the official broadcaster or provider.
4. Do not use if source cannot be verified.

---

# 61. Manual Discovery Method 58: Search by Channel Name

For a specific channel:

```text
"Channel Name" "m3u8"
"Channel Name" "live stream"
"Channel Name" "official live"
"Channel Name" "HLS"
"Channel Name" "playlist.m3u8"
```

Legal-focused:

```text
"Channel Name" "official" "live"
"Channel Name" site:official-domain.com live
```

---

# 62. Manual Discovery Method 59: Search by EPG ID

If you know an EPG ID:

```text
"channel.id" "xmltv"
"channel.id" "tvg-id"
"channel.id" "m3u"
```

This helps match playlists and EPG data.

---

# 63. Manual Discovery Method 60: Search by Logo URL or Domain

If you find a channel logo:

```text
"logo-url" "m3u"
"channel-logo.png" "tvg-logo"
site:logo-domain.com "tvg-logo"
```

This can reveal related playlists or databases.

---

# 64. Manual Discovery Method 61: Search Public Web Directories Carefully

Some servers expose directory listings.

Search:

```text
intitle:"index of" "playlist.m3u"
intitle:"index of" ".m3u8"
intitle:"index of" "epg.xml"
intitle:"index of" "xmltv"
```

Use only clearly public/authorized content. Directory exposure does not automatically mean permission.

---

# 65. Manual Discovery Method 62: Check IPTV-Org Style Databases

Some projects separate:

- Channel database
- Stream database
- Logo database
- EPG database
- Playlist generator

Search:

```text
channels.csv iptv
streams.csv iptv
guides.xml iptv
logos iptv github
```

These databases help build clean playlists.

---

# 66. Manual Discovery Method 63: Use M3U Validators

Validation ideas:

- Confirm playlist syntax.
- Confirm stream URLs respond.
- Confirm channel count.
- Confirm duplicate channels.
- Confirm EPG ID coverage.
- Confirm logo URLs.

Manual commands:

```bash
curl -L "https://example.com/playlist.m3u" | head
curl -I "https://example.com/playlist.m3u"
grep -c "#EXTINF" playlist.m3u
grep -c "tvg-id" playlist.m3u
```

---

# 67. Manual Discovery Method 64: Check Jellyfin Import Behavior

After adding a source:

- Did Jellyfin import channels?
- Did channel logos appear?
- Did guide data map?
- Are channels duplicated?
- Are playback errors client-specific?
- Does transcoding start?
- Does direct play work?
- Are channels too slow to start?

If problems occur, place Threadfin/xTeVe between Jellyfin and the source.

---

# 68. Manual Discovery Method 65: Search for Alternate Protocols

Some sources are not HLS but still usable.

Search:

```text
rtmp live stream public
rtsp public stream
dash mpd live stream
icecast m3u radio
shoutcast m3u radio
```

Formats:

```text
http://
https://
rtmp://
rtsp://
udp://
rtp://
.mpd
.m3u8
.pls
```

Jellyfin compatibility varies.

---

# 69. Manual Discovery Method 66: Use Streamlink Plugin List

Streamlink supports many official streaming platforms.

Workflow:

```text
Official site URL
  → Streamlink plugin
  → playable stream
  → optional local relay
  → M3U entry
```

Search:

```text
Streamlink supported sites live TV
Streamlink official broadcaster
Streamlink HLS
```

This is useful when a site does not expose a stable plain M3U.

---

# 70. Manual Discovery Method 67: Search Public IPTV Examples in Config Files

Search config repositories:

```text
site:github.com "M3U_URL"
site:github.com "XMLTV_URL"
site:github.com "iptv.m3u"
site:github.com "epg.xml.gz"
site:github.com "xteve" "m3u"
site:github.com "threadfin" "m3u"
```

This can reveal example sources used by self-hosters.

---

# 71. Manual Discovery Method 68: Check IPTV App Sample Configs

Some open-source IPTV apps include sample playlists.

Search:

```text
open source IPTV player sample playlist
iptv app sample m3u
m3u sample channels
```

Inspect:

- README examples
- test fixtures
- demo playlists
- sample XMLTV files

---

# 72. Manual Discovery Method 69: Search Broadcast Standards/Regional Listings

Search local broadcasting authorities or public broadcaster lists:

```text
free to air channels list
public broadcaster live stream
community television live stream
government channel live
```

Then find each channel’s official stream.

---

# 73. Manual Discovery Method 70: Ask the Right Question When Searching

Bad search:

```text
free premium iptv all channels
```

Better search:

```text
official public live stream m3u8
free-to-air broadcaster live stream
public access tv m3u8
FAST m3u playlist
legal IPTV m3u
```

Good searches lead to safer, more stable results.

---

# 74. “Do Not Miss” Search Query Master List

Copy/paste these when hunting manually.

```text
"EXTM3U"
"#EXTM3U"
"#EXTINF"
"#EXTINF:-1"
"tvg-id"
"tvg-name"
"tvg-logo"
"group-title"
"playlist.m3u"
"playlist.m3u8"
"channels.m3u"
"tv.m3u"
"index.m3u8"
"master.m3u8"
"live.m3u8"
"chunklist.m3u8"
"#EXT-X-STREAM-INF"
"#EXT-X-TARGETDURATION"
"#EXT-X-MEDIA-SEQUENCE"
"xmltv"
"epg.xml"
"guide.xml"
"xmltv.xml"
"epg.xml.gz"
"programme start"
"channel id"
"FAST channels m3u"
"Pluto TV m3u8"
"Plex Live TV m3u8"
"Samsung TV Plus m3u8"
"LG Channels m3u8"
"Rakuten TV m3u8"
"public broadcaster m3u8"
"official live stream m3u8"
"government tv live stream"
"parliament tv live m3u8"
"public access tv m3u8"
"university tv live m3u8"
"radio m3u playlist"
"visual radio m3u8"
"Jellyfin m3u tuner"
"Threadfin m3u xmltv"
"xTeVe m3u xmltv"
"Tvheadend IPTV automatic network"
```

---

# 75. Recommended Full Workflow

Use this process every time:

```text
1. Search using exact IPTV terms.
2. Prefer official/public/free/legal sources.
3. Find raw M3U/M3U8/XMLTV URLs.
4. Confirm the source domain and legality.
5. Test playlist download with browser/curl.
6. Test playback in VLC.
7. Test stream with ffprobe.
8. Check for DRM, tokens, cookies, login, and geo-restrictions.
9. Add source to your spreadsheet.
10. Import into Threadfin/xTeVe.
11. Remove dead/unwanted channels.
12. Map XMLTV EPG.
13. Export cleaned playlist.
14. Add cleaned source to Jellyfin.
15. Schedule regular checks.
```

---

# 76. Jellyfin Setup Summary

Recommended Jellyfin setup:

```text
Admin Dashboard
  → Live TV
  → Add tuner device
  → M3U tuner
  → Paste playlist URL
  → Add XMLTV guide data
  → Refresh guide
  → Map channels if needed
```

Better setup:

```text
Raw public playlists
  → Threadfin/xTeVe
  → Clean and map
  → Jellyfin
```

---

# 77. Spreadsheet Columns to Track Sources

Use these columns:

```csv
Source,Direct raw URL(s),Type,Legality,note,Last updated seen,Reliability and usage notes,Tags,Country,Language,Category,EPG URL,Channel count,Tested in VLC,Tested in ffprobe,Tested in Jellyfin,Status,Date tested
```

Status examples:

```text
Working
Partially working
Dead
Geo-blocked
Tokenized
Requires headers
EPG only
Playlist only
Needs proxy
Unverified
Rejected - legal concern
```

---

# 78. Final Safety and Quality Rules

Use sources that are:

- Public
- Official
- Free-to-air
- Government/public access
- Educational
- Free ad-supported
- Openly documented
- Clearly legal

Avoid sources that are:

- Pirated
- Premium bundles
- Credential dumps
- Paywall bypasses
- DRM bypasses
- Subscription leaks
- Private provider playlists
- Reseller panel exports
- “VIP IPTV” lists

Knowledge is useful when it is clean, verifiable, and responsibly used.

---

# 79. Quick Glossary

| Term | Meaning |
|---|---|
| IPTV | TV delivered over IP networks |
| M3U | Playlist file format |
| M3U8 | UTF-8 M3U; common for HLS |
| HLS | HTTP Live Streaming |
| EPG | Electronic Program Guide |
| XMLTV | XML TV guide format |
| FAST | Free Ad-Supported Streaming TV |
| Tuner | Live TV input source |
| Raw URL | Direct file URL, not web page |
| Proxy | Tool that filters/relays playlists |
| Tokenized stream | URL that expires |
| DRM | Digital Rights Management |
| Geo-blocked | Restricted by region |
| tvg-id | M3U field used for guide matching |
| group-title | M3U category/group field |
| master playlist | HLS playlist pointing to variants |
| media playlist | HLS playlist pointing to segments |

---

# 80. Short Answer

These are usually called:

```text
IPTV playlists
M3U playlists
M3U8 playlists
HLS streams
Live TV sources
M3U tuner sources
FAST channel playlists
XMLTV/EPG guide sources
```

The most manual way to find them is:

```text
Search GitHub/search engines for EXTM3U, M3U, M3U8, XMLTV, EPG
Inspect official broadcaster live pages with browser Network tools
Search FAST/public broadcaster/government/education sources
Validate with VLC, ffprobe, Threadfin/xTeVe, then Jellyfin
Track everything in a source registry
```

