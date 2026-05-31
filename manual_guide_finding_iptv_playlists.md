# Manual Guide to Finding IPTV Playlists, M3U/M3U8 Streams, and EPG Sources

## Purpose

This guide explains what IPTV playlist sources are called, how they work, and how to manually find legal/free/public playlist sources that can be used with Jellyfin, Threadfin, xTeVe, Tvheadend, Kodi, VLC, or similar media tools.

This document focuses on **legal/public/free-to-air/official/free ad-supported TV sources**. Avoid using pirated, credential-leaked, paid-provider, or unauthorized rebroadcast playlists.

---

## 1. What These Sources Are Called

When searching manually, use the correct terminology. Different communities and tools use different names for the same or related things.

| Term | Meaning | Typical File/URL |
|---|---|---|
| IPTV playlist | A list of live TV channels or streams | `.m3u`, `.m3u8` |
| M3U playlist | Plain text playlist containing media URLs | `.m3u` |
| M3U8 playlist | UTF-8 encoded M3U playlist, commonly used for HLS streams | `.m3u8` |
| HLS stream | HTTP Live Streaming stream; often used by live TV websites | `master.m3u8`, `playlist.m3u8`, `index.m3u8` |
| Master playlist | HLS playlist that points to multiple quality variants | `master.m3u8` |
| Media playlist | HLS playlist that points to video/audio segments | `.ts`, `.m4s`, `.mp4` segment URLs |
| XMLTV | XML format used for TV guide data | `.xml`, `.xml.gz` |
| EPG | Electronic Program Guide; schedule/guide data | XMLTV source |
| FAST channels | Free Ad-Supported Streaming TV channels | Pluto TV, Plex, Samsung TV Plus, etc. |
| OTT streams | Online TV streams delivered over the internet | HLS/DASH streams |
| Public broadcaster stream | Official stream from a TV/radio/news/government/broadcaster website | Usually `.m3u8` |
| Tuner source | Playlist URL added into Jellyfin/Threadfin/Tvheadend as a TV tuner | M3U URL |
| Live TV source | Generic name used by apps for channel playlists | M3U/M3U8 |
| Channel list | Human-friendly term for IPTV playlist | M3U |
| TV guide source | EPG/XMLTV data source | XML/XML.GZ |
| Stream aggregator | Website or repository that collects public stream links | GitHub repo/site |
| Playlist proxy | Tool that cleans, maps, filters, and republishes IPTV playlists | Threadfin, xTeVe, Telly |
| Xtream Codes API | Provider-style IPTV API format | Server URL + username + password |
| DASH stream | MPEG-DASH streaming format, alternative to HLS | `.mpd` |
| RTMP stream | Older streaming protocol sometimes still used | `rtmp://...` |
| RTSP stream | Often used by cameras or internal streams | `rtsp://...` |

---

## 2. What Jellyfin Usually Needs

For Jellyfin Live TV, you normally need:

1. **M3U tuner URL**
   - This is the playlist/channel list.
   - Example format:
     ```text
     https://example.com/playlist.m3u
     ```

2. **XMLTV / EPG URL**
   - This is the guide/schedule data.
   - Example format:
     ```text
     https://example.com/guide.xml.gz
     ```

3. Optional proxy/manager:
   - Threadfin
   - xTeVe
   - Telly
   - Tvheadend

Recommended flow:

```text
Playlist sources + EPG sources
        ↓
Threadfin / xTeVe / Tvheadend
        ↓
Jellyfin Live TV
        ↓
Clients: browser, Android TV, mobile, Kodi, etc.
```

---

## 3. Common File and URL Patterns

When manually searching, look for these patterns:

```text
.m3u
.m3u8
.xml
.xml.gz
.json
master.m3u8
playlist.m3u8
index.m3u8
live.m3u8
channels.m3u
tv.m3u
iptv.m3u
playlist.m3u
guide.xml
epg.xml
xmltv.xml
```

Common HLS stream filenames:

```text
master.m3u8
index.m3u8
playlist.m3u8
chunklist.m3u8
variant.m3u8
live.m3u8
stream.m3u8
```

Common video segment patterns:

```text
.ts
.m4s
.mp4
aac
vtt
```

---

## 4. Manual Discovery Method 1: GitHub Search

GitHub is one of the best places to find public IPTV playlist repositories.

### Search terms

Use GitHub search with these queries:

```text
iptv playlist
m3u playlist
m3u8 playlist
live tv m3u
public iptv
free iptv
legal iptv
EXTM3U
#EXTINF
tvg-id
tvg-logo
xmltv
epg xmltv
```

### Advanced GitHub search

Search by file extension:

```text
extension:m3u iptv
extension:m3u8 iptv
extension:xml xmltv
extension:json iptv
filename:playlist.m3u
filename:playlist.m3u8
filename:tv.m3u
filename:channels.m3u
filename:epg.xml
filename:guide.xml
```

Search by IPTV markers:

```text
"EXTM3U"
"#EXTINF"
"tvg-id"
"tvg-name"
"tvg-logo"
"group-title"
```

Search for country-specific playlists:

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
```

Search GitHub topics:

```text
https://github.com/topics/iptv
https://github.com/topics/m3u
https://github.com/topics/m3u8
https://github.com/topics/hls
https://github.com/topics/xmltv
https://github.com/topics/epg
https://github.com/topics/live-tv
```

### What to check in a GitHub repo

When you open a repo, check:

- Does it have `.m3u` or `.m3u8` files?
- Does the playlist start with `#EXTM3U`?
- Does it mention legal/public/free-to-air streams?
- When was the repository last updated?
- Are streams from official broadcaster domains?
- Does it include an EPG/XMLTV source?
- Are issues open about dead links?
- Does the README mention Jellyfin, Kodi, VLC, Tvheadend, xTeVe, or Threadfin?

### How to get raw GitHub playlist URLs

GitHub page URL:

```text
https://github.com/user/repo/blob/main/playlist.m3u
```

Raw URL:

```text
https://raw.githubusercontent.com/user/repo/main/playlist.m3u
```

For Jellyfin/Threadfin, use the **raw** URL, not the GitHub webpage URL.

---

## 5. Manual Discovery Method 2: GitLab, Codeberg, Gitea, and Other Git Hosts

Do not only search GitHub. Some playlists are hosted on other code platforms.

Search these platforms:

```text
GitLab
Codeberg
Gitea
SourceForge
Bitbucket
NotABug
Forgejo instances
Self-hosted Git servers
```

Search queries:

```text
site:gitlab.com iptv m3u
site:gitlab.com "EXTM3U"
site:codeberg.org iptv m3u
site:codeberg.org "EXTM3U"
site:bitbucket.org iptv m3u
site:sourceforge.net xmltv
```

Look for raw file links similar to GitHub raw links.

---

## 6. Manual Discovery Method 3: Google/Bing/DuckDuckGo Search Operators

Search engines can find playlist files directly.

### Basic search queries

```text
iptv m3u playlist
free legal iptv m3u
public iptv playlist
m3u8 live tv stream
xmltv epg source
free xmltv guide
```

### Filetype searches

```text
filetype:m3u iptv
filetype:m3u8 iptv
filetype:xml xmltv
filetype:gz xmltv
filetype:m3u live tv
filetype:m3u8 "live"
```

### URL pattern searches

```text
inurl:m3u8 live tv
inurl:playlist.m3u
inurl:playlist.m3u8
inurl:channels.m3u
inurl:tv.m3u
inurl:epg.xml
inurl:guide.xml
inurl:xmltv.xml
```

### Content marker searches

```text
"EXTM3U" "tvg-logo"
"EXTM3U" "group-title"
"EXTM3U" "tvg-id"
"#EXTINF:-1" "http"
"#EXT-X-STREAM-INF"
"#EXT-X-TARGETDURATION"
```

### Legal/public stream-focused queries

```text
official live stream m3u8
public live stream m3u8
free to air m3u8
government tv live stream m3u8
news channel live stream m3u8
public broadcaster live m3u8
```

### Search specific domains

```text
site:*.gov m3u8 live
site:*.edu m3u8 live
site:*.org m3u8 live tv
site:youtube.com/live official channel
site:tv "m3u8"
```

---

## 7. Manual Discovery Method 4: Browser Developer Tools

Many official broadcaster websites use HLS streams internally. You can inspect your browser network traffic to find the `.m3u8`.

### Steps

1. Open the broadcaster's official live TV page.
2. Press `F12` to open Developer Tools.
3. Go to the **Network** tab.
4. Start the video.
5. Filter network requests using:
   ```text
   m3u8
   ```
6. Look for:
   ```text
   master.m3u8
   playlist.m3u8
   index.m3u8
   ```
7. Right-click the request and copy the URL.
8. Test the URL in VLC or ffprobe.
9. If it works without cookies/tokens, it may be usable in Jellyfin/Threadfin.
10. If it requires short-lived tokens, cookies, or headers, it may not work reliably in Jellyfin.

### What to avoid

Do not bypass paywalls, DRM, subscriptions, geo-blocking, login systems, or encryption.

### Signs the stream may not work in Jellyfin

- URL has an expiring token.
- URL contains `signature=`, `token=`, `expires=`, `hdnts=`, `Policy=`, `Key-Pair-Id=`.
- Stream requires cookies.
- Stream requires special headers.
- Stream uses DRM.
- Stream only works inside the official website/app.
- Stream expires after minutes or hours.

---

## 8. Manual Discovery Method 5: VLC / Media Player Inspection

VLC can help test whether a stream is usable.

### Test a playlist

1. Open VLC.
2. Go to:
   ```text
   Media → Open Network Stream
   ```
3. Paste the M3U/M3U8 URL.
4. Confirm whether the channel plays.

### Check stream codec

In VLC:

```text
Tools → Codec Information
```

Look for:

- Video codec
- Audio codec
- Resolution
- Stream URL
- Bitrate

### Save or inspect playlist

If VLC opens a playlist, you can inspect the loaded playlist and verify individual channel URLs.

---

## 9. Manual Discovery Method 6: ffmpeg and ffprobe

Use `ffprobe` to test whether a stream is valid.

### Test a stream

```bash
ffprobe "https://example.com/live/master.m3u8"
```

### Test with timeout

```bash
ffprobe -rw_timeout 10000000 "https://example.com/live/master.m3u8"
```

### Test a playlist item

```bash
ffmpeg -i "https://example.com/live/master.m3u8" -t 10 -f null -
```

### What success looks like

A valid stream usually returns:

- Duration or live stream info
- Video stream
- Audio stream
- Codec details
- No 403/404/timeout error

### Common errors

| Error | Meaning |
|---|---|
| 403 Forbidden | Stream may require headers, cookies, token, or region |
| 404 Not Found | Dead link |
| 451 Unavailable | Geo-restricted/legal restriction |
| Invalid data found | Not a real media stream |
| Connection timed out | Server down or blocking |
| HTTP 302 loop | Redirect issue |
| DRM/encrypted errors | Not suitable for normal IPTV use |

---

## 10. Manual Discovery Method 7: Search Official Broadcaster Websites

Official broadcaster sites are often the safest legal sources.

Search for:

```text
official live stream
watch live
live tv
live channel
public livestream
24/7 live stream
```

Examples of broadcaster categories:

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

Manual workflow:

1. Find the official website.
2. Open the live page.
3. Use browser Developer Tools.
4. Filter `m3u8`.
5. Test the stream.
6. Confirm whether it is public and official.
7. Add it to a personal M3U playlist.

---

## 11. Manual Discovery Method 8: Search FAST Providers

FAST means **Free Ad-Supported Streaming TV**.

These providers often have free live channels:

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
KlowdTV free channels
Sling Freestream
Fubo Free
TCL Channel
Vizio WatchFree+
```

Search queries:

```text
Pluto TV m3u8 playlist
Plex live tv m3u8
Samsung TV Plus m3u8
LG Channels m3u8
Rakuten TV m3u8
FAST channels m3u
FAST playlist m3u8
```

Important notes:

- Some FAST playlists are community-maintained.
- Some providers use region-specific channel lineups.
- Some streams may include ad markers.
- Some streams may break if provider APIs change.
- Some require playlist generators rather than static files.

---

## 12. Manual Discovery Method 9: Search Known IPTV Aggregators

Search for public IPTV aggregators and index projects.

Useful search terms:

```text
IPTV aggregator
public IPTV list
legal IPTV playlist
free-to-air IPTV playlist
open IPTV playlist
awesome IPTV
iptv github list
```

Common aggregator types:

```text
GitHub repositories
Playlist indexes
FAST playlist generators
Country playlist sites
Public stream databases
EPG databases
Community forums
Kodi addon source lists
Tvheadend source collections
```

When using aggregators, always verify the legality and source of each stream.

---

## 13. Manual Discovery Method 10: Search by Country or Language

Country-specific playlists are very common.

Search pattern:

```text
[country] iptv m3u
[country] live tv m3u8
[country] free tv channels m3u
[country] public tv m3u
[language] iptv playlist
```

Examples:

```text
pakistan iptv m3u
india iptv m3u
arabic iptv m3u
urdu iptv m3u
turkish iptv m3u
spanish iptv m3u
french iptv m3u
german iptv m3u
uk iptv m3u
usa iptv m3u
canada iptv m3u
```

Better legal-focused searches:

```text
pakistan official live stream m3u8
india public broadcaster live m3u8
uk parliament live stream m3u8
usa local tv live stream m3u8
```

---

## 14. Manual Discovery Method 11: Search by Category

Search by content category:

```text
news live m3u8
weather live m3u8
sports news live m3u8
business news live m3u8
religious tv live m3u8
kids tv live m3u8
music tv live m3u8
parliament tv live m3u8
government tv live m3u8
education tv live m3u8
local tv live m3u8
```

Legal/public categories that are easier to find:

```text
News
Weather
Government
Parliament
Education
Religion
NASA/science
Public access TV
Local municipality channels
University channels
Radio/visual radio
```

Be careful with:

```text
Premium sports
Paid movie channels
Cable-only networks
Pay-per-view
Subscription channels
Adult content
Pirated packages
```

---

## 15. Manual Discovery Method 12: YouTube Live and Streamlink

Some official channels broadcast on YouTube Live. Jellyfin usually does not directly use YouTube URLs as M3U channels, but tools like Streamlink can resolve or restream them.

Search:

```text
official YouTube live news channel
official YouTube live TV
official 24/7 live stream
```

Tools:

```text
Streamlink
yt-dlp
FFmpeg
```

Example concept:

```text
Official YouTube Live URL
        ↓
Streamlink extracts playable stream
        ↓
Local relay/proxy
        ↓
M3U entry for Jellyfin/Threadfin
```

Important:

- YouTube stream URLs expire.
- Direct extracted URLs are usually short-lived.
- A local relay is more reliable than putting extracted URLs directly into Jellyfin.
- Respect YouTube and broadcaster terms.

---

## 16. Manual Discovery Method 13: Kodi Addons and PVR Sources

Kodi IPTV communities often list legal public stream sources.

Search:

```text
Kodi IPTV Simple Client m3u
Kodi legal IPTV addon
Kodi public TV m3u
Kodi PVR IPTV source
```

Check:

- Addon README files
- XML channel lists
- M3U files
- Source URLs used by addons

Do not use piracy addons or unauthorized paid channel bundles.

---

## 17. Manual Discovery Method 14: Tvheadend, xTeVe, Threadfin, and Telly Communities

These tools are commonly used with IPTV playlists. Their communities often share formatting tips and public playlist references.

Search:

```text
Threadfin m3u playlist
xTeVe m3u sources
Tvheadend IPTV automatic network m3u
Telly m3u xmltv
Jellyfin m3u tuner xmltv
```

Useful things to look for:

- Example M3U syntax
- XMLTV matching rules
- Channel mapping workflows
- Buffering/proxy settings
- Playlist cleanup scripts
- Dead-link checking scripts

---

## 18. Manual Discovery Method 15: EPG/XMLTV Discovery

An IPTV playlist gives you channels. EPG/XMLTV gives you schedules.

Search terms:

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

Search queries:

```text
filetype:xml xmltv
filetype:gz xmltv
inurl:epg.xml
inurl:xmltv.xml
inurl:guide.xml
"xmltv" "channel id"
"programme start" "programme stop" "channel="
```

Common EPG source types:

```text
Public XMLTV projects
Country-specific EPG generators
Provider-specific guide data
Community EPG repositories
Self-generated EPG using WebGrabPlus
Self-generated EPG using zap2xml
Self-generated EPG using xmltv grabbers
```

### EPG matching fields

M3U playlists often include:

```text
tvg-id
tvg-name
tvg-logo
group-title
```

XMLTV guide files include channel IDs. For guide matching, `tvg-id` should match the XMLTV channel ID.

Example M3U entry:

```m3u
#EXTM3U
#EXTINF:-1 tvg-id="Channel.ID" tvg-name="Channel Name" tvg-logo="https://example.com/logo.png" group-title="News",Channel Name
https://example.com/live/master.m3u8
```

---

## 19. Manual Discovery Method 16: Search Public APIs and JSON Feeds

Some services expose channel data through JSON APIs.

Search terms:

```text
iptv api
channel json
live tv json
m3u generator json
FAST api m3u8
playlist api m3u
```

Search queries:

```text
site:github.com iptv api json
site:github.com channels.json m3u8
site:github.com streams.json iptv
"streams.json" "m3u8"
"channels.json" "tvg"
```

Workflow:

1. Find JSON/API feed.
2. Inspect whether it contains stream URLs.
3. Convert stream list into M3U.
4. Match with XMLTV if available.
5. Test in VLC/ffprobe.
6. Add to Threadfin/Jellyfin.

---

## 20. Manual Discovery Method 17: Inspect Mobile/Web Apps Carefully

Some official broadcaster apps use public streaming endpoints.

Manual workflow:

1. Use official website first.
2. If the web player does not expose the stream, check whether the app has official documentation or public API.
3. Do not bypass encryption, DRM, login, paid access, or obfuscation.
4. Only use streams that are public and authorized.

Avoid:

```text
Credential extraction
App reverse engineering to bypass restrictions
DRM bypass
Token bypass
Paywall bypass
Geo-restriction bypass
Private API abuse
```

---

## 21. Manual Discovery Method 18: Search CDN Patterns

Many official streams are hosted on CDNs.

Common CDN/streaming host patterns:

```text
akamaihd.net
akamaized.net
cloudfront.net
fastly.net
llnwd.net
cdnvideo.ru
mux.com
jwplayer
brightcove
theoplayer
hls
live
stream
```

Search examples:

```text
site:akamaized.net m3u8 news live
site:cloudfront.net m3u8 live tv
site:fastly.net m3u8 live
"master.m3u8" "news"
"playlist.m3u8" "live"
```

Caution:

- A CDN URL alone does not prove legality.
- Always trace the stream back to an official broadcaster or authorized provider.

---

## 22. Manual Discovery Method 19: Search Internet Archive and Historical Lists

Sometimes old IPTV repos are archived or mirrored.

Search:

```text
site:webcache.googleusercontent.com iptv m3u
site:archive.org iptv m3u
site:archive.org xmltv
"iptv playlist" "archive"
```

Use this mainly to discover project names, not necessarily working links. Old stream links often die.

---

## 23. Manual Discovery Method 20: Community Forums and Subreddits

Search discussion communities for legal/public sources and tool configuration help.

Search terms:

```text
Jellyfin IPTV m3u
Threadfin playlist sources
xTeVe playlist sources
Tvheadend IPTV m3u
legal IPTV sources
public m3u playlist
```

Places to search:

```text
Jellyfin forums
Jellyfin subreddit
Kodi forums
Tvheadend forums
Linux media server forums
Home server communities
GitHub Discussions
Stack Overflow only for technical errors
```

Avoid communities that focus on pirated IPTV provider lists.

---

## 24. Manual Discovery Method 21: Public Access, Government, and Education Streams

These are often legal and publicly accessible.

Search queries:

```text
city council live stream m3u8
public access tv m3u8
government channel live stream
parliament live m3u8
senate live stream m3u8
university tv live stream m3u8
education channel live stream m3u8
```

Possible sources:

```text
City TV channels
State government TV
National parliament TV
University channels
Educational broadcasters
Public access networks
Local municipality channels
Court/government hearing streams
```

These sources may not always have polished EPG data, but they are often stable.

---

## 25. Manual Discovery Method 22: News and International Broadcasters

Many international news channels provide free live streams.

Search:

```text
official news live stream m3u8
international news channel m3u8
24 hour news live m3u8
world news live stream official
```

Common examples of public/free broadcaster categories:

```text
International news
Public broadcaster news
Business news
Weather news
Regional news
Multilingual news
```

Always use official broadcaster pages or clearly legal public playlists.

---

## 26. Manual Discovery Method 23: Radio and Visual Radio Streams

Some IPTV playlists include radio channels or visual radio streams.

Search:

```text
radio m3u playlist
visual radio m3u8
internet radio m3u
radio station live stream m3u
```

Formats may include:

```text
.m3u
.pls
.aac
.mp3
.m3u8
```

Jellyfin Live TV is focused on TV/video, but VLC/Kodi/Tvheadend may support many radio streams.

---

## 27. Manual Discovery Method 24: Use Playlist Generators

Some sources do not provide a static M3U but can generate one.

Search:

```text
iptv m3u generator
FAST m3u generator
Pluto TV m3u generator
Samsung TV Plus m3u generator
Plex m3u generator
```

Generator types:

```text
Web generator
GitHub Action generated playlist
Local script
Docker container
API-to-M3U converter
JSON-to-M3U converter
```

Things to check:

- Is it open source?
- Is it actively maintained?
- Does it generate EPG too?
- Does it support country/region filtering?
- Can it run locally?
- Does it require credentials?

---

## 28. Manual Discovery Method 25: Build Your Own M3U File

You can manually create a playlist from verified public stream URLs.

Example:

```m3u
#EXTM3U
#EXTINF:-1 tvg-id="NHKWorld.jp" tvg-name="NHK World" group-title="News",NHK World
https://example.com/nhk/index.m3u8

#EXTINF:-1 tvg-id="France24.en" tvg-name="France 24 English" group-title="News",France 24 English
https://example.com/france24/index.m3u8
```

Useful fields:

| Field | Purpose |
|---|---|
| `tvg-id` | Matches channel with XMLTV guide |
| `tvg-name` | Display/matching name |
| `tvg-logo` | Channel logo URL |
| `group-title` | Category/group in player |
| Channel name after comma | Display name |

---

## 29. Manual Discovery Method 26: Convert Lists to M3U

Sometimes you find URLs in text, JSON, CSV, or HTML instead of M3U.

You can convert:

```text
JSON → M3U
CSV → M3U
HTML table → M3U
Plain URL list → M3U
API response → M3U
```

Basic M3U structure:

```m3u
#EXTM3U
#EXTINF:-1,Channel Name
https://example.com/stream.m3u8
```

---

## 30. Manual Discovery Method 27: Check Existing Software Presets

Some apps include example playlists, tuner examples, or provider templates.

Search inside documentation for:

```text
m3u tuner
live tv
xmltv
playlist url
guide url
iptv source
```

Software to check:

```text
Jellyfin
Emby
Kodi IPTV Simple Client
Tvheadend
Threadfin
xTeVe
Telly
Channels DVR documentation
Plex DVR documentation
VLC
MPV
Streamlink
WebGrabPlus
```

---

## 31. Manual Discovery Method 28: Monitor Repository Updates

For active sources, check update frequency.

Look at:

```text
Last commit date
Release date
GitHub Actions date
Issues mentioning dead links
Pull requests
README update date
Generated playlist timestamp
EPG generation timestamp
```

Useful GitHub searches:

```text
"Generated at" "m3u"
"Last updated" "playlist.m3u"
"updated daily" "iptv"
"GitHub Actions" "iptv"
```

---

## 32. Manual Discovery Method 29: Validate Playlist Quality

Before adding a source to Jellyfin, validate it.

Checklist:

- Playlist opens in browser or downloads.
- File starts with `#EXTM3U`.
- Channels have `#EXTINF`.
- Stream URLs are HTTP/HTTPS.
- No suspicious credentials in URL.
- No obvious piracy branding.
- Streams play in VLC.
- Streams play in ffmpeg/ffprobe.
- EPG is available or can be mapped.
- Logos are valid.
- Channels are grouped properly.
- Channel count is reasonable.
- Dead channels are removed.
- Region restrictions are understood.
- Source is actively maintained.

---

## 33. Manual Discovery Method 30: Validate Legal Status

Use this legal sanity checklist:

### Safer signs

```text
Official broadcaster domain
Government/public broadcaster source
Free ad-supported platform
Openly documented public stream
Free-to-air channel
Public access channel
Educational/government stream
Repository claims public/legal streams only
```

### Red flags

```text
Premium cable channels for free
Pay-per-view channels
Sports packages for free
Thousands of paid channels
Xtream credentials shared publicly
URLs containing username/password
Telegram/Discord reseller lists
"VIP IPTV"
"premium IPTV free"
"all countries all channels"
Adult/piracy bundles
Channels from paid providers without authorization
```

If unsure, do not use it.

---

## 34. Manual Discovery Method 31: Use Link Checkers and Playlist Validators

Useful checks:

```bash
curl -I "https://example.com/playlist.m3u"
curl -L "https://example.com/playlist.m3u" | head
ffprobe "https://example.com/stream.m3u8"
ffmpeg -i "https://example.com/stream.m3u8" -t 5 -f null -
```

Check HTTP status:

| Status | Meaning |
|---|---|
| 200 | Good |
| 301/302 | Redirect; may still work |
| 403 | Forbidden |
| 404 | Dead link |
| 410 | Gone |
| 451 | Legal/geo restriction |
| 5xx | Server problem |

---

## 35. Manual Discovery Method 32: Use Region Testing

Some streams work only in certain countries.

Test from:

```text
Your home network
Your server network
Your mobile network
Your VPS region
A legal VPN location, if allowed by provider terms
```

Do not bypass region restrictions if the provider does not allow it.

---

## 36. Manual Discovery Method 33: Track Sources in a Spreadsheet

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
Channel count
EPG URL
Country
Language
Category
Tested in VLC
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
```

---

## 37. Manual Discovery Method 34: Use Threadfin/xTeVe as a Filter Layer

Do not feed huge playlists directly into Jellyfin if they contain thousands of channels.

Recommended process:

1. Add source playlist to Threadfin/xTeVe.
2. Remove dead channels.
3. Remove unwanted countries/categories.
4. Map EPG.
5. Normalize channel names.
6. Export cleaned M3U.
7. Add cleaned M3U tuner to Jellyfin.

Benefits:

```text
Cleaner Jellyfin channel list
Better EPG matching
Less scan time
Fewer dead channels
Better grouping
Easier channel numbering
```

---

## 38. Manual Discovery Method 35: Search for Logos and Channel Metadata

Useful search terms:

```text
channel logos github
iptv logos
tvg-logo
channel database
iptv channel database
```

Metadata fields:

```text
Channel name
Country
Language
Category
Logo
Website
EPG ID
Alternative names
Broadcast region
```

Good metadata improves Jellyfin display and guide matching.

---

## 39. Manual Discovery Method 36: Use Existing Public Channel Databases

Search for:

```text
iptv channel database
public channel database
channels.json iptv
streams.json iptv
logos.json iptv
epg database iptv
```

These databases may not be playlists themselves, but they help with:

```text
Channel IDs
EPG IDs
Logos
Categories
Country codes
Language codes
Alternative names
Official websites
```

---

## 40. Manual Discovery Method 37: Watch for Tokenized Streams

Some `.m3u8` URLs work only temporarily.

Signs:

```text
expires=
token=
signature=
sig=
hdnts=
Policy=
Key-Pair-Id=
X-Amz-Signature=
X-Amz-Expires=
jwt=
auth=
```

These links are poor for Jellyfin unless you use an authorized generator or proxy that refreshes them.

---

## 41. Manual Discovery Method 38: Identify DRM-Protected Streams

DRM streams usually will not work in normal IPTV tools.

Signs:

```text
Widevine
FairPlay
PlayReady
license server
EXT-X-KEY
SAMPLE-AES
encrypted
DRM
.mpd with license
```

Avoid trying to bypass DRM.

---

## 42. Manual Discovery Method 39: Search for Public Test Streams

Public test streams are useful for testing your setup, not for building a channel lineup.

Search:

```text
public HLS test stream
m3u8 test stream
sample HLS stream
apple bipbop m3u8
video test m3u8
```

Use these to verify:

```text
Jellyfin tuner works
Threadfin proxy works
VLC playback works
Network access works
```

---

## 43. Manual Discovery Method 40: Use RSS/Sitemap/HTML Scraping for Official Sites

Some official broadcaster pages list live URLs in HTML, JavaScript, RSS, or sitemap files.

Search or inspect:

```text
view-source:
sitemap.xml
robots.txt
RSS feeds
JavaScript files
embedded player configs
JSON config files
```

Browser search inside page source:

```text
m3u8
hls
stream
live
source
video
playlist
```

Do not bypass security, private APIs, login, DRM, or paywalls.

---

## 44. Manual Discovery Method 41: Search Package Managers and Docker Images

Some playlist generators are distributed as Docker images or packages.

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

Places to check:

```text
Docker Hub
GitHub Container Registry
npm
PyPI
Homebrew
Linux package repos
```

---

## 45. Manual Discovery Method 42: Search GitHub Actions Artifacts and Generated Pages

Some projects generate playlists daily using GitHub Actions and publish to GitHub Pages.

Search:

```text
site:github.io iptv m3u
site:github.io playlist.m3u
site:github.io epg.xml.gz
"workflow" "playlist.m3u"
"github actions" "epg.xml"
```

Look for URLs like:

```text
https://username.github.io/repo/playlist.m3u
https://username.github.io/repo/epg.xml.gz
```

---

## 46. Manual Discovery Method 43: Search Raw Content CDNs

Some public lists are served from raw file CDNs.

Search:

```text
site:raw.githubusercontent.com "EXTM3U"
site:raw.githubusercontent.com "tvg-id"
site:cdn.jsdelivr.net "EXTM3U"
site:gitcdn.link "EXTM3U"
site:raw.githack.com "EXTM3U"
```

Common raw hosting patterns:

```text
raw.githubusercontent.com
cdn.jsdelivr.net/gh/
github.io
gitlab.com/.../-/raw/
codeberg.org/.../raw/
```

---

## 47. Manual Discovery Method 44: Search for Playlist Mirrors

Some projects mirror playlists across multiple locations.

Search:

```text
"playlist.m3u" "mirror"
"iptv m3u mirror"
"m3u8 mirror"
"backup playlist"
```

Mirrors can help when one URL is unavailable, but verify the mirror is trustworthy.

---

## 48. Manual Discovery Method 45: Use Local Network Tuners and HDHomeRun

If your goal is Jellyfin Live TV, you are not limited to internet IPTV.

Other tuner sources:

```text
HDHomeRun
DVB tuner
ATSC tuner
ISDB tuner
Satellite tuner
CableCARD where supported
Tvheadend tuner backend
SAT>IP
```

These provide legal local/OTA channels depending on your region and hardware.

---

## 49. Manual Discovery Method 46: Convert OTA/Tuner Channels to IPTV

Tools like Tvheadend can expose tuner channels as network streams.

Flow:

```text
Physical tuner / OTA antenna
        ↓
Tvheadend
        ↓
M3U playlist output
        ↓
Jellyfin / Kodi / VLC
```

This is useful when you want both local TV and internet IPTV in one interface.

---

## 50. Manual Discovery Method 47: Check Player Compatibility

Before finalizing a source, test in multiple tools:

```text
VLC
MPV
ffprobe
Threadfin
xTeVe
Tvheadend
Jellyfin
Kodi IPTV Simple Client
```

A stream that works in VLC may not always work in Jellyfin if it needs special headers, has codec issues, or uses unusual playlist formatting.

---

## 51. Manual Discovery Method 48: Search for Header Requirements

Some streams need custom HTTP headers.

Search terms:

```text
m3u8 user-agent required
m3u8 referer required
iptv m3u user agent
hls referer header
```

Common required headers:

```text
User-Agent
Referer
Origin
Cookie
Authorization
```

Jellyfin support for custom headers may be limited depending on setup. Threadfin, xTeVe, Streamlink, or a local proxy may help when the use is legitimate and allowed.

---

## 52. Manual Discovery Method 49: Keep a Dead-Link Refresh Routine

IPTV links change frequently. Maintain a schedule:

```text
Daily: check critical playlists
Weekly: scan full playlist
Monthly: remove dead channels
Monthly: verify EPG mapping
Quarterly: review legality/source status
```

Track:

```text
Date tested
HTTP status
Playback result
EPG match
Notes
Replacement URL
```

---

## 53. Manual Discovery Method 50: Build a Personal Source Registry

Create your own master registry.

Recommended format:

```csv
Source,Direct raw URL(s),Type,Legality,note,Last updated seen,Reliability and usage notes,Tags
```

Add extra operational fields:

```csv
Country,Language,Category,EPG URL,Status,Date tested,Channel count,Tool tested
```

This avoids losing sources and helps you rebuild Jellyfin quickly.

---

## 54. Good Search Query Library

Copy/paste these searches.

### General IPTV playlist searches

```text
"EXTM3U" "tvg-logo"
"EXTM3U" "group-title"
"EXTM3U" "tvg-id"
"iptv" "playlist.m3u"
"iptv" "playlist.m3u8"
"live tv" "m3u8"
"public iptv" "m3u"
"legal iptv" "m3u"
"free to air" "m3u8"
```

### GitHub searches

```text
site:github.com "EXTM3U"
site:github.com "tvg-id"
site:github.com "playlist.m3u"
site:github.com "playlist.m3u8"
site:raw.githubusercontent.com "EXTM3U"
site:github.io "iptv" "m3u"
```

### EPG searches

```text
"xmltv" "programme start"
"xmltv" "channel id"
"inurl:epg.xml"
"inurl:xmltv.xml"
"inurl:guide.xml"
"epg.xml.gz"
"xmltv.xml.gz"
```

### HLS searches

```text
"master.m3u8" "live"
"playlist.m3u8" "live"
"index.m3u8" "live"
"#EXT-X-STREAM-INF"
"#EXT-X-TARGETDURATION"
```

### Official broadcaster searches

```text
"official live stream" "m3u8"
"public broadcaster" "live stream" "m3u8"
"government tv" "live stream"
"parliament tv" "m3u8"
"city council" "live stream" "m3u8"
```

### FAST searches

```text
"Pluto TV" "m3u8"
"Plex Live TV" "m3u8"
"Samsung TV Plus" "m3u8"
"LG Channels" "m3u8"
"Rakuten TV" "m3u8"
"FAST channels" "m3u"
"FAST playlist" "m3u8"
```

---

## 55. Recommended Legal Source Categories to Prioritize

Prioritize:

```text
IPTV-org style public stream projects
Official broadcaster websites
Government/public access streams
Public broadcasters
FAST TV sources
Educational/university channels
News channels with official live feeds
EPG/XMLTV open projects
Your own OTA/DVB/HDHomeRun tuner
```

Avoid:

```text
Pirated premium channel bundles
Shared paid IPTV credentials
Reseller panels
Telegram dumps
Suspicious "all channels free" lists
DRM-protected content
Paywall bypasses
Credential/token leakage
```

---

## 56. How to Add Sources to Jellyfin

General steps:

1. Open Jellyfin Admin Dashboard.
2. Go to Live TV.
3. Add a tuner device.
4. Choose M3U tuner.
5. Paste the playlist raw URL.
6. Add XMLTV guide data if available.
7. Refresh guide data.
8. Map channels if needed.
9. Test playback.

Better production setup:

```text
Raw playlist source
        ↓
Threadfin/xTeVe cleanup
        ↓
Clean playlist URL
        ↓
Jellyfin M3U tuner
```

---

## 57. How to Add Sources to Threadfin/xTeVe

General steps:

1. Add M3U playlist source.
2. Add XMLTV source.
3. Scan channels.
4. Disable unwanted channels.
5. Map EPG IDs.
6. Assign channel numbers.
7. Export cleaned M3U and XMLTV.
8. Add Threadfin/xTeVe output to Jellyfin.

---

## 58. Final Practical Workflow

Use this repeatable process:

```text
1. Search GitHub/GitLab/search engines using IPTV terms.
2. Find raw M3U/M3U8/XMLTV URLs.
3. Verify source legality.
4. Test in browser/curl.
5. Test in VLC.
6. Test in ffprobe.
7. Check update frequency.
8. Add source to spreadsheet.
9. Import into Threadfin/xTeVe.
10. Remove dead/unwanted channels.
11. Map XMLTV guide.
12. Export cleaned tuner source.
13. Add to Jellyfin.
14. Schedule periodic validation.
```

---

## 59. Quick Glossary

| Word | Meaning |
|---|---|
| IPTV | Internet Protocol Television |
| M3U | Playlist file format |
| M3U8 | UTF-8 M3U, common for HLS |
| HLS | HTTP Live Streaming |
| EPG | Electronic Program Guide |
| XMLTV | XML format for TV listings |
| FAST | Free Ad-Supported Streaming TV |
| Tuner | Source Jellyfin uses for Live TV |
| Stream URL | Direct URL to media stream |
| Playlist URL | URL to many stream entries |
| Raw URL | Direct file URL, not webpage |
| Proxy | Middle layer that cleans or relays streams |
| Tokenized stream | Stream URL that expires |
| DRM | Digital Rights Management |

---

## 60. Important Reminder

Finding a `.m3u8` URL does not automatically mean it is legal, stable, or allowed for redistribution. Prefer official, public, free-to-air, public broadcaster, government, educational, and authorized FAST sources. Avoid paid/premium/pirated sources and do not bypass DRM, login systems, paywalls, or geo-restrictions.

