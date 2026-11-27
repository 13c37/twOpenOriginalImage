# twOpenOriginalImage

[![greasy fork version](https://img.shields.io/greasyfork/v/606352?label=Greasy%20Fork)](https://greasyfork.org/en/scripts/606352-twopenoriginalimage)
[![greasy fork installs](https://img.shields.io/greasyfork/dt/606352?label=installs)](https://greasyfork.org/en/scripts/606352-twopenoriginalimage)
[![license: mit](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

open and save images from x (twitter) in original size (`name=orig`). works on posts with up to 20 photos, on the new twitter / x layout (2026 redesign) and the old one.

![demo: open a photo, step through a post, download, switch to original size](docs/demo.webp)

<sub>demo recorded on the old layout; the viewer looks the same on the new one. demo artwork: [@shockyoupan](https://x.com/shockyoupan), [@hex_termina](https://x.com/hex_termina).</sub>

**actively maintained.** continuation of furyu's *twitter 原寸びゅー* (twOpenOriginalImage), which was discontinued at 0.1.16.

## install

1. install a userscript manager: [violentmonkey](https://violentmonkey.github.io/), [tampermonkey](https://www.tampermonkey.net/) or [scriptcat](https://docs.scriptcat.org/en/).
2. install the script from **[greasy fork](https://greasyfork.org/en/scripts/606352-twopenoriginalimage)** or from the [latest github release](https://github.com/13c37/twOpenOriginalImage/releases/latest/download/twOpenOriginalImage.user.js) ([all releases](https://github.com/13c37/twOpenOriginalImage/releases))

updates arrive automatically through your userscript manager.

## usage

click any photo in a post (or enable the icon button under *post button* in settings):

| action | default |
|---|---|
| all images on one page | click |
| one image per page | <kbd>alt</kbd> + click |
| download selected image | <kbd>shift</kbd> + click |

in the viewer: <kbd>j</kbd> / <kbd>k</kbd> next / previous · <kbd>d</kbd> download · <kbd>z</kbd> zip · <kbd>s</kbd> size · <kbd>b</kbd> background · <kbd>esc</kbd> close.

settings: userscript manager menu → **settings**. theme (dark / light / auto) is under *general*.

<img src="docs/settings.png" alt="settings window" width="720">

## bugs

open an [issue](https://github.com/13c37/twOpenOriginalImage/issues) with the post url and your browser + userscript manager.

## changelog

### 0.1.40
- fixed: opening a later photo of a post scrolled visibly through the other photos; the viewer now opens right on the clicked one.

### 0.1.39
- script description mentions the new twitter / x layout; the japanese one no longer mentions tweetdeck.

### 0.1.38
- works on x's redesigned website (being rolled out since november 2026); the old design keeps working.

### 0.1.37
- viewer and download buttons use x's font, matching the settings window and post button.

### 0.1.36
- viewer opens immediately with a loading indicator; the clicked photo loads first. much faster on posts with many photos.
- classic compact viewer bar restored.
- interface text is lower case throughout.
- fixed: mouse wheel over the viewer could scroll the page behind it.

### 0.1.35
- fixed: settings content overlapping the title bar and buttons when *see-through panel* is on.

### 0.1.34
- faster viewer: photos decode in the background and the clicked photo is loaded first.
- loading spinner bundled with the script.

### 0.1.33
- greasy fork no longer shows a donation link to the maintainer; furyu's link stays in credits and settings.

### 0.1.32
- uses `@match` instead of `@include` (https only).

### 0.1.31
- removed the obsolete tweetdeck match.

### 0.1.30
- post button is off by default and shows only an icon unless a label is set. clicking a photo opens the original.

### 0.1.28
- fixed: post button stayed highlighted after closing the viewer.
- new option: see-through settings panel.

### 0.1.27
- on opened posts, the button sits in the action bar next to reply / repost / like.

### 0.1.26
- post button and settings follow x's look (font, colours, switches); settings laid out in two columns.

### 0.1.25
- settings fit on one screen with clearer names; obsolete tweetdeck options hidden.
- lower cpu use: page scans are batched instead of running on every page change.

### 0.1.24
- new settings window with dark / light / auto theme. click outside or press <kbd>esc</kbd> to close.

### 0.1.23
- supports posts with up to 20 photos.

### 0.1.17 – 0.1.22 (coxxs)
- `x.com` support, layout fixes, configurable click actions, `name=orig` url handling.

### ≤ 0.1.16 (furyu)
- original script.

## credits

- **[furyu](https://github.com/furyutei)** — original author (2016–). donations: <https://memo.furyutei.com/about#send_donation>
- **coxxs** — maintained 0.1.17–0.1.22
- **13c37** — current maintainer (0.1.23+)

## license

[mit](LICENSE). original copyright © 2016 furyu; bundled libraries keep their own notices (see the script header).
