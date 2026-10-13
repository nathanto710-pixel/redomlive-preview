# Email hero banners for the 5 REDOM LIVE EDMs (1200x600, shown at 600x300). Run: python3 tools/edm_banners.py
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "src/assets"
OUT = A / "email"
OUT.mkdir(exist_ok=True)
F = ROOT / "tools/og"
anton = lambda s: ImageFont.truetype(str(F / "anton.ttf"), s)
mono = lambda s: ImageFont.truetype(str(F / "plexmono-500.ttf"), s)
PLUM, DEEP, CORAL, CREAM, MINT = (110, 0, 72), (77, 0, 50), (255, 113, 80), (255, 243, 233), (176, 246, 187)
W, H = 1200, 600

# photo, horizontal focus (0 left .. 1 right), vertical focus
SHOTS = {1: ("stage-a.jpg", 0.62, 0.3), 2: ("stage-b.jpg", 0.42, 0.3), 3: ("the-room-poster.jpg", 0.55, 0.45),
         4: ("about-2.jpg", 0.5, 0.25), 5: ("about-1.jpg", 0.5, 0.25)}


def cover(path, w, h, fx, fy):
    im = Image.open(path).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = max(0, min(im.width - w, round(im.width * fx - w / 2)))
    y = max(0, min(im.height - h, round(im.height * fy - h / 2)))
    return im.crop((x, y, x + w, y + h))


def tracked(d, xy, text, font, fill, sp):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + sp


for n, (photo, fx, fy) in SHOTS.items():
    img = Image.new("RGB", (W, H), DEEP)
    ph = cover(A / photo, 700, H, fx, fy)
    img.paste(ph, (W - 700, 0))
    # plum panel with a soft edge into the photo
    grad = Image.new("L", (220, 1))
    for i in range(220):
        grad.putpixel((i, 0), 255 - int(255 * i / 219))
    mask = grad.resize((220, H))
    img.paste(Image.new("RGB", (220, H), DEEP), (W - 700, 0), mask)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 10), fill=CORAL)
    f = anton(118)
    d.text((64, 70), "REDOM", font=f, fill=CREAM)
    d.text((64 + d.textlength("REDOM ", font=f), 70), "LIVE", font=f, fill=CORAL)
    d.text((66, 230), "THE RESET", font=anton(64), fill=CREAM)
    tracked(d, (68, 330), "3-HOUR LIVE WORKSHOP", mono(24), MINT, 3)
    tracked(d, (68, 372), "SYDNEY 22-23 OCT · MELBOURNE 29-30 OCT", mono(22), CREAM, 2)
    bt = "GET A SEAT"
    bf = anton(40)
    bw = d.textlength(bt, font=bf)
    d.rectangle((64, 450, 64 + bw + 60, 528), fill=CORAL)
    d.text((94, 461), bt, font=bf, fill=DEEP)
    img.save(OUT / f"edm{n}-hero.jpg", quality=86, optimize=True, progressive=True)
print("banners in", OUT)
