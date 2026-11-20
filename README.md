# twOpenOriginalImage

[![Greasy Fork version](https://img.shields.io/greasyfork/v/606352?label=Greasy%20Fork)](https://greasyfork.org/en/scripts/606352-twopenoriginalimage)
[![Greasy Fork installs](https://img.shields.io/greasyfork/dt/606352?label=installs)](https://greasyfork.org/en/scripts/606352-twopenoriginalimage)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Open and save images from X (Twitter) in original size (`name=orig`). Works on posts with up to 20 photos.

**Actively maintained.** Continuation of furyu's *Twitter 原寸びゅー* (twOpenOriginalImage), which was discontinued at 0.1.16.

## Install

1. Install a userscript manager: [Violentmonkey](https://violentmonkey.github.io/), [Tampermonkey](https://www.tampermonkey.net/) or [ScriptCat](https://docs.scriptcat.org/en/).
2. Install the script from **[Greasy Fork](https://greasyfork.org/en/scripts/606352-twopenoriginalimage)** or directly from GitHub: [twOpenOriginalImage.user.js](https://github.com/13c37/twOpenOriginalImage/raw/main/twOpenOriginalImage.user.js)

Updates arrive automatically through your userscript manager.

## Usage

Click any photo in a post (or enable the icon button under *Post button* in Settings):

| Action | Default |
|---|---|
| All images on one page | Click |
| One image per page | <kbd>Alt</kbd> + Click |
| Download selected image | <kbd>Shift</kbd> + Click |

Settings: userscript manager menu → **Settings**. Theme (dark / light / auto) is under *General*.

## Bugs

Open an [issue](https://github.com/13c37/twOpenOriginalImage/issues) with the post URL and your browser + userscript manager.

## Changelog

### 0.1.36 — instant viewer, old look back
- **Opens instantly on 20-photo posts.** Before, every photo was downloaded one after another just to check its file format, and only then did the viewer open (≈8 s of nothing in a test with 20 photos). Now the viewer opens at once with a spinner and "loading… 3 / 20"; the clicked photo downloads first on its own, the rest 3 at a time. Format fallback (jpg → png → gif) now happens per photo, only if one fails; downloads and ZIP still get the right file.
- **Old compact viewer bar is back** (`[j]next [k]previous … close [esc]`), dark/light following X.
- **All text in lower case**: viewer bar, settings window, button tooltips, download button.
- **Scrolling no longer leaks to X**: the wheel on the viewer's top bar did scroll the page behind it, and below the last photo (or on single-photo posts) scrolling down kept scrolling X. Cause: at 125% zoom a fractional height made the "already at the bottom" check fail.

### 0.1.35 — settings window fix
- With "See-through panel" on, settings scrolled under the title bar and the credits slid under Reset/Save/Close, so text overlapped. Now only the settings list scrolls; the title bar, credits and buttons stay fixed and nothing passes beneath them.
- The scrollbar sits only beside the settings list (thin, X colours) instead of running the full height of the window and into the rounded corners.

### 0.1.34 — image viewer
- **Opens faster**: the viewer appears as soon as the photo you clicked (and the ones above it) has loaded, instead of waiting for all photos. On 20-photo posts with full-size originals this is the biggest win. Photos further down still fit the screen when they arrive.
- **New header in X's style**: follows X dark/light mode, X font, keys shown as small labels (J Next, K Previous, D Download, S Size, B Background), round ✕ close. Labels collapse to keys on narrow windows.
- Loading spinner is now drawn locally (the old one was a 2016 image from Twitter's servers) and no longer flashes a white screen in dark mode.
- Images decode off the main thread (`decoding=async`), the clicked photo loads first (`fetchpriority=high`).
- Removed ~230 lines of commented-out old code.

### 0.1.33
- Removed `@contributionURL`: Greasy Fork showed it as "Thank 13c37 by making a donation" while it pointed to furyu. furyu's donation link stays in Credits and in the settings window.

### 0.1.32
- `@include` → `@match` (exact sites, https only; plain http redirects to https anyway).

### 0.1.31
- Removed the dead `tweetdeck.twitter.com` match (TweetDeck no longer exists).

### 0.1.30
- Post button is **off by default** (just click a photo — it opens the original). Turn it on under *Post button*.
- Label is **empty by default** = icon only, sized like X's own icons. Type a label (placeholder: "e.g. Original") to show text next to the icon.

### 0.1.29
- Post button off by default, icon only.

### 0.1.28
- Post button no longer stays highlighted after you click it and close the viewer.
- New *General → See-through panel*: settings window slightly transparent (no blur). On by default.

### 0.1.27
- Opened posts: the Original button now sits in the post's action bar (next to reply / repost / like), not under the timestamp.
- Settings: slightly smaller text; removed the duplicate theme button in the header (Theme lives in *General*).

### 0.1.26
- **Post button now looks like X's own actions**: X's font (Chirp), grey icon + label, blue hover circle. Empty label = icon only.
- **Settings in landscape** (two columns, no scrolling), ordered by importance: General → Post button → Viewer | Click actions → Downloads. Credits moved to the bottom.
- Settings use X's colours, font, pill buttons and switches. Turning the script off greys out every other option.

### 0.1.25
- Settings fit on one screen (no scrolling at 1080p / 1440p): compact grouped list — Click actions, Viewer, Button, Downloads, General.
- Clearer setting names; dead TweetDeck options hidden (TweetDeck is gone; defaults still apply).
- Removed the glass/blur option. Save is disabled until something changes; button label greys out when buttons are off.
- Performance: page scans are batched (max ~10/s) instead of running on every DOM change X makes; night-mode attribute only written when it changes.

### 0.1.24
- Redesigned settings dialog: dark / light / auto theme (toggle in the header), optional see-through glass panel, switches instead of checkboxes, scales from phone to 4K.
- Click outside the dialog or press <kbd>Esc</kbd> to close.
- Credits for the original author (furyu) with website and donation link are now shown in the dialog.

### 0.1.23
- Support posts with up to 20 photos (previously only the first ~6 were picked up). Photo list is read from the post data, with a fallback to the syndication API.

### 0.1.17 – 0.1.22 (Coxxs)
- `x.com` support, layout fixes, configurable click actions, dependency updates, `?name=orig` URL handling.

### ≤ 0.1.16 (furyu)
- Original script. 0.1.16 was furyu's final release.

## Credits

- **[furyu](https://github.com/furyutei)** — original author (2016–). Donations: <https://memo.furyutei.com/about#send_donation>
- **Coxxs** — maintained 0.1.17–0.1.22
- **13c37** — current maintainer (0.1.23+)

## License

[MIT](LICENSE). Original copyright © 2016 furyu; bundled libraries keep their own notices (see the script header).
