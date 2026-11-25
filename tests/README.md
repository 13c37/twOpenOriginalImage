# tests

release checks: the userscript runs on a simulated x.com page in headless chromium (photos served locally, no real x traffic).

```
pip install -r tests/requirements.txt
python -m playwright install chromium
python tests/suite.py
```

covers: viewer opening and loading order, format fallback for downloads / zip, keyboard shortcuts, scrolling, dark / light mode, new-tab mode, japanese ui, settings window layout, lower-case text, fonts, and page errors.

runs automatically on every push (github actions → *tests*).
