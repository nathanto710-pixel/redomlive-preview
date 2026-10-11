# REDOM LIVE landing page (preview)

Landing page for REDOM LIVE: The Reset (Sydney 22-23 Oct, Melbourne 29-30 Oct 2026).

- `src/` is the site. Every push to `main` redeploys it to GitHub Pages.
- `build.py` makes a single-file copy in `dist/` for sending as an attachment (not deployed).
- `tools/og/` has the source for the link-preview image.

Preview build: `noindex` is on and the Open Graph URLs point at GitHub Pages. Before the real domain goes live, remove `noindex` and swap the URLs in `src/index.html`.
