# One-off: apply Redom's round-2 feedback (Oct 2026) to src/index.html
p = "src/index.html"
L = open(p).read().split("\n")


def find(pat, start=0):
    for i in range(start, len(L)):
        if pat in L[i]:
            return i
    raise SystemExit("missing " + pat)


check = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 4.8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="square"/></svg>'
cross = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" fill="none" stroke="currentColor" stroke-width="2"/></svg>'

# 1. replace the #reset section with problem -> solution -> old vs new
s = find('<section id="reset"')
e = find("</section>", s)
old_items = ["7% growth. Forever.", "Buy “quality”. Wait.", "Follow the herd.", "Same plan as 2019."]
new_items = ["Follow the money.", "Buy where jobs are going.", "Get in before the herd.", "New map. New world."]
old_li = "".join(f"<li>{cross}<span>{x}</span></li>" for x in old_items)
new_li = "".join(f"<li>{check}<span>{x}</span></li>" for x in new_items)
new_html = f'''<section id="problem" class="problem">
<div class="wrap">
<h2 class="problem-h">You're being sold a 2019 strategy for a <span>2030 economy.</span></h2>
<div class="problem-old"><s>Buy "quality".</s> <s>Assume 7% a year.</s> <s>Wait.</s></div>
<div class="problem-body">
<p>That advice was built for a world that's gone.</p>
<p>Jobs are moving. Money is moving. Whole markets are about to end up on the wrong side of it.</p>
<p class="problem-cost">Buy in the wrong one and it can cost you hundreds of thousands.</p>
</div>
</div>
</section>

<section id="solution" class="solution">
<div class="wrap">
<div class="sol-cards">
<div class="sol-card"><div class="sol-name">The Money Map</div><p>Shows you where the jobs, people and property wealth go next.</p></div>
<div class="sol-card"><div class="sol-name">The RESET method</div><p>Turns that into what to buy, where, and when.</p></div>
</div>
<div class="sol-lead">Here's the difference...</div>
<div class="ovn">
<div class="ovn-col ovn-old">
<div class="ovn-kicker">Looks backwards</div>
<div class="ovn-title">The old way</div>
<svg class="ovn-chart" viewBox="0 0 480 260" aria-hidden="true"><path d="M10 10V230H470" fill="none" stroke="#7D3563" stroke-width="2"/><path d="M12 205C70 200 90 180 140 172S210 160 250 120 300 100 330 96" fill="none" stroke="#D8B9C9" stroke-width="3"/><circle cx="330" cy="96" r="7" fill="#D8B9C9"/><path d="M330 96L470 30" fill="none" stroke="#D8B9C9" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round"/><path d="M330 104V230" stroke="#D8B9C9" stroke-width="1.5" stroke-dasharray="3 5"/><text x="342" y="150" fill="#D8B9C9" font-family="IBM Plex Mono, monospace" font-size="12" letter-spacing="1.5">“IT ALWAYS GOES UP”</text><text x="330" y="254" fill="#A8789A" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="13" letter-spacing="2">TODAY</text></svg>
<ul>{old_li}</ul>
</div>
<div class="ovn-vs" aria-hidden="true">VS</div>
<div class="ovn-col ovn-new">
<div class="ovn-kicker">Looks forwards</div>
<div class="ovn-title">The new way</div>
<svg class="ovn-chart" viewBox="0 0 480 260" aria-hidden="true"><text x="440" y="24" fill="#4D0032" text-anchor="end" font-family="IBM Plex Mono, monospace" font-size="13" letter-spacing="2">WHERE THE MONEY IS GOING</text><g fill="none" stroke="#4D0032"><path d="M10 185C120 186 190 180 250 132S360 64 440 62" stroke-width="1" opacity=".35"/><path d="M10 195C120 196 190 190 250 140S360 66 440 62" stroke-width="1" opacity=".55"/><path d="M10 215C120 214 190 210 250 160S360 74 440 62" stroke-width="1" opacity=".45"/><path d="M10 225C120 224 190 220 250 170S360 78 440 62" stroke-width="1" opacity=".35"/><path d="M10 205C120 205 190 200 250 150S360 70 440 62" stroke-width="3"/><circle cx="440" cy="62" r="18" stroke-width="1" opacity=".5"/><circle cx="440" cy="62" r="11" stroke-width="1" opacity=".7"/></g><circle cx="440" cy="62" r="6" fill="#4D0032"/><circle cx="262" cy="139" r="6" fill="#FFF3E9" stroke="#4D0032" stroke-width="2"/></svg>
<ul>{new_li}</ul>
</div>
</div>
<div class="ovn-foot">The world changed. <span>The playbook didn't.</span></div>
</div>
</section>'''
L[s:e + 1] = new_html.split("\n")

# 2. remove the rear-view / prestige / payroll band
i = find("Rear-view mirrors are for reversing.")
s = i
while not L[s].startswith("<section"):
    s -= 1
e = find("</section>", i)
del L[s:e + 1]
if L[s] == "" and L[s - 1] == "":
    del L[s]

# 3. remove the $560k box and the forecast chart from #calls
c = find('<section id="calls"')
a = find("$1 million in Sydney", c)
s = a
while "display: flex; flex-wrap: wrap; gap: 32px 64px; align-items: center" not in L[s]:
    s -= 1
pidx = find("Five-year price forecasts to 2031", c)
e = pidx + 2  # p, close right column, close the flex row
assert L[e + 1].strip() == "</div>" and L[e + 2].strip() == "</section>", L[e:e + 3]
del L[s:e + 1]

# 4. track record: Melbourne units call is 2025
k = find("2021 · Melbourne units")
L[k] = L[k].replace("2021 · Melbourne units", "2025 · Melbourne units")

# 5. tickets: replace the chips (incl. the hot seat) with "What you'll get"
s = find("Three hours in the room") - 1
assert "display: flex; flex-wrap: wrap; gap: 10px" in L[s]
e = find("</div>", s + 7)
items = [
    "3 hour education on how to invest for 2026 and beyond",
    "Unpack the 20 markets that'll move and WHY",
    "Discover which 9 areas will HURT",
    "Tactics to invest with to beat the herd following the old playbook",
    "Walk away with your own individual strategy",
    "Get the 10 year score for every property investment you have",
    "A free early digital copy of the Money Map™ Book, released 2027",
]
get = ('<div class="get">\n<h3 class="get-h">What you\'ll get</h3>\n<ul class="get-list">'
       + "".join(f"<li>{check}<span>{x}</span></li>" for x in items) + "</ul>\n</div>")
L[s:e + 1] = get.split("\n")

t = "\n".join(L)
css = open("tools/round2.css").read().strip()
t = t.replace("/* State locks on the map:", css + "\n/* State locks on the map:", 1)
open(p, "w").write(t)
print("ok")
