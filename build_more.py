"""Six more animated SVGs for the profile README. Run: python3 build_more.py
Writes assets/about.svg, stack.svg, process.svg, work.svg, contact.svg, code.svg
"""
import math
import os

OUT = "assets"
os.makedirs(OUT, exist_ok=True)

INK, LINE, PAPER, CODE, MUTED, PEN = "#0e0f12", "#24262b", "#e9e4d6", "#d8d4c8", "#9a9a93", "#ff5a36"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
EASE = "cubic-bezier(.2,.8,.2,1)"


def kf(name, *frames):
    return "@keyframes %s{%s}" % (name, "".join("%s{%s}" % (sel, props) for sel, props in frames))


def anim(cls, name, d, ease="linear", extra=""):
    return ".%s{animation:%s %ss %s infinite%s}" % (cls, name, d, ease, extra)


def pc(t, d):
    return round(t / d * 100, 3)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def doc(name, w, h, title, css, body, bg=INK, stroke=LINE, rx=16, rm=""):
    css = css + "@media (prefers-reduced-motion:reduce){*{animation:none!important}%s}" % rm
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">
  <title>{esc(title)}</title>
  <style>{css}</style>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" fill="{bg}" stroke="{stroke}"/>
{body}
</svg>
'''
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(svg)


def fade_all(d, t_out):
    """whole group fades in fast, holds, fades out so the loop reset is unseen"""
    return kf("all", ("0%", "opacity:0"), (f"{pc(0.4, d)}%,{pc(t_out, d)}%", "opacity:1"), (f"{pc(t_out+0.9, d)}%,100%", "opacity:0")) + anim("all", "all", d)


# =============================================================== 1. ABOUT
def about():
    d = 12.0
    INKTXT, SOFT, PB = "#0e0f12", "#55524a", "#e9e4d6"
    CW, FS = 21.5, 46
    css = fade_all(d, 10.2)
    body = [f'<text x="60" y="64" font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="#6b685f">WHAT I DO</text>']
    rm = ""
    lines = [
        (140, [("I build websites that ", 0), ("load fast", 1), (",", 0)]),
        (205, [("look clean", 1), (", and ", 0), ("convert", 1), (".", 0)]),
    ]
    k = 0
    for y, segs in lines:
        x = 60.0
        for txt, hi in segs:
            w = len(txt) * CW
            vis = txt.strip()
            lead = len(txt) - len(txt.lstrip())
            tx = x + lead * CW
            tw = len(vis) * CW
            body.append(
                f'<text x="{tx:.1f}" y="{y}" font-family="{SERIF}" font-size="{FS}" letter-spacing="-0.5" fill="{INKTXT}" textLength="{tw:.1f}" lengthAdjust="spacing">{esc(vis)}</text>'
            )
            if hi:
                t0 = 1.0 + k * 1.1
                ln = round(tw + 10)
                css += kf(f"u{k}", ("0%," + f"{pc(t0, d)}%", f"stroke-dashoffset:{ln}"), (f"{pc(t0+0.7, d)}%,100%", "stroke-dashoffset:0"))
                css += f".u{k}{{stroke-dasharray:{ln};stroke-dashoffset:{ln};animation:u{k} {d}s {EASE} infinite}}"
                rm += f".u{k}{{stroke-dashoffset:0}}"
                body.append(
                    f'<path class="u{k}" d="M{x+lead*CW-4:.1f},{y+14} Q{x+lead*CW+tw/2:.1f},{y+8} {x+lead*CW+tw+4:.1f},{y+11}" fill="none" stroke="{PEN}" stroke-width="4.5" stroke-linecap="round"/>'
                )
                k += 1
            x += w
    body.append(f'<text x="60" y="268" font-family="{SANS}" font-size="18" fill="#3a3935">Web developer at Insights Marketers, Ernakulam.</text>')
    doc("about", 1000, 300, "What I do: I build websites that load fast, look clean, and convert.", css, '<g class="all">' + "\n".join(body) + "</g>", bg=PB, stroke="#cfc9b8", rm=rm)


# =============================================================== 2. STACK
def stack():
    d = 26.0
    rows = [
        ("HTML CSS JavaScript TypeScript React Next.js".split(), 104, -1),
        ("Python Node.js Git Docker Figma".split(), 164, 1),
    ]
    PC, GAP = 10.8, 16
    css = ""
    body = [
        '<clipPath id="cl"><rect x="1" y="1" width="998" height="228" rx="15"/></clipPath>',
        f'<linearGradient id="gl" x1="0" x2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>',
        f'<linearGradient id="gr" x1="1" x2="0"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>',
        f'<text x="60" y="56" font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="{MUTED}">TOOLS I REACH FOR</text>',
        '<g clip-path="url(#cl)">',
    ]
    rm = ""
    for ri, (items, cy, dirn) in enumerate(rows):
        widths = [len(s) * PC + 44 for s in items]
        S = sum(widths) + GAP * len(items)
        n = math.ceil((1000 + S) / S) + 1
        pills, x = [], 0.0
        for _ in range(n):
            for s, pw in zip(items, widths):
                pills.append(
                    f'<rect x="{x:.1f}" y="{cy-22}" width="{pw:.1f}" height="44" rx="22" fill="none" stroke="#33363d"/>'
                    f'<text x="{x+22:.1f}" y="{cy+6}" font-family="{MONO}" font-size="18" fill="{CODE}" textLength="{len(s)*PC:.1f}" lengthAdjust="spacing">{esc(s)}</text>'
                )
                x += pw + GAP
        a, b = (0, -S) if dirn < 0 else (-S, 0)
        css += kf(f"m{ri}", ("0%", f"transform:translateX({a:.1f}px)"), ("100%", f"transform:translateX({b:.1f}px)"))
        css += f".m{ri}{{animation:m{ri} {d - ri*4}s linear infinite}}"
        rm += f".m{ri}{{transform:translateX(-20px)}}"
        body.append(f'<g class="m{ri}">{"".join(pills)}</g>')
    body.append(f'<rect x="0" y="0" width="140" height="230" fill="url(#gl)"/><rect x="860" y="0" width="140" height="230" fill="url(#gr)"/></g>')
    doc("stack", 1000, 230, "Tools I use: HTML, CSS, JavaScript, TypeScript, React, Next.js, Python, Node.js, Git, Docker, Figma", css, "\n".join(body), rm=rm)


# =============================================================== 3. PROCESS
def process():
    d = 14.0
    xs = [120 + i * 760 / 3 for i in range(4)]
    y = 126
    stages = [("BRIEF", "Listen first."), ("DESIGN", "Sketch in Figma."), ("BUILD", "React and Next.js."), ("SHIP", "On the deadline.")]
    t0, t1 = 1.2, 9.2
    css = fade_all(d, 12.2)
    css += kf("ln", (f"0%,{pc(t0,d)}%", "stroke-dashoffset:760"), (f"{pc(t1,d)}%,100%", "stroke-dashoffset:0")) + ".ln{stroke-dasharray:760;stroke-dashoffset:760;animation:ln %ss linear infinite}" % d
    css += kf("hd", (f"0%,{pc(t0,d)}%", "transform:translateX(0)"), (f"{pc(t1,d)}%,100%", "transform:translateX(760px)")) + ".hd{animation:hd %ss linear infinite}" % d
    rm = ".ln{stroke-dashoffset:0}.hd{transform:translateX(760px)}"
    body = [
        '<g class="all">',
        f'<text x="60" y="60" font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="{MUTED}">HOW A BRIEF BECOMES A WEBSITE</text>',
        f'<line x1="{xs[0]}" y1="{y}" x2="{xs[3]}" y2="{y}" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>',
        f'<line class="ln" x1="{xs[0]}" y1="{y}" x2="{xs[3]}" y2="{y}" stroke="{PEN}" stroke-width="3" stroke-linecap="round"/>',
    ]
    for i, ((name, sub), x) in enumerate(zip(stages, xs)):
        tr = t0 + (t1 - t0) * i / 3
        css += kf(f"n{i}", (f"0%,{pc(tr,d)}%", "opacity:0"), (f"{pc(tr+0.35,d)}%,100%", "opacity:1"))
        css += f".n{i}{{animation:n{i} {d}s linear infinite}}"
        rm += f".n{i}{{opacity:1}}"
        body.append(
            f'<circle cx="{x:.1f}" cy="{y}" r="12" fill="{INK}" stroke="#33363d" stroke-width="2"/>'
            f'<g class="n{i}"><circle cx="{x:.1f}" cy="{y}" r="12" fill="{PEN}"/>'
            f'<text x="{x:.1f}" y="{y+58}" text-anchor="middle" font-family="{MONO}" font-size="14" letter-spacing="2.4" fill="{PAPER}">{name}</text>'
            f'<text x="{x:.1f}" y="{y+88}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="19" fill="{MUTED}">{sub}</text></g>'
        )
    # check on the last node
    tc = t1 + 0.1
    css += kf("ck", (f"0%,{pc(tc,d)}%", "stroke-dashoffset:22"), (f"{pc(tc+0.5,d)}%,100%", "stroke-dashoffset:0")) + ".ck{stroke-dasharray:22;stroke-dashoffset:22;animation:ck %ss ease-out infinite}" % d
    rm += ".ck{stroke-dashoffset:0}"
    cx = xs[3]
    body.append(f'<path class="ck" d="M{cx-5:.1f},{y} l4,4 l7,-8" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    body.append(f'<g class="hd"><circle cx="{xs[0]}" cy="{y}" r="5.5" fill="{PAPER}"/></g></g>')
    doc("process", 1000, 280, "My process: brief, design, build, ship", css, "\n".join(body), rm=rm)


# =============================================================== 4. WORK
def work():
    d = 14.0
    css = fade_all(d, 12.2)
    rm = ""
    body = [
        '<g class="all">',
        f'<text x="60" y="60" font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="{MUTED}">SELECTED WORK</text>',
        f'<text x="60" y="108" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">CLIENT</text>',
        f'<text x="360" y="108" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">WHAT I BUILT</text>',
        f'<text x="720" y="108" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">STATUS</text>',
        f'<line x1="60" y1="124" x2="940" y2="124" stroke="{LINE}"/>',
    ]
    rows = [("Company website", "Live", 220), ("E-commerce platform", "Private repo", 170), ("Internal tools", "Login only", 260)]
    for i, (what, status, bw) in enumerate(rows):
        y = 170 + i * 54
        t = 0.9 + i * 0.6
        css += kf(f"r{i}", (f"0%,{pc(t,d)}%", "opacity:0"), (f"{pc(t+0.5,d)}%,100%", "opacity:1"))
        css += f".r{i}{{animation:r{i} {d}s linear infinite}}"
        css += kf(f"bar{i}", (f"0%,{pc(t+0.4,d)}%", "transform:scaleX(0)"), (f"{pc(t+1.1,d)}%,100%", "transform:scaleX(1)"))
        css += f".bar{i}{{transform-box:fill-box;transform-origin:0 50%;animation:bar{i} {d}s {EASE} infinite}}"
        rm += f".r{i}{{opacity:1}}.bar{i}{{transform:scaleX(1)}}"
        body.append(
            f'<rect class="bar{i}" x="60" y="{y-22}" width="{bw}" height="30" fill="{PAPER}"/>'
            f'<g class="r{i}"><text x="360" y="{y}" font-family="{SANS}" font-size="21" fill="{CODE}">{what}</text>'
            f'<text x="720" y="{y}" font-family="{MONO}" font-size="15" fill="{MUTED}">{status}</text>'
            f'<line x1="60" y1="{y+22}" x2="940" y2="{y+22}" stroke="{LINE}"/></g>'
        )
    ts = 5.2
    css += kf("stamp", (f"0%,{pc(ts,d)}%", "transform:scale(1.7) rotate(-6deg);opacity:0"), (f"{pc(ts+0.22,d)}%,100%", "transform:scale(1) rotate(-6deg);opacity:1"))
    css += f".stamp{{transform-box:fill-box;transform-origin:50% 50%;animation:stamp {d}s cubic-bezier(.3,1.5,.5,1) infinite}}"
    rm += ".stamp{transform:rotate(-6deg);opacity:1}"
    body.append(
        f'<g class="stamp"><rect x="650" y="318" width="290" height="62" rx="6" fill="none" stroke="{PEN}" stroke-width="3.5"/>'
        f'<text x="795" y="361" text-anchor="middle" font-family="{MONO}" font-weight="700" font-size="30" letter-spacing="6" fill="{PEN}">UNDER NDA</text></g>'
    )
    body.append(f'<text x="60" y="360" font-family="{SERIF}" font-style="italic" font-size="19" fill="{MUTED}">Clients and code stay private.</text></g>')
    doc("work", 1000, 410, "Selected work: client names and code are private, under NDA", css, "\n".join(body), rm=rm)


# =============================================================== 5. CONTACT
def contact():
    css = kf("ring", ("0%", "transform:scale(1);opacity:.55"), ("80%,100%", "transform:scale(3.6);opacity:0"))
    css += ".ring{transform-box:fill-box;transform-origin:50% 50%;animation:ring 2.2s ease-out infinite}"
    css += kf("rise", ("0%", "transform:translateY(14px);opacity:0"), ("100%", "transform:translateY(0);opacity:1"))
    css += ".rise{animation:rise .9s %s .15s both}" % EASE
    css += kf("nudge", ("0%", "transform:translateX(0)"), ("100%", "transform:translateX(18px)"))
    css += ".nudge{animation:nudge 1.1s ease-in-out infinite alternate}"
    rm = ".ring{opacity:0}"
    body = f'''  <g class="rise">
    <circle class="ring" cx="70" cy="62" r="6" fill="{INK}"/>
    <circle cx="70" cy="62" r="6" fill="{INK}"/>
    <text x="90" y="67" font-family="{MONO}" font-size="13" letter-spacing="2.4" fill="{INK}">BRIEFS WELCOME</text>
    <text x="58" y="158" font-family="{SANS}" font-weight="800" font-size="72" letter-spacing="-2.8" fill="{INK}">Let’s build something.</text>
    <g class="nudge"><text x="842" y="158" font-family="{SANS}" font-weight="800" font-size="72" fill="{INK}">→</text></g>
  </g>'''
    doc("contact", 1000, 220, "Let's build something. Briefs welcome.", css, body, bg=PEN, stroke="#e8481f", rm=rm)


# =============================================================== 6. CODE
def code():
    d = 16.0
    CW, FS = 10.8, 18
    KEY, P, S, K, ID = "#b9b5a8", "#6e7078", PAPER, PEN, PAPER
    lines = [
        [("const ", K), ("athul", ID), (" = {", P)],
        [("  role", KEY), (": ", P), ('"Web developer"', S), (",", P)],
        [("  at", KEY), (": ", P), ('"Insights Marketers"', S), (",", P)],
        [("  base", KEY), (": ", P), ('"Ernakulam, Kerala"', S), (",", P)],
        [("  builds", KEY), (": [", P), ('"websites"', S), (", ", P), ('"e-commerce"', S), (", ", P), ('"internal tools"', S), ("],", P)],
        [("  stack", KEY), (": [", P), ('"React"', S), (", ", P), ('"Next.js"', S), (", ", P), ('"TypeScript"', S), (", ", P), ('"Node"', S), ("],", P)],
        [("  ships", KEY), (": ", P), ('"on the deadline"', S), (",", P)],
        [("};", P)],
    ]
    WIN = "#0b0c0f"
    css = fade_all(d, 14.0)
    css += "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1.1s steps(1) infinite}"
    rm = ""
    body = [
        '<g class="all">',
        f'<rect x="1" y="1" width="998" height="46" rx="15" fill="#15161a"/><rect x="1" y="30" width="998" height="17" fill="#15161a"/>',
        f'<circle cx="30" cy="24" r="6" fill="#2d2f35"/><circle cx="52" cy="24" r="6" fill="#2d2f35"/><circle cx="74" cy="24" r="6" fill="#2d2f35"/>',
        f'<text x="500" y="29" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">athul.ts</text>',
    ]
    for i, segs in enumerate(lines):
        y = 104 + i * 38
        n = sum(len(t) for t, _ in segs)
        tl = n * CW
        t = 0.9 + i * 1.15
        t_done = t + 0.15 + min(1.0, n * 0.04)
        last = i == len(lines) - 1
        spans = "".join(f'<tspan fill="{c}">{esc(tx)}</tspan>' for tx, c in segs)
        body.append(
            f'<text x="44" y="{y}" font-family="{MONO}" font-size="{FS}" fill="#6e7078">{i+1}</text>'
            f'<text x="92" y="{y}" font-family="{MONO}" font-size="{FS}" xml:space="preserve" textLength="{tl:.1f}" lengthAdjust="spacing">{spans}</text>'
            f'<rect class="cv{i}" x="90" y="{y-24}" width="{tl+30:.1f}" height="34" fill="{WIN}"/>'
            f'<g class="cu{i}"><rect class="blink" x="92" y="{y-20}" width="10" height="26" fill="{PEN}"/></g>'
        )
        css += kf(f"cv{i}", (f"0%,{pc(t,d)}%", f"transform:scaleX(1);animation-timing-function:steps({n},end)"), (f"{pc(t_done,d)}%,100%", "transform:scaleX(0)"))
        css += f".cv{i}{{transform-box:fill-box;transform-origin:100% 50%;animation:cv{i} {d}s linear infinite}}"
        end = (f"{pc(t_done,d)}%,100%", f"transform:translateX({tl:.1f}px);opacity:1") if last else None
        frames = [
            (f"0%,{pc(t,d)}%", "transform:translateX(0);opacity:0"),
            (f"{pc(t+0.01,d)}%", f"transform:translateX(0);opacity:1;animation-timing-function:steps({n},end)"),
        ]
        if last:
            frames.append(end)
        else:
            frames += [(f"{pc(t_done,d)}%", f"transform:translateX({tl:.1f}px);opacity:1"), (f"{pc(t_done+0.01,d)}%,100%", f"transform:translateX({tl:.1f}px);opacity:0")]
        css += kf(f"cu{i}", *frames) + f".cu{i}{{animation:cu{i} {d}s linear infinite}}"
        rm += f".cv{i}{{transform:scaleX(0)}}.cu{i}{{opacity:{1 if last else 0}}}"
    body.append("</g>")
    doc("code", 1000, 420, "A tiny code window describing Athul: web developer at Insights Marketers, Ernakulam", css, "\n".join(body), bg=WIN, rm=rm)


for fn in (about, stack, process, work, contact, code):
    fn()
print("ok")
