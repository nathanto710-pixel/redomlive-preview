# Inline src/assets into one self-contained HTML: dist/redomlive.html
import base64, re, mimetypes, pathlib
root = pathlib.Path(__file__).parent
html = (root / "src/index.html").read_text()
mime = {".woff2": "font/woff2", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
def inline(m):
    p = root / "src" / m.group(1)
    if not p.exists():
        return m.group(1)
    return "data:%s;base64,%s" % (mime.get(p.suffix, mimetypes.guess_type(p.name)[0]), base64.b64encode(p.read_bytes()).decode())
html = re.sub(r'(?<=["(])(assets/[^")]+)(?=[")])', inline, html)
(root / "dist/redomlive.html").write_text(html)
print("dist/redomlive.html", len(html) // 1024, "KB")
