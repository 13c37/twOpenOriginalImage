# twOpenOriginalImage

Open and save images from X (Twitter) in original size (`name=orig`). Works on posts with up to 20 photos.

**Actively maintained.** Continuation of furyu's *Twitter 原寸びゅー* (twOpenOriginalImage), which was discontinued at 0.1.16.

## Install

1. Install a userscript manager: [Violentmonkey](https://violentmonkey.github.io/), [Tampermonkey](https://www.tampermonkey.net/) or [ScriptCat](https://docs.scriptcat.org/en/).
2. Install the script: [twOpenOriginalImage.user.js](https://github.com/13c37/twOpenOriginalImage/raw/main/twOpenOriginalImage.user.js)

Updates arrive automatically through your userscript manager.

## Usage

Hover a post with images and use the **Original** button:

| Action | Default |
|---|---|
| All images on one page | Click |
| One image per page | <kbd>Alt</kbd> + Click |
| Download selected image | <kbd>Shift</kbd> + Click |

Actions can be changed in the userscript menu → Settings.

## Bugs

Open an [issue](https://github.com/13c37/twOpenOriginalImage/issues) with the post URL and your browser + userscript manager.

## Changelog

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
