# Tests

Release checks: the userscript runs on a simulated x.com page in headless Chromium (photos served locally, no real X traffic).

```
pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/suite.py
```

Covers: viewer opening and loading order, format fallback for downloads / ZIP, keyboard shortcuts, scrolling, dark / light mode, new-tab mode, Japanese UI, settings window layout, lower-case text, fonts, and page errors.

Runs automatically on every push (GitHub Actions → *tests*).
