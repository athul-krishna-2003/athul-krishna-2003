"""Profile README cards, v2. Run: python3 build_v2.py  ->  assets/*.svg

Direction: chalk / deep navy / one ultramarine. Plain copy. One move per card.
The numbers in stats() are PLACEHOLDERS: edit the config there.
"""
import math
import os

OUT = "assets"
os.makedirs(OUT, exist_ok=True)

CHALK, NAVY, BLUE, ICE = "#f2f3ee", "#0a0f24", "#2f4bff", "#e3e7ff"
MC, MN = "#5a6072", "#9aa3c4"           # muted on chalk / on navy (>= 5:1)
HC, HN = "#d9dbd2", "#1c2340"           # hairlines on chalk / navy
LB = "#5b74ff"                          # blue that reads on navy
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
EASE = "cubic-bezier(.2,.8,.2,1)"
WIPE = "cubic-bezier(.7,0,.25,1)"


def kf(name, *frames):
    return "@keyframes %s{%s}" % (name, "".join("%s{%s}" % (s, p) for s, p in frames))


def pc(t, d):
    return round(t / d * 100, 3)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fade_all(d, t_out):
    return kf("all", ("0%", "opacity:0"), (f"{pc(0.4, d)}%,{pc(t_out, d)}%", "opacity:1"), (f"{pc(t_out + 0.9, d)}%,100%", "opacity:0")) \
        + f".all{{animation:all {d}s linear infinite}}"


def doc(name, w, h, label, css, body, bg, stroke, rm="", defs=""):
    css += "@media (prefers-reduced-motion:reduce){*{animation:none!important}%s}" % rm
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">
  <title>{esc(label)}</title>
  <defs>{defs}</defs>
  <style>{css}</style>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="{bg}" stroke="{stroke}"/>
{body}
</svg>
'''
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(svg)


# ============================================================ 1 HERO
def hero():
    d, t0, t1 = 11.0, 1.0, 4.2
    W, H = 1000, 462
    css = fade_all(d, 9.3)
    css += kf("clip", (f"0%,{pc(t0,d)}%", "clip-path:inset(0 100% 0 0) fill-box"), (f"{pc(t1,d)}%,100%", "clip-path:inset(0 0 0 0) fill-box"))
    css += f".clip{{animation:clip {d}s {WIPE} infinite}}"
    css += kf("scan",
              ("0%", "transform:translateX(0);opacity:0"),
              (f"{pc(t0-0.02,d)}%", "transform:translateX(0);opacity:0"),
              (f"{pc(t0,d)}%", "transform:translateX(0);opacity:1"),
              (f"{pc(t1,d)}%", "transform:translateX(1000px);opacity:1"),
              (f"{pc(t1+0.15,d)}%,100%", "transform:translateX(1000px);opacity:0"))
    css += f".scan{{animation:scan {d}s {WIPE} infinite}}"
    rm = ".clip{clip-path:inset(0 0 0 0) fill-box}.scan{opacity:0}"

    def words(fill_attrs):
        return (
            f'<text x="50" y="206" font-family="{SANS}" font-weight="800" font-size="196" letter-spacing="-6" textLength="500" lengthAdjust="spacingAndGlyphs" {fill_attrs}>Athul</text>'
            f'<text x="50" y="384" font-family="{SANS}" font-weight="800" font-size="196" letter-spacing="-6" textLength="740" lengthAdjust="spacingAndGlyphs" {fill_attrs}>Krishna</text>'
        )

    body = f'''  <g class="all">
    {words(f'fill="none" stroke="{ICE}" stroke-width="2" stroke-opacity=".9"')}
    <g class="clip"><rect width="{W}" height="{H}" fill="none"/>{words(f'fill="{CHALK}"')}</g>
    <rect class="scan" x="0" y="20" width="3" height="420" fill="{ICE}"/>
    <text x="56" y="438" font-family="{SANS}" font-size="20" fill="{ICE}">Web developer</text>
    <text x="944" y="438" text-anchor="end" font-family="{SANS}" font-size="20" fill="{ICE}">Insights Marketers, Ernakulam</text>
  </g>'''
    doc("hero", W, H, "Athul Krishna, web developer at Insights Marketers, Ernakulam", css, body, BLUE, "#2640e6", rm)


# ============================================================ 2 ABOUT
def about():
    d = 8.0
    CW, FS = 19.4, 40
    lines = [
        (100, [("I write the code for client websites at a", 0)]),
        (156, [("marketing agency. Most of it is ", 0), ("under NDA", 1), (",", 0)]),
        (212, [("so there isn’t much I can link to.", 0)]),
    ]
    base, hl = [], ""
    for y, segs in lines:
        x = 56.0
        for txt, hi in segs:
            lead = len(txt) - len(txt.lstrip())
            vis = txt.strip()
            tx, tw = x + lead * CW, len(vis) * CW
            a = f'y="{y}" font-family="{SANS}" font-weight="500" font-size="{FS}" letter-spacing="-0.6" textLength="{tw:.1f}" lengthAdjust="spacing"'
            base.append(f'<text x="{tx:.1f}" {a} fill="{NAVY}">{esc(vis)}</text>')
            if hi:
                hl = (f'<g class="hl"><rect x="{tx-12:.1f}" y="{y-36}" width="{tw+24:.1f}" height="52" rx="8" fill="{BLUE}"/>'
                      f'<text x="{tx:.1f}" y="{y}" font-family="{SANS}" font-weight="500" font-size="{FS}" fill="{CHALK}" textLength="{tw:.1f}" lengthAdjust="spacingAndGlyphs">{esc(vis)}</text></g>')
            x += len(txt) * CW
    css = kf("hlc", (f"0%,{pc(1.2,d)}%", "clip-path:inset(0 100% 0 0) fill-box"), (f"{pc(2.0,d)}%,100%", "clip-path:inset(0 0 0 0) fill-box"))
    css += kf("hlo", ("0%,80%", "opacity:1"), ("90%,100%", "opacity:0"))
    css += f".hl{{animation:hlc {d}s {WIPE} infinite,hlo {d}s linear infinite}}"
    rm = ".hl{clip-path:inset(0 0 0 0) fill-box;opacity:1}"
    doc("about", 1000, 270, "I write the code for client websites at a marketing agency. Most of it is under NDA, so there isn't much I can link to.",
        css, "\n".join(base) + hl, CHALK, HC, rm)


# ============================================================ 3 WORK
def work():
    W, H = 1000, 470
    css = kf("sc", ("0%", "transform:translateY(0)"), ("100%", "transform:translateY(-540px)"))
    css += ".sc{animation:sc 18s ease-in-out infinite alternate}"
    rm = ".sc{transform:translateY(-220px)}"
    page = []
    page.append(f'<rect x="0" y="0" width="1000" height="1100" fill="{NAVY}"/>')
    # nav
    page.append(f'<rect x="40" y="76" width="96" height="22" rx="4" fill="{BLUE}"/>')
    for i in range(4):
        page.append(f'<rect x="{600+i*88}" y="82" width="60" height="10" rx="5" fill="{ICE}" fill-opacity=".55"/>')
    # hero block
    page.append(f'<rect x="0" y="130" width="1000" height="330" fill="{BLUE}"/>')
    page.append(f'<rect x="60" y="190" width="520" height="40" rx="6" fill="{CHALK}"/><rect x="60" y="246" width="430" height="40" rx="6" fill="{CHALK}"/>')
    page.append(f'<rect x="60" y="312" width="360" height="14" rx="7" fill="{ICE}" fill-opacity=".7"/><rect x="60" y="338" width="300" height="14" rx="7" fill="{ICE}" fill-opacity=".7"/>')
    page.append(f'<rect x="60" y="380" width="160" height="48" rx="24" fill="{CHALK}"/>')
    page.append(f'<circle cx="800" cy="300" r="120" fill="#6f86ff"/><circle cx="860" cy="240" r="46" fill="{CHALK}"/>')
    # cards
    for i in range(3):
        x = 60 + i * 305
        page.append(f'<rect x="{x}" y="520" width="270" height="230" rx="14" fill="#141b3d" stroke="#2a335e"/>')
        page.append(f'<rect x="{x+24}" y="544" width="44" height="44" rx="10" fill="{LB}"/>')
        page.append(f'<rect x="{x+24}" y="612" width="180" height="16" rx="8" fill="{ICE}" fill-opacity=".8"/>')
        page.append(f'<rect x="{x+24}" y="644" width="214" height="10" rx="5" fill="{ICE}" fill-opacity=".35"/><rect x="{x+24}" y="666" width="150" height="10" rx="5" fill="{ICE}" fill-opacity=".35"/>')
    # image band
    page.append(f'<rect x="60" y="800" width="880" height="230" rx="16" fill="#1d2a6b"/><circle cx="260" cy="915" r="70" fill="{LB}"/><rect x="420" y="850" width="430" height="24" rx="12" fill="{CHALK}" fill-opacity=".85"/><rect x="420" y="892" width="330" height="14" rx="7" fill="{ICE}" fill-opacity=".5"/>')
    page.append(f'<rect x="0" y="1060" width="1000" height="40" fill="#121936"/>')
    body = f'''  <g clip-path="url(#vp)">
    <g class="sc"><g filter="url(#bl)">{"".join(page)}</g></g>
  </g>
  <rect x="1" y="1" width="998" height="56" rx="17" fill="#121936"/><rect x="1" y="30" width="998" height="27" fill="#121936"/>
  <circle cx="34" cy="29" r="6" fill="none" stroke="#2a335e" stroke-width="2"/><circle cx="58" cy="29" r="6" fill="none" stroke="#2a335e" stroke-width="2"/><circle cx="82" cy="29" r="6" fill="none" stroke="#2a335e" stroke-width="2"/>
  <rect x="120" y="14" width="640" height="30" rx="15" fill="{NAVY}"/>
  <text x="142" y="34" font-family="{MONO}" font-size="14" fill="{MN}">https://</text>
  <rect x="210" y="23" width="140" height="12" rx="3" fill="{MN}"/>
  <text x="358" y="34" font-family="{MONO}" font-size="14" fill="{MN}">.in</text>
  <rect x="302" y="238" width="396" height="52" rx="26" fill="{CHALK}"/>
  <text x="500" y="271" text-anchor="middle" font-family="{SANS}" font-weight="600" font-size="20" fill="{NAVY}" textLength="340" lengthAdjust="spacing">Client site, blurred. Under NDA.</text>'''
    defs = ('<filter id="bl" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="8"/></filter>'
            '<clipPath id="vp"><path d="M1,57 H999 V451 Q999,469 981,469 H19 Q1,469 1,451 Z"/></clipPath>')
    doc("work", W, H, "A client website, blurred on purpose because the work is under NDA", css, body, NAVY, HN, rm, defs)


# ============================================================ 4 STATS
def stats():
    # ===================== CONFIG: replace with your real numbers =====================
    counters = [(3, "+", "YEARS CODING"), (40, "+", "SITES SHIPPED"), (25, "+", "CLIENTS"), (100, "%", "ON-TIME HANDOVERS")]
    months = list("JFMAMJJASO")
    monthly = [1, 2, 2, 4, 3, 5, 4, 6, 5, 7]
    chart_title = "SITES SHIPPED IN 2026"
    # ==================================================================================
    d, DW, LH, FS = 14.0, 46, 84, 76
    W, H = 1000, 450
    css = fade_all(d, 12.2)
    rm, body = "", ['<g class="all">']
    uid = 0
    for ci, (val, suf, lab) in enumerate(counters):
        x0, y0 = 60 + ci * 225, 118
        s = str(val)
        for di, ch in enumerate(s):
            uid += 1
            t0 = 0.5 + ci * 0.15 + di * 0.12
            t1 = t0 + 1.9
            dist = int(ch) * LH
            css += kf(f"d{uid}", (f"0%,{pc(t0,d)}%", "transform:translateY(0)"), (f"{pc(t1,d)}%,100%", f"transform:translateY(-{dist}px)"))
            css += f".d{uid}{{animation:d{uid} {d}s {EASE} infinite}}"
            rm += f".d{uid}{{transform:translateY(-{dist}px)}}"
            cx = x0 + di * DW + DW / 2
            reel = "".join(f'<text x="{cx}" y="{y0+k*LH}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="{FS}" letter-spacing="-2" fill="{NAVY}">{k}</text>' for k in range(10))
            body.append(f'<clipPath id="c{uid}"><rect x="{x0+di*DW}" y="{y0-62}" width="{DW}" height="76"/></clipPath><g clip-path="url(#c{uid})"><g class="d{uid}">{reel}</g></g>')
        body.append(f'<text x="{x0+len(s)*DW+2}" y="{y0}" font-family="{SANS}" font-weight="800" font-size="{FS}" fill="{BLUE}">{suf}</text>')
        body.append(f'<text x="{x0}" y="{y0+34}" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MC}">{lab}</text>')
    body.append(f'<line x1="60" y1="186" x2="940" y2="186" stroke="{HC}"/>')
    body.append(f'<text x="60" y="226" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MC}">{chart_title}</text>')
    base, maxh, ymax = 394, 124, max(monthly)
    for i, v in enumerate(monthly):
        cx = 60 + 44 + i * 88
        h = v / ymax * maxh
        t = 1.6 + i * 0.12
        last = i == len(monthly) - 1
        css += kf(f"b{i}", (f"0%,{pc(t,d)}%", "transform:scaleY(0)"), (f"{pc(t+0.9,d)}%,100%", "transform:scaleY(1)"))
        css += f".b{i}{{transform-box:fill-box;transform-origin:50% 100%;animation:b{i} {d}s {EASE} infinite}}"
        rm += f".b{i}{{transform:scaleY(1)}}"
        body.append(f'<rect class="b{i}" x="{cx-22}" y="{base-h:.1f}" width="44" height="{h:.1f}" rx="6" fill="{BLUE if last else NAVY}"/>')
        body.append(f'<text x="{cx}" y="{base+24}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MC}">{months[i]}</text>')
        if last:
            css += kf("vl", (f"0%,{pc(t+0.6,d)}%", "opacity:0"), (f"{pc(t+1.0,d)}%,100%", "opacity:1")) + f".vl{{animation:vl {d}s linear infinite}}"
            rm += ".vl{opacity:1}"
            body.append(f'<text class="vl" x="{cx}" y="{base-h-12:.1f}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="20" fill="{NAVY}">{v}</text>')
    body.append(f'<line x1="60" y1="{base}" x2="940" y2="{base}" stroke="{HC}"/></g>')
    doc("stats", W, H, "Years coding, sites shipped, clients, on-time handovers, and sites shipped per month in 2026", css, "\n".join(body), CHALK, HC, rm)


# ============================================================ 5 STACK
def stack():
    items = "HTML CSS JavaScript TypeScript React Next.js Python Node.js Git Docker Figma".split()
    N, SP, SLOT, HOLD = len(items), 78, 1.5, 1.0
    d = SLOT * N
    CY, H = 200, 400
    lst = items[-3:] + items + items[:3]
    css = ""
    fr = []
    for i in range(N + 1):
        ty = CY - (3 + i) * SP
        t = i * SLOT
        fr.append((f"{pc(t,d)}%,{pc(t+HOLD,d)}%" if i < N else "100%", f"transform:translateY({ty}px)"))
    css += kf("reel", *fr) + f".reel{{animation:reel {d}s cubic-bezier(.7,0,.2,1) infinite}}"
    rm = f".reel{{transform:translateY({CY-3*SP}px)}}.f3{{fill-opacity:1}}"
    texts = []
    for k, name in enumerate(lst):
        i = k - 3
        cls = ""
        if 0 <= i <= N:
            t = i * SLOT
            if i == 0:
                f = [("0%," + f"{pc(HOLD+0.05,d)}%", "fill-opacity:1"), (f"{pc(HOLD+0.5,d)}%,100%", "fill-opacity:0")]
            elif i < N:
                f = [(f"0%,{pc(t-0.45,d)}%", "fill-opacity:0"), (f"{pc(t+0.05,d)}%,{pc(t+HOLD+0.05,d)}%", "fill-opacity:1"), (f"{pc(t+HOLD+0.5,d)}%,100%", "fill-opacity:0")]
            else:
                f = [(f"0%,{pc(t-0.45,d)}%", "fill-opacity:0"), ("100%", "fill-opacity:1")]
            css += kf(f"f{k}", *f) + f".f{k}{{animation:f{k} {d}s linear infinite}}"
            cls = f' class="f{k}"'
        texts.append(
            f'<text{cls} x="120" y="{k*SP+21}" font-family="{SANS}" font-weight="800" font-size="60" letter-spacing="-1.5" '
            f'fill="{CHALK}" fill-opacity="0" stroke="{ICE}" stroke-opacity=".5" stroke-width="1.4">{esc(name)}</text>'
        )
    counters = []
    for i in range(N):
        t = i * SLOT
        if i == 0:
            fr = [(f"0%,{pc(SLOT-0.01,d)}%", "opacity:1"), (f"{pc(SLOT,d)}%,100%", "opacity:0")]
        elif i == N - 1:
            fr = [(f"0%,{pc(t-0.01,d)}%", "opacity:0"), (f"{pc(t,d)}%,100%", "opacity:1")]
        else:
            fr = [(f"0%,{pc(t-0.01,d)}%", "opacity:0"), (f"{pc(t,d)}%,{pc(t+SLOT-0.01,d)}%", "opacity:1"), (f"{pc(t+SLOT,d)}%,100%", "opacity:0")]
        css += kf(f"n{i}", *fr) + f".n{i}{{animation:n{i} {d}s linear infinite}}"
        rm += f".n{i}{{opacity:{1 if i == 0 else 0}}}"
        counters.append(f'<text class="n{i}" x="940" y="206" text-anchor="end" font-family="{MONO}" font-size="16" fill="{MN}">{i+1:02d} / {N}</text>')
    body = f'''  <clipPath id="sc"><rect x="1" y="1" width="998" height="{H-2}" rx="17"/></clipPath>
  <g clip-path="url(#sc)">
    <g class="reel">{"".join(texts)}</g>
    <rect x="0" y="0" width="1000" height="120" fill="url(#tg)"/><rect x="0" y="{H-120}" width="1000" height="120" fill="url(#bg2)"/>
  </g>
  <circle cx="80" cy="{CY}" r="7" fill="{LB}"/>
  {"".join(counters)}'''
    defs = (f'<linearGradient id="tg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="bg2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></linearGradient>')
    doc("stack", 1000, H, "Tools: HTML, CSS, JavaScript, TypeScript, React, Next.js, Python, Node.js, Git, Docker, Figma", css, body, NAVY, HN, rm, defs)


# ============================================================ 6 PROCESS
def process():
    d = 14.0
    y = 240
    nodes = [("Brief", 80, 0.0), ("Figma", 250, 0.921), ("Code", 420, 1.843), ("Staging", 590, 2.764), ("Live", 920, 10.0)]
    path = "M80,240 L590,240 A80,80 0 1 1 590,80 A80,80 0 1 1 590,240 A80,80 0 1 1 590,80 A80,80 0 1 1 590,240 L920,240"
    css = fade_all(d, 12.6)
    rm = ""
    body = [
        '<g class="all">',
        f'<text x="60" y="48" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MC}">HOW A SITE GETS TO LIVE</text>',
        f'<circle cx="590" cy="160" r="80" fill="none" stroke="#c9ccc1" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/>',
        f'<line x1="80" y1="{y}" x2="920" y2="{y}" stroke="#c9ccc1" stroke-width="2"/>',
        f'<text x="590" y="156" text-anchor="middle" font-family="{SANS}" font-size="18" fill="{MC}">Client asks</text>',
        f'<text x="590" y="180" text-anchor="middle" font-family="{SANS}" font-size="18" fill="{MC}">for changes</text>',
    ]
    for i, (name, x, t) in enumerate(nodes):
        css += kf(f"n{i}", (f"0%,{pc(t,d)}%", "opacity:0" if t > 0 else "opacity:1"), (f"{pc(t+0.3,d)}%,100%", "opacity:1"))
        css += f".n{i}{{animation:n{i} {d}s linear infinite}}"
        rm += f".n{i}{{opacity:1}}"
        body.append(
            f'<circle cx="{x}" cy="{y}" r="10" fill="{CHALK}" stroke="{NAVY}" stroke-width="2.5"/>'
            f'<circle class="n{i}" cx="{x}" cy="{y}" r="10" fill="{BLUE}" stroke="{BLUE}" stroke-width="2.5"/>'
            f'<text x="{x}" y="{y+46}" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="20" fill="{NAVY}">{name}</text>'
        )
    tc = 10.1
    css += kf("ck", (f"0%,{pc(tc,d)}%", "stroke-dashoffset:24"), (f"{pc(tc+0.5,d)}%,100%", "stroke-dashoffset:0"))
    css += f".ck{{stroke-dasharray:24;stroke-dashoffset:24;animation:ck {d}s ease-out infinite}}"
    rm += ".ck{stroke-dashoffset:0}"
    body.append(f'<path class="ck" d="M913,{y} l5,5 l9,-10" fill="none" stroke="{CHALK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    body.append(
        f'<circle r="8" fill="{BLUE}"><animateMotion dur="{d}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;0.714286;1" path="{path}"/></circle>'
        '</g>'
    )
    doc("process", 1000, 330, "How a site gets to live: brief, Figma, code, staging, then client changes before going live", css, "\n".join(body), CHALK, HC, rm)


# ============================================================ 7 CODE
def code():
    d, CW, FS = 16.0, 12.0, 20
    KEY, P, S = ICE, "#b9c4ff", CHALK
    lines = [
        [("const ", "#ffffff"), ("athul", "#ffffff"), (" = {", P)],
        [("  role", KEY), (": ", P), ('"Web developer"', S), (",", P)],
        [("  at", KEY), (": ", P), ('"Insights Marketers"', S), (",", P)],
        [("  base", KEY), (": ", P), ('"Ernakulam, Kerala"', S), (",", P)],
        [("  builds", KEY), (": [", P), ('"websites"', S), (", ", P), ('"e-commerce"', S), (", ", P), ('"internal tools"', S), ("],", P)],
        [("  stack", KEY), (": [", P), ('"React"', S), (", ", P), ('"Next.js"', S), (", ", P), ('"TypeScript"', S), (", ", P), ('"Node"', S), ("],", P)],
        [("  ships", KEY), (": ", P), ('"on the deadline"', S), (",", P)],
        [("};", P)],
    ]
    css = fade_all(d, 14.0)
    css += "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1.1s steps(1) infinite}"
    rm, body = "", ['<g class="all">']
    for i, segs in enumerate(lines):
        y = 96 + i * 40
        n = sum(len(t) for t, _ in segs)
        tl = n * CW
        t = 0.9 + i * 1.15
        td = t + 0.15 + min(1.0, n * 0.04)
        last = i == len(lines) - 1
        spans = "".join(f'<tspan fill="{c}"{" font-weight=\"800\"" if c == "#ffffff" else ""}>{esc(tx)}</tspan>' for tx, c in segs)
        body.append(
            f'<text x="56" y="{y}" font-family="{MONO}" font-size="{FS}" fill="#8fa0ff">{i+1}</text>'
            f'<text x="104" y="{y}" font-family="{MONO}" font-size="{FS}" xml:space="preserve" textLength="{tl:.1f}" lengthAdjust="spacing">{spans}</text>'
            f'<rect class="cv{i}" x="102" y="{y-26}" width="{tl+30:.1f}" height="36" fill="{BLUE}"/>'
            f'<g class="cu{i}"><rect class="blink" x="104" y="{y-22}" width="11" height="28" fill="{CHALK}"/></g>'
        )
        css += kf(f"cv{i}", (f"0%,{pc(t,d)}%", f"transform:scaleX(1);animation-timing-function:steps({n},end)"), (f"{pc(td,d)}%,100%", "transform:scaleX(0)"))
        css += f".cv{i}{{transform-box:fill-box;transform-origin:100% 50%;animation:cv{i} {d}s linear infinite}}"
        fr = [(f"0%,{pc(t,d)}%", "transform:translateX(0);opacity:0"),
              (f"{pc(t+0.01,d)}%", f"transform:translateX(0);opacity:1;animation-timing-function:steps({n},end)")]
        if last:
            fr.append((f"{pc(td,d)}%,100%", f"transform:translateX({tl:.1f}px);opacity:1"))
        else:
            fr += [(f"{pc(td,d)}%", f"transform:translateX({tl:.1f}px);opacity:1"), (f"{pc(td+0.01,d)}%,100%", f"transform:translateX({tl:.1f}px);opacity:0")]
        css += kf(f"cu{i}", *fr) + f".cu{i}{{animation:cu{i} {d}s linear infinite}}"
        rm += f".cv{i}{{transform:scaleX(0)}}.cu{i}{{opacity:{1 if last else 0}}}"
    body.append("</g>")
    doc("code", 1000, 420, "Athul as a few lines of code: web developer, Insights Marketers, Ernakulam", css, "\n".join(body), BLUE, "#2640e6", rm)


# ============================================================ 8 CONTACT
def contact():
    d = 7.0
    css = fade_all(d, 5.8)
    css += kf("ln", (f"0%,{pc(1.0,d)}%", "stroke-dashoffset:300"), (f"{pc(1.8,d)}%,100%", "stroke-dashoffset:0"))
    css += f".ln{{stroke-dasharray:300;stroke-dashoffset:300;animation:ln {d}s {EASE} infinite}}"
    css += kf("hd", (f"0%,{pc(1.7,d)}%", "stroke-dashoffset:90"), (f"{pc(2.2,d)}%,100%", "stroke-dashoffset:0"))
    css += f".hd{{stroke-dasharray:90;stroke-dashoffset:90;animation:hd {d}s {EASE} infinite}}"
    rm = ".ln,.hd{stroke-dashoffset:0}"
    body = f'''  <g class="all">
    <text x="54" y="126" font-family="{SANS}" font-weight="800" font-size="88" letter-spacing="-3" fill="{CHALK}" textLength="560" lengthAdjust="spacingAndGlyphs">Get in touch</text>
    <line class="ln" x1="650" y1="96" x2="940" y2="96" stroke="{LB}" stroke-width="7" stroke-linecap="round"/>
    <polyline class="hd" points="906,62 940,96 906,130" fill="none" stroke="{LB}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  </g>'''
    doc("contact", 1000, 190, "Get in touch", css, body, NAVY, HN, rm)


for fn in (hero, about, work, stats, stack, process, code, contact):
    fn()
print("ok")
