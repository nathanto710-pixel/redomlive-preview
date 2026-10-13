# Builds the 5 REDOM LIVE EDMs as email-safe HTML for HubSpot (custom HTML / coded email).
# Copy is verbatim from the "EDMs & LinkedIn" Google Doc (incl. intentional informal spelling).
# Markup in COPY: [[text]] = link to the landing page (where Adi commented "Hyperlink"), **bold**, *italic*.
# Run: python3 tools/edms.py  -> edms/EDM1..5.html + edms/preview.html
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "edms"
OUT.mkdir(exist_ok=True)
LP = "https://redomlive.au"
IMG = "https://nathanto710-pixel.github.io/redomlive-preview/assets/email"   # swap for HubSpot File Manager URLs if preferred
UTM = "?utm_source=hubspot&utm_medium=email&utm_campaign=redomlive&utm_content=edm{n}"

EDMS = [
 ("Property only grows when banks lend you the $", "Wed 14 Oct", """Hey [Name],
I'm going to say something that'll annoy a few people (hopefully not you).
The last 30 years didn't make Australians rich because property is magic. It made us rich because the bank kept handing us bigger and bigger loans.
It's the first thing I’m going to pulling apart at our workshop, in Sydney next week and Melbourne the week after. [[You can grab your ticket here]].
Think about what actually happened.
→ Rates fell from 17% down to nearly 2%.
→ Households went from a single income to 2 incomes.
→ Even loan terms got stretched out to 30 years.
Every single one of those things let you borrow more, and borrowing more is just another way of saying buying the same property for a little bit more next year.
But I don’t know if you’ve noticed, but there’s a major problem with this.
You can only pull each of those levers once. Rates can't fall from 17% again. You can't add a 3rd income, unless your kid suddenly starts contributing to the household by the time they’re 6.
And the funny thing is, it’s all going the other way with the cash rate sitting on record high at 4.60% after 4 consecutive rate rises this year.
So when a buyer's agent promises you 7% a year forever, what they're really promising is another 30 years of cheaper and bigger credit - where exactly is this cheap credit coming from?
That’s why where you buy over the next couple of decades won’t just be about buying ‘quality’ and waiting. It'll be about buying where incomes & jobs are actually still growing, because that's the only thing left that lifts a price when the bank won't.
That’s how we’ll spend the 3 hours together in that workshop - I’ll break it all down for you in person. **I’m also going to give you access to a proprietary website that will give you the entire map of Australia broken down region by region based on my theory - [[but only if you come along to the workshop.]]**
Looking forward to seeing you there.
Redom
PS - This is general information only, not financial or credit advice personalized to you."""),
 ("A price can't go where the bank won't lend", "Fri 16 Oct", """Hey [Name],
Everyone wants to argue about where prices are going. I find that conversation a bit pointless, to be honest.
The simple reason is this - a property price can't go anywhere the bank won't lend.
What does that mean? Well if the local buyers can’t actually borrow the money they need from the bank, the price of a suburb simply cannot go up, no matter how low the supply is or how premium the suburb is.
That is what I’m going to [[break down at the workshop next week]] in Sydney (Melbourne the following week).
You see, I run Flint, and we settled over $1 billion in loans in our 1st year, so I get to watch this ceiling move in real time, across thousands of loan applications.
And you know what I see? Borrowing capacity is getting hammered like there’s no tomorrow. So even on a typical double-income household, the amount you can borrow is FAR less than what you could just a few years ago.
So if you look at the Sydney’s and the Melbourne’s, there are plenty of suburbs in these cities where prices are sitting right up against what people can actually borrow. There's simply no room left to push.
But don’t stress because there are markets where prices are sitting well below what the locals can comfortably borrow, so those markets aren’t even remotely close to a ceiling yet.
**In the workshop (and only in the workshop), I’m going to share my top 20 picks for long term investment in Australia, while breaking down all of the above.**
[[You can come and see me and the Alaya team in person]].
Redom
P.S. General information only, not financial or credit advice."""),
 ("Australia's about to get rich. You’re not.", "Mon 19 Oct", """Hey [Name],
I used to model this country's economy at the Treasury before I left to start my own mortgage broking company. So trust me when I say what I'm about to say is not a doomsday take.
Australia is going to get richer over the next 10 years.
The problem I see though is a lot of Australians are very likely going to end up poorer at the same time, and it’s scary what that’s going to do to a lot of property markets.
It's the uncomfortable idea underneath [[the whole workshop]] I’m running with the Alaya team this month - Sydney on the 22nd & 23rd, and Melbourne on the 29th & 30th.
Let me quickly touch on it.
We spent 20 years being the quarry for China's building boom. The next 20, we become the power station for the world's AI boom, the data centres, the energy, the water, the metals that all of it runs on. That’s billions of dollars that is going to end up in Australia.
Ironically, the jobs that carry the big mortgages - the consultants, the analysts, the back-office finance roles, those are the first ones AI’s coming for first.
I’m going to go on the record to say that 4.6% unemployment might just be the best number we might see ever.
So the question I'd be asking my buyer’s agent is simple.
*In 15 years, who's actually earning the income that holds up the suburb I'm buying in?*
If the honest answer is "people in jobs that are getting automated," that's a problem you’re about to get stuck with.
I’m going to break all of this down over the [[3 hours in the workshop]], and give you access to a website we’ve built that breaks down all of Australia, region by region, based on these principles. Nothing like this exists anywhere I know of.
But you only get it if you join me and the Alaya team in the workshop, so I can talk it through with you.
Redom
P.S. General information only, my opinion, not advice for your situation."""),
 ("I called Darwin very early. Here’s my next one.", "Tue 20 Oct", """Hey [Name],
I'll put my cards on the table, because I think that's the only way you should take anyone in this industry seriously.
Back in 2024 I said buy Darwin. Everyone looked at me a bit funny. It's now the only capital city still rising.
Early last year I called Hobart when no one had even considered it, since it was one of the only markets struggling during the COVID boom.
I’m telling you this because I’m about to [[get into a room in Sydney (22nd & 23rd October) and Melbourne (29th & 30th October)]] to walk you through why these weren’t just lucky guesses.
They came out of the same method every time, and the method is kind of boring. As an ex-economist and someone running one of the biggest mortgage companies in Australia, I see the Australia economy in a way very few people do.
Here’re some outlooks I’m hanging my hat on:
→ Sydney, lower in 2031 than it is today.
→ The old "7% a year, it always doubles" rule is dead.
→ The ‘blue-chip’ suburbs all $50,000 buyer’s agents want to flog you will take an absolute hammering.
If you disagree, we can have a debate in person.
Looking forward to seeing you there. [[Get your tickets here]].
Redom
P.S. General information only, my base case, and forecasts can be wrong. Come decide for yourself."""),
 ("Come argue with me in person next week.", "Wed 21 Oct", """Hey [Name],
I say a few spicy that make people want to fight me.
Things like:
→ Sydney will almost definitely be worth less in 2031 than it is today.
→ A nurse in Launceston is on better off than a fancy-shmancy consultant in Mosman.
If you just read that and thought "this guy’s lost it," - great, [[come argue with me in person]].
In the workshops I’m running with Adi and the Alaya team this month (Sydney on the 22nd & 23rd + Melb on the 29th & 30th) - I really didn’t want 3 hours of me just talking.
I want people to question and challenge me so we can actually form our own conclusions about what we think is Australia’s economic future.
I used to model this economy at the Treasury over a decade ago and I now watch borrowing capacity move across 1000s of loans at Flint. So my logic is formed from a perspective very few people in the country can claim to have - economist + mortgage broker + property investor.
That’s why I’m confident the logic really holds up. I’ve even had the team build you an exclusive website (only get access if you attend the workshop) that breaks down all of Australia, region by region, based on where I believe the best opportunities lie over the next 10+ years.
Worst case scenario, you lose $49 and 3 hours of your time. Best case, you walk away with knowledge that 99.9% of Australia will never get access to.
[[You can come fight with me here]].
Redom
P.S. General information only, not financial or credit advice."""),
]

FONT = "Arial, Helvetica, sans-serif"
HEAD_FONT = "'Anton', Impact, 'Arial Narrow Bold', 'Arial Black', sans-serif"
INK, PLUM, DEEP, CORAL, CREAM, MAUVE = "#2A1022", "#6E0048", "#4D0032", "#FF7150", "#FFF3E9", "#8C5578"


def inline(t, link):
    t = html.escape(t, quote=False)
    t = re.sub(r"\[\[(.+?)\]\]", lambda m: f'<a href="{link}" target="_blank" style="color:{PLUM};font-weight:bold;text-decoration:underline;">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(.+?)\*(?!\w)", r"<em>\1</em>", t)
    return t.replace("[Name]", "{{ contact.firstname }}")


def body_html(text, link):
    lines, out, arrows = text.split("\n"), [], []
    p = f'margin:0 0 16px 0;font-family:{FONT};font-size:16px;line-height:1.6;color:{INK};'

    def flush():
        if arrows:
            out.append(f'<p style="{p}">' + "<br>".join(inline(a, link) for a in arrows) + "</p>")
            arrows.clear()
    for ln in lines:
        if ln.startswith("→"):
            arrows.append(ln); continue
        flush()
        if ln == "Redom":
            out.append(f'<p style="margin:24px 0 16px 0;font-family:{HEAD_FONT};font-size:24px;line-height:1;color:{DEEP};letter-spacing:0.5px;">Redom</p>')
        elif ln.startswith(("PS", "P.S.")):
            out.append(f'<p style="margin:0;font-family:{FONT};font-size:13px;line-height:1.5;color:{MAUVE};">{inline(ln, link)}</p>')
        else:
            out.append(f'<p style="{p}">{inline(ln, link)}</p>')
    flush()
    return "\n".join(out)


def session(day, time):
    return (f'<tr><td style="padding:6px 0;font-family:{HEAD_FONT};font-size:18px;line-height:1.2;color:{CREAM};text-transform:uppercase;">{day}</td>'
            f'<td align="right" style="padding:6px 0;font-family:{FONT};font-size:14px;color:#EFDDE0;white-space:nowrap;">{time}</td></tr>')


def event_block(link):
    city = lambda name, addr, rows: f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 18px 0;">
<tr><td style="font-family:{HEAD_FONT};font-size:28px;line-height:1;color:{CORAL};text-transform:uppercase;padding-bottom:4px;">{name}</td></tr>
<tr><td style="font-family:{FONT};font-size:14px;color:#F3C9B9;padding-bottom:8px;">{addr}</td></tr>
<tr><td><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid #A8789A;">{rows}</table></td></tr>
</table>'''
    return f'''<tr><td style="padding:8px 32px 32px 32px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{DEEP};">
<tr><td style="padding:28px 28px 8px 28px;">
<p style="margin:0 0 4px 0;font-family:{HEAD_FONT};font-size:30px;line-height:1.05;color:{CREAM};text-transform:uppercase;">REDOM LIVE: The Reset</p>
<p style="margin:0 0 22px 0;font-family:{FONT};font-size:14px;letter-spacing:1px;color:#B0F6BB;text-transform:uppercase;">3-hour live workshop</p>
{city("Sydney", "66 Goulburn Street, Sydney NSW 2000", session("Thu 22 Oct", "6pm to 9pm") + session("Fri 23 Oct", "12pm to 3pm"))}
{city("Melbourne", "20/31 Queen Street, Melbourne VIC 3000", session("Thu 29 Oct", "6pm to 9pm") + session("Fri 30 Oct", "12pm to 3pm"))}
</td></tr>
<tr><td style="padding:4px 28px 28px 28px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>
<td align="center" bgcolor="{CORAL}" style="background:{CORAL};">
<a href="{link}" target="_blank" style="display:block;padding:16px 24px;font-family:{HEAD_FONT};font-size:22px;letter-spacing:0.5px;color:{DEEP};text-decoration:none;text-transform:uppercase;">Get a seat</a>
</td></tr></table>
</td></tr>
</table>
</td></tr>'''


def email(n, subject, text):
    link = LP + UTM.format(n=n)
    preheader = {1: "Sydney 22-23 Oct · Melbourne 29-30 Oct. A 3-hour live workshop.",
                 2: "Why borrowing power decides where prices can go.",
                 3: "Who earns the income that holds up your suburb?",
                 4: "Darwin, Hobart, and the calls I'm making now.",
                 5: "Sydney this week, Melbourne next. Come challenge me."}[n]
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(subject)}</title>
<style>@media (max-width:620px){{.wrap{{width:100%!important}} .pad{{padding-left:20px!important;padding-right:20px!important}}}}</style>
</head>
<body style="margin:0;padding:0;background:#F3E3D8;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F3E3D8;">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;">
<tr><td><a href="{link}" target="_blank"><img src="{IMG}/edm{n}-hero.jpg" width="600" alt="REDOM LIVE: The Reset. 3-hour live workshop, Sydney 22-23 Oct, Melbourne 29-30 Oct. Get a seat." style="display:block;width:100%;max-width:600px;height:auto;border:0;"></a></td></tr>
<tr><td class="pad" style="padding:32px 32px 8px 32px;">
{body_html(text, link)}
</td></tr>
{event_block(link)}
</table>
</td></tr>
</table>
</body></html>
'''


rows = []
for i, (subject, send, text) in enumerate(EDMS, 1):
    (OUT / f"EDM{i}.html").write_text(email(i, subject, text))
    rows.append((i, send, subject))
(OUT / "schedule.md").write_text("# REDOM LIVE EDM schedule\n\n| # | Send | Subject | File |\n|---|---|---|---|\n" +
                                 "\n".join(f"| {i} | {s} | {html.unescape(sub)} | EDM{i}.html |" for i, s, sub in rows) + "\n")
print("\n".join(f"EDM{i}  {s}  {sub}" for i, s, sub in rows))
