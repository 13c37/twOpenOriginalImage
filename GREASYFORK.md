**maintained continuation of furyu's *twitter 原寸びゅー* (twitter view original images)**, which was discontinued and removed. earlier forks (coxxs) are no longer updated for x's changes.

<img src="https://raw.githubusercontent.com/13c37/twOpenOriginalImage/main/docs/demo.webp" alt="demo: open a photo, step through a post, download, switch to original size" width="800">

<sub>demo artwork: @shockyoupan, @hex_termina</sub>

**works on the new twitter / x layout** (the redesign rolling out since november 2026) **and the old one.** the script detects which one you have on every page load, nothing to set up.

### what's new compared to older versions
- works with posts that have **up to 20 photos** (older versions only picked up ~6)
- viewer opens instantly with a loading indicator
- redesigned settings: dark / light / auto theme, everything on one screen
- optional post button that matches x's own icons (off by default)
- lighter on the page: batched scans instead of running on every dom change

### usage
- **click** a photo → all originals on one page
- **alt + click** → one image per page
- **shift + click** → download the selected image
- in the viewer: **j** / **k** next / previous · **d** download · **z** zip · **s** size · **b** background · **esc** close
- settings: userscript manager menu → **settings**

### credits
original author: **furyu** ([website](https://memo.furyutei.com/) · [support furyu](https://memo.furyutei.com/about#send_donation)). versions 0.1.17–0.1.22 by coxxs. maintained by 13c37.

source & bug reports: [github.com/13c37/twOpenOriginalImage](https://github.com/13c37/twOpenOriginalImage)
