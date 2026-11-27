# tests

release checks: the userscript runs on simulated x.com pages in headless chromium, for the old design (`fixture.html`) and the redesigned website (`fixture_new.html`). photos are served locally, no real x traffic.

```
pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/suite.py
```

covers: viewer opening and loading order, the redesigned website (photo clicks, quoted posts, post button, key v, status pages), format fallback for downloads / zip, keyboard shortcuts, scrolling, dark / light mode, new-tab mode, japanese ui, settings window layout, lower-case text, fonts, and page errors.

runs automatically on every push (github actions → *tests*).
