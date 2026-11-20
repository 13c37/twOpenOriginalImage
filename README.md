# twOpenOriginalImage

Open and save images from X (Twitter) in original size (`name=orig`). Works on posts with up to 20 photos.

**Actively maintained.** Continuation of furyu's *Twitter 原寸びゅー* (twOpenOriginalImage), which was discontinued at 0.1.16.

## Install

1. Install a userscript manager: [Violentmonkey](https://violentmonkey.github.io/), [Tampermonkey](https://www.tampermonkey.net/) or [ScriptCat](https://docs.scriptcat.org/en/).
2. Install the script: [twOpenOriginalImage.user.js](https://github.com/13c37/twOpenOriginalImage/raw/main/twOpenOriginalImage.user.js)

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

- **[furyu](https://github.com/furyutei)** — original author (2016–). Original repo: [furyutei/twOpenOriginalImage](https://github.com/furyutei/twOpenOriginalImage). Donations: <https://memo.furyutei.com/about#send_donation>
- **Coxxs** — maintained 0.1.17–0.1.22
- **13c37** — current maintainer (0.1.23+)

## License

[MIT](LICENSE). Original copyright © 2016 furyu; bundled libraries keep their own notices (see the script header).
