"""Generates the animated SVGs for the profile README.

Signature move: a client brief is struck through with a red pen and the code
that implements it types in beneath. One loop, ~20s. Nothing else moves except
a blinking cursor.
"""
import os

OUT = "assets"
os.makedirs(OUT, exist_ok=True)

# --- tokens -----------------------------------------------------------------
INK = "#0e0f12"        # background
LINE = "#24262b"       # hairlines
PAPER = "#e9e4d6"      # brief text
CODE = "#d8d4c8"       # code text
MUTED = "#9a9a93"      # labels (>= 7:1 on INK)
PEN = "#ff5a36"        # the one accent

SERIF = "Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"

W, H = 1000, 500
D = 20.0  # loop length in seconds


def pct(t):
    return round(t / D * 100, 3)


ROWS = [
    # brief, code, start time
    ("\u201cMake it feel more premium.\u201d", "letter-spacing: -0.03em;", 1.2),
    ("\u201cCan it convert better?\u201d", '<Cta position="above-fold" />', 4.2),
    ("\u201cLike the other site, but ours.\u201d", "git checkout -b not-a-copy", 7.2),
    ("\u201cNeeded it by Friday.\u201d", "git push origin main", 10.2),
]

BRIEF_X, CODE_X = 60, 520
BRIEF_SIZE, CODE_SIZE = 24, 20
BRIEF_CW, CODE_CW = 11.2, 12.0  # rough per-char widths
ROW_Y0, ROW_GAP = 300, 52

css = []
body = []

for i, (brief, code, t) in enumerate(ROWS):
    y = ROW_Y0 + i * ROW_GAP
    last = i == len(ROWS) - 1
    bw = round(len(brief) * BRIEF_CW)
    cw = round(len(code) * CODE_CW)
    steps = len(code)

    t_in = t               # brief fades in
    t_strike = t + 1.0     # pen strikes
    t_type = t + 1.7       # code types
    t_done = t_type + 1.3

    # row group: fade in, hold, fade out for the loop
    css.append(
        f"@keyframes g{i}{{0%,{pct(t_in)}%{{opacity:0}}{pct(t_in+0.5)}%,92%{{opacity:1}}96%,100%{{opacity:0}}}}"
        f".g{i}{{animation:g{i} {D}s linear infinite}}"
    )
    # brief dims once struck
    css.append(
        f"@keyframes b{i}{{0%,{pct(t_strike)}%{{opacity:1}}{pct(t_strike+0.5)}%,100%{{opacity:.42}}}}"
        f".b{i}{{animation:b{i} {D}s linear infinite}}"
    )
    # pen stroke draws
    css.append(
        f"@keyframes s{i}{{0%,{pct(t_strike)}%{{stroke-dashoffset:{bw}}}{pct(t_strike+0.45)}%,100%{{stroke-dashoffset:0}}}}"
        f".s{i}{{stroke-dasharray:{bw};stroke-dashoffset:{bw};animation:s{i} {D}s cubic-bezier(.2,.8,.2,1) infinite}}"
    )
    # cover rect uncovers the code, stepped like typing
    css.append(
        f"@keyframes c{i}{{0%,{pct(t_type)}%{{transform:scaleX(1);animation-timing-function:steps({steps},end)}}"
        f"{pct(t_done)}%,100%{{transform:scaleX(0)}}}}"
        f".c{i}{{transform-box:fill-box;transform-origin:100% 50%;animation:c{i} {D}s linear infinite}}"
    )
    # cursor rides the leading edge
    cur_end = (
        f"{pct(t_done)}%,100%{{transform:translateX({cw}px);opacity:1}}"
        if last
        else f"{pct(t_done)}%{{transform:translateX({cw}px);opacity:1}}{pct(t_done+0.01)}%,100%{{transform:translateX({cw}px);opacity:0}}"
    )
    css.append(
        f"@keyframes k{i}{{0%,{pct(t_type)}%{{transform:translateX(0);opacity:0}}"
        f"{pct(t_type+0.01)}%{{transform:translateX(0);opacity:1;animation-timing-function:steps({steps},end)}}"
        f"{cur_end}}}"
        f".k{i}{{animation:k{i} {D}s linear infinite}}"
    )

    body.append(f'''
  <g class="g{i}">
    <text class="b{i}" x="{BRIEF_X}" y="{y}" font-family="{SERIF}" font-style="italic" font-size="{BRIEF_SIZE}" fill="{PAPER}">{brief}</text>
    <line class="s{i}" x1="{BRIEF_X-8}" y1="{y-6}" x2="{BRIEF_X-8+bw}" y2="{y-10}" stroke="{PEN}" stroke-width="2.5" stroke-linecap="round"/>
    <text x="{CODE_X}" y="{y}" font-family="{MONO}" font-size="{CODE_SIZE}" fill="{CODE}" xml:space="preserve">{code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</text>
    <rect class="c{i}" x="{CODE_X-2}" y="{y-24}" width="{cw+30}" height="34" fill="{INK}"/>
    <g class="k{i}"><rect class="blink" x="{CODE_X}" y="{y-20}" width="10" height="26" fill="{PEN}"/></g>
  </g>''')

css.append("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1.1s steps(1) infinite}")

# reduced motion: show the finished state, no movement
rm = ["@media (prefers-reduced-motion:reduce){*{animation:none!important}"]
for i in range(len(ROWS)):
    rm.append(f".b{i}{{opacity:.42}}.s{i}{{stroke-dashoffset:0}}.c{i}{{transform:scaleX(0)}}.k{i}{{opacity:0}}")
rm.append("}")
css.append("".join(rm))

hero = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">Athul Krishna, web developer</title>
  <desc id="d">Client briefs are struck through with a red pen and replaced by the code that ships them.</desc>
  <style>
{chr(10).join(css)}
  </style>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{INK}" stroke="{LINE}"/>

  <text x="60" y="64" font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="{MUTED}">INSIGHTS MARKETERS  \u00b7  ERNAKULAM, KERALA</text>
  <text x="58" y="146" font-family="{SANS}" font-weight="700" font-size="72" letter-spacing="-2.4" fill="{PAPER}">Athul Krishna</text>
  <text x="60" y="190" font-family="{SERIF}" font-size="24" fill="{MUTED}">I turn client briefs into websites that ship.</text>

  <line x1="60" y1="222" x2="{W-60}" y2="222" stroke="{LINE}"/>
  <text x="{BRIEF_X}" y="254" font-family="{MONO}" font-size="12" letter-spacing="2.2" fill="{MUTED}">THE BRIEF</text>
  <text x="{CODE_X}" y="254" font-family="{MONO}" font-size="12" letter-spacing="2.2" fill="{MUTED}">THE BUILD</text>
{"".join(body)}
</svg>
'''
open(f"{OUT}/hero.svg", "w", encoding="utf-8").write(hero)

# --- footer: one quiet closing line ---------------------------------------
foot = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 120" width="{W}" height="120" role="img" aria-label="Not every project is huge. Some are just the start of something worth building.">
  <style>
    @keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
    .blink{{animation:blink 1.1s steps(1) infinite}}
    @media (prefers-reduced-motion:reduce){{.blink{{animation:none}}}}
  </style>
  <rect x="0.5" y="0.5" width="{W-1}" height="119" rx="16" fill="{INK}" stroke="{LINE}"/>
  <text x="60" y="68" font-family="{SERIF}" font-style="italic" font-size="22" fill="{PAPER}">Not every project is huge. Some are just the start of something worth building.</text>
  <rect class="blink" x="{60+round(78*10.05)+8}" y="46" width="10" height="26" fill="{PEN}"/>
</svg>
'''
open(f"{OUT}/footer.svg", "w", encoding="utf-8").write(foot)
print("ok")
