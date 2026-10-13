# Builds src/thank-you.html (REDOM LIVE post-payment page) from the landing page's <head> styles, plus .ics calendar files.
# Run: python3 tools/thankyou.py
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
page = (SRC / "index.html").read_text()
head = page[:page.index("</head>")]

head = head.replace("<title>REDOM LIVE: The Reset</title>", "<title>You're in | REDOM LIVE</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Your seat at REDOM LIVE: The Reset is confirmed.">', head)
head = re.sub(r'\n<meta property="og:[^\n]*|\n<meta name="twitter:[^\n]*', "", head)   # never shared, keep it private

SESSIONS = [
    ("Sydney", "Thursday 22 October", "6pm to 9pm", "20261022T070000Z", "20261022T100000Z", "66 Goulburn Street, Sydney NSW 2000"),
    ("Sydney", "Friday 23 October", "12pm to 3pm", "20261023T010000Z", "20261023T040000Z", "66 Goulburn Street, Sydney NSW 2000"),
    ("Melbourne", "Thursday 29 October", "6pm to 9pm", "20261029T070000Z", "20261029T100000Z", "20/31 Queen Street, Melbourne VIC 3000"),
    ("Melbourne", "Friday 30 October", "12pm to 3pm", "20261030T010000Z", "20261030T040000Z", "20/31 Queen Street, Melbourne VIC 3000"),
]
DETAILS = "REDOM LIVE: The Reset. A 3-hour live property workshop with Redom Syed. Bring your postcode."

cal_dir = SRC / "assets" / "cal"
cal_dir.mkdir(exist_ok=True)

MONO = "font-family: 'IBM Plex Mono', ui-monospace, monospace"
ANTON = "font-family: 'Anton', 'Impact', sans-serif"
PIN = ('<svg viewBox="0 0 16 16" aria-hidden="true" style="width: 16px; height: 16px; flex: 0 0 auto; margin-top: 3px"><path d="M8 1.5a4.8 4.8 0 0 0-4.8 4.8C3.2 10 8 14.5 8 14.5s4.8-4.5 4.8-8.2A4.8 4.8 0 0 0 8 1.5z" '
       'fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="8" cy="6.3" r="1.7" fill="currentColor"/></svg>')
BTN = (f"display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0 16px; {MONO}; font-size: 13px; "
       "letter-spacing: 0.08em; text-transform: uppercase; text-decoration: none")


def session_rows(city):
    rows = []
    for c, day, time, start, end, addr in SESSIONS:
        if c != city:
            continue
        slug = f"redomlive-{c.lower()}-{day.split()[1]}-oct"
        title = f"REDOM LIVE: The Reset ({c})"
        (cal_dir / f"{slug}.ics").write_text(
            "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//REDOM LIVE//EN\r\nBEGIN:VEVENT\r\n"
            f"UID:{slug}@redomlive\r\nDTSTAMP:20261013T000000Z\r\nDTSTART:{start}\r\nDTEND:{end}\r\n"
            f"SUMMARY:{title}\r\nLOCATION:{addr.replace(',', chr(92) + ',')}\r\nDESCRIPTION:{DETAILS.replace(',', chr(92) + ',')}\r\n"
            "END:VEVENT\r\nEND:VCALENDAR\r\n")
        g = ("https://calendar.google.com/calendar/render?action=TEMPLATE"
             f"&amp;text={quote(title)}&amp;dates={start}/{end}&amp;location={quote(addr)}&amp;details={quote(DETAILS)}")
        rows.append(f'''<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px 20px; padding-top: 14px; border-top: 1px solid #A8789A">
<div style="display: flex; flex-direction: column; gap: 2px"><div style="{ANTON}; font-size: 28px; line-height: 1.05; text-transform: uppercase">{day}</div><div style="{MONO}; font-size: 14px; letter-spacing: 0.06em; text-transform: uppercase; color: #EFDDE0">{time}</div></div>
<div style="display: flex; flex-wrap: wrap; gap: 8px">
<a href="{g}" target="_blank" rel="noopener" style="{BTN}; background: #FF7150; color: #4D0032">Google Calendar</a>
<a href="assets/cal/{slug}.ics" download style="{BTN}; border: 1px solid #F3C9B9; color: #F3C9B9">Apple / Outlook</a>
</div>
</div>''')
    return "\n".join(rows)


def card(city):
    addr = next(s[5] for s in SESSIONS if s[0] == city)
    maps = "https://www.google.com/maps/search/?api=1&amp;query=" + quote(addr)
    return f'''<div style="flex: 1 1 400px; min-width: 0; box-sizing: border-box; background: #4D0032; color: #FFF3E9; padding: clamp(22px, 2.6vw, 32px); display: flex; flex-direction: column; gap: 14px">
<div style="{ANTON}; font-size: clamp(44px, 5vw, 64px); line-height: 1; text-transform: uppercase">{city}</div>
<a class="venue" href="{maps}" target="_blank" rel="noopener" style="display: inline-flex; align-items: flex-start; gap: 8px; color: #F3C9B9; text-decoration: underline; text-decoration-color: rgba(243,201,185,.4); text-underline-offset: 3px; font-size: 17px; line-height: 1.4">{PIN}<span>{addr}</span></a>
{session_rows(city)}
</div>'''


# Picked from youtube.com/@AusPropertyRedom (latest uploads, closest to the workshop themes), 2026-10-13
VIDEOS = [
    ("vbE700KxaAo", "Banks are handing investors more money right now", "22:23"),
    ("wDzJLX7toAo", "Empty auctions and reduced signs across Sydney", "18:32"),
    ("wF6kFlocJEc", "The dangerous credit signals nobody is watching", "26:05"),
    ("t-KvLCb9rP8", "Will Sydney see its biggest house price fall in 40 years?", "26:04"),
    ("emyZTfQu5LU", "Why AI Data Centres Could Change Australian Property For The Next 10 Years", "29:36"),
    ("QTdjnQyVXko", "Brisbane's Winning Pattern Is Now Flashing In Melbourne", "15:19"),
]


def videos():
    out = []
    for vid, title, dur in VIDEOS:
        out.append(f'''<a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" style="display: flex; flex-direction: column; gap: 12px; color: #FFF3E9; text-decoration: none">
<span style="position: relative; display: block; aspect-ratio: 16 / 9; background: #33001F; overflow: hidden">
<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" style="width: 100%; height: 100%; object-fit: cover; display: block">
<span style="position: absolute; right: 8px; bottom: 8px; padding: 2px 8px; background: rgba(0,0,0,.8); {MONO}; font-size: 13px; letter-spacing: 0.04em">{dur}</span>
</span>
<span style="font-size: 18px; line-height: 1.35; font-weight: 600">{title}</span>
</a>''')
    return "\n".join(out)


def step(n, title, body):
    return f'''<div style="flex: 1 1 280px; min-width: 0; border-top: 3px solid #4D0032; padding-top: 16px; display: flex; flex-direction: column; gap: 6px">
<div style="{MONO}; font-size: 14px; letter-spacing: 0.12em; color: #C7411F">{n}</div>
<div style="{ANTON}; font-size: clamp(26px, 2.6vw, 34px); line-height: 1.05; text-transform: uppercase">{title}</div>
<p style="margin: 0; font-size: 18px; line-height: 1.5">{body}</p>
</div>'''


body = f'''<body>
<div style="width: 100%; box-sizing: border-box; background: #4D0032; color: #FFF3E9; font-family: 'Archivo', 'Helvetica Neue', sans-serif; font-size: 18px; line-height: 1.5; overflow-x: hidden">

<header style="padding: 20px clamp(20px, 5vw, 80px); border-bottom: 1px solid #7D3563">
<div style="max-width: 1200px; margin: 0 auto"><a href="./" style="text-decoration: none; color: inherit; {ANTON}; font-size: 28px; letter-spacing: 0.02em; line-height: 1; text-transform: uppercase">Redom <span style="color: #FF7150">Live</span></a></div>
</header>

<section style="padding: clamp(40px, 4.4vw, 64px) clamp(20px, 5vw, 80px) clamp(48px, 5vw, 72px)">
<div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 40px 64px; align-items: center">
<div style="flex: 1 1 520px; min-width: 0; display: flex; flex-direction: column; gap: 22px">
<div style="{MONO}; font-size: 14px; letter-spacing: 0.12em; text-transform: uppercase; color: #B0F6BB">Payment received · Seat confirmed</div>
<h1 style="margin: 0; {ANTON}; font-weight: 400; font-size: clamp(52px, 7vw, 100px); line-height: 0.95; text-transform: uppercase">You're in.<br><span style="color: #FF7150">See you in the room.</span></h1>
<p style="margin: 0; max-width: 640px; font-size: 20px; line-height: 1.5">Your seat at REDOM LIVE: The Reset is confirmed. We've sent a confirmation email with your session details. If it isn't in your inbox in the next few minutes, check your spam or promotions folder.</p>
</div>
<div style="flex: 0 1 380px; min-width: 0; margin: 0 auto">
<img src="assets/stage-a.jpg" alt="Redom Syed presenting on stage" style="width: 100%; aspect-ratio: 4 / 5; object-fit: cover; object-position: 50% 30%; display: block; box-shadow: 14px 14px 0 #FF7150">
</div>
</div>
</section>

<section style="background: #FFF3E9; color: #4D0032; padding: clamp(44px, 4.6vw, 64px) clamp(20px, 5vw, 80px)">
<div style="max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 32px">
<h2 style="margin: 0; {ANTON}; font-weight: 400; font-size: clamp(40px, 5vw, 70px); line-height: 0.98; text-transform: uppercase">What happens next.</h2>
<div style="display: flex; flex-wrap: wrap; gap: 28px 40px">
{step("01", "Check your inbox", "Your confirmation email has your session, date and time.")}
{step("02", "Lock it in", "Add your session to your calendar below so it doesn't slip.")}
{step("03", "Bring your postcode", "Walk out with your own area's score.")}
</div>
<div style="display: flex; flex-wrap: wrap; gap: 24px">
{card("Sydney")}
{card("Melbourne")}
</div>
<div style="box-sizing: border-box; background: #F3E3D8; border: 2px solid #4D0032; padding: clamp(16px, 2vw, 22px) clamp(18px, 2.2vw, 26px); display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 24px">
<div style="{ANTON}; font-size: clamp(24px, 2.4vw, 30px); line-height: 1.05; text-transform: uppercase">The door guarantee.</div>
<p style="margin: 0; flex: 1 1 380px; font-size: 18px">Nothing changes how you think? I refund your ticket at the door.</p>
</div>
</div>
</section>

<section style="padding: clamp(44px, 4.6vw, 64px) clamp(20px, 5vw, 80px)">
<div style="max-width: 1200px; margin: 0 auto; display: flex; flex-direction: column; gap: 28px">
<div style="display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 16px 40px">
<div style="display: flex; flex-direction: column; gap: 8px">
<div style="{ANTON}; font-size: clamp(36px, 4.4vw, 60px); line-height: 1; text-transform: uppercase">While you wait.</div>
<p style="margin: 0; font-size: 18px; color: #D8B9C9">Catch up on Australian Property Talk.</p>
</div>
<a href="https://www.youtube.com/@AusPropertyRedom" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; min-height: 52px; padding: 0 24px; border: 2px solid #FF7150; color: #FF7150; text-decoration: none; {ANTON}; font-size: 20px; letter-spacing: 0.03em; text-transform: uppercase">See all videos</a>
</div>
<div class="yt-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 28px 24px">
{videos()}
</div>
</div>
</section>

<footer style="padding: 32px clamp(20px, 5vw, 80px) 44px; border-top: 1px solid #7D3563">
<div style="max-width: 1200px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 20px 64px; align-items: flex-start">
<div style="{ANTON}; font-size: 28px; letter-spacing: 0.02em; line-height: 1; text-transform: uppercase">Redom <span style="color: #FF7150">Live</span></div>
<p style="margin: 0; flex: 1 1 480px; font-size: 14px; line-height: 1.6; color: #D8B9C9">General information only. Redom Syed's opinion, not financial, credit, tax or legal advice. Forecasts are his base case and may be wrong. Past performance is not a reliable indicator of future performance. Get advice before you act. [ Licence and company details ]</p>
</div>
</footer>

</div>
</body>
</html>
'''

(SRC / "thank-you.html").write_text(head + "</head>\n" + body)
print("wrote src/thank-you.html and", len(list(cal_dir.glob("*.ics"))), "calendar files")
