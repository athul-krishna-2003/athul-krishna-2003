"""Animated stats panel: odometer counters, growing bars, self-drawing line.

>>> EDIT THE CONFIG BELOW WITH YOUR REAL NUMBERS, then run: python3 build_stats.py <<<
The values shipped here are PLACEHOLDERS.
"""
import os

# ============================ CONFIG: your numbers ===========================
COUNTERS = [  # (value, suffix, label)
    (3, "+", "YEARS BUILDING"),
    (40, "+", "SITES SHIPPED"),
    (25, "+", "CLIENTS"),
    (100, "%", "ON-TIME HANDOVERS"),
]
SKILLS = [  # (name, level 0-100, self-rated)
    ("HTML / CSS", 92),
    ("JavaScript", 88),
    ("React / Next.js", 85),
    ("TypeScript", 78),
    ("Node.js", 70),
    ("Figma", 72),
]
CHART_TITLE = "SITES SHIPPED, 2026"
MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O"]
MONTHLY = [1, 2, 2, 4, 3, 5, 4, 6, 5, 7]
# =============================================================================

OUT = "assets"
os.makedirs(OUT, exist_ok=True)

INK, LINE, PAPER, CODE, MUTED, PEN = "#0e0f12", "#24262b", "#e9e4d6", "#d8d4c8", "#9a9a93", "#ff5a36"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
EASE = "cubic-bezier(.2,.8,.2,1)"

W, H, D = 1000, 500, 16.0


def pct(t):
    return round(t / D * 100, 3)


css, body, rm = [], [], []

# --- whole panel fades in / holds / fades out so the loop resets unseen ----
css.append(f"@keyframes all{{0%{{opacity:0}}2%,90%{{opacity:1}}96%,100%{{opacity:0}}}}.all{{animation:all {D}s linear infinite}}")

body.append(f'<text x="60" y="56" font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="{MUTED}">BY THE NUMBERS</text>')

# --- odometer counters ------------------------------------------------------
DW, LH, FS = 34, 64, 58
col_w = 220
uid = 0
for ci, (val, suffix, label) in enumerate(COUNTERS):
    x0, y0 = 60 + ci * col_w, 142
    digits = str(val)
    for di, ch in enumerate(digits):
        d = int(ch)
        cx = x0 + di * DW + DW / 2
        uid += 1
        t0 = 0.4 + ci * 0.15 + di * 0.12
        t1 = t0 + 1.8
        dist = d * LH
        css.append(
            f"@keyframes d{uid}{{0%,{pct(t0)}%{{transform:translateY(0)}}{pct(t1)}%,100%{{transform:translateY(-{dist}px)}}}}"
            f".d{uid}{{animation:d{uid} {D}s {EASE} infinite}}"
        )
        rm.append(f".d{uid}{{transform:translateY(-{dist}px)}}")
        reel = "".join(
            f'<text x="{cx}" y="{y0 + k * LH}" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="{FS}" fill="{PAPER}">{k}</text>'
            for k in range(10)
        )
        body.append(
            f'<clipPath id="cp{uid}"><rect x="{x0 + di * DW}" y="{y0 - 48}" width="{DW}" height="60"/></clipPath>'
            f'<g clip-path="url(#cp{uid})"><g class="d{uid}">{reel}</g></g>'
        )
    sx = x0 + len(digits) * DW + 2
    body.append(f'<text x="{sx}" y="{y0}" font-family="{SANS}" font-weight="700" font-size="{FS}" fill="{PEN}">{suffix}</text>')
    body.append(f'<text x="{x0}" y="{y0 + 34}" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{MUTED}">{label}</text>')

body.append(f'<line x1="60" y1="204" x2="{W-60}" y2="204" stroke="{LINE}"/>')

# --- skill bars -------------------------------------------------------------
body.append(f'<text x="60" y="238" font-family="{MONO}" font-size="12" letter-spacing="2.2" fill="{MUTED}">STACK, SELF-RATED</text>')
BX, BW = 200, 280
for i, (name, lvl) in enumerate(SKILLS):
    y = 276 + i * 38
    t0 = 1.4 + i * 0.22
    t1 = t0 + 1.1
    css.append(
        f"@keyframes b{i}{{0%,{pct(t0)}%{{transform:scaleX(0)}}{pct(t1)}%,100%{{transform:scaleX(1)}}}}"
        f".b{i}{{transform-box:fill-box;transform-origin:0 50%;animation:b{i} {D}s {EASE} infinite}}"
        f"@keyframes n{i}{{0%,{pct(t0+0.6)}%{{opacity:0}}{pct(t1)}%,100%{{opacity:1}}}}.n{i}{{animation:n{i} {D}s linear infinite}}"
    )
    rm.append(f".b{i}{{transform:scaleX(1)}}.n{i}{{opacity:1}}")
    body.append(
        f'<text x="60" y="{y+5}" font-family="{MONO}" font-size="14" fill="{CODE}">{name}</text>'
        f'<rect x="{BX}" y="{y-5}" width="{BW}" height="10" rx="5" fill="{LINE}"/>'
        f'<rect class="b{i}" x="{BX}" y="{y-5}" width="{BW*lvl/100:.1f}" height="10" rx="5" fill="{PEN if i == 0 else PAPER}"/>'
        f'<text class="n{i}" x="{BX+BW+14}" y="{y+5}" font-family="{MONO}" font-size="13" fill="{MUTED}">{lvl}</text>'
    )

# --- line graph ---------------------------------------------------------------
body.append(f'<text x="560" y="238" font-family="{MONO}" font-size="12" letter-spacing="2.2" fill="{MUTED}">{CHART_TITLE}</text>')
GX0, GX1, GY0, GY1 = 580, 940, 276, 440  # left, right, top, baseline
ymax = max(MONTHLY) + 1
n = len(MONTHLY)
pts = [(GX0 + 12 + i * (GX1 - GX0 - 24) / (n - 1), GY1 - v / ymax * (GY1 - GY0)) for i, v in enumerate(MONTHLY)]
for g in range(4):
    gy = GY1 - g * (GY1 - GY0) / 3
    body.append(f'<line x1="{GX0}" y1="{gy:.1f}" x2="{GX1}" y2="{gy:.1f}" stroke="{LINE}"/>')
for (px, _), m in zip(pts, MONTHS):
    body.append(f'<text x="{px:.1f}" y="{GY1+22}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{m}</text>')

seg = [((pts[i+1][0]-pts[i][0])**2 + (pts[i+1][1]-pts[i][1])**2) ** 0.5 for i in range(n - 1)]
L = round(sum(seg)) + 2
LT0, LT1 = 2.0, 5.0
css.append(
    f"@keyframes ln{{0%,{pct(LT0)}%{{stroke-dashoffset:{L}}}{pct(LT1)}%,100%{{stroke-dashoffset:0}}}}"
    f".ln{{stroke-dasharray:{L};stroke-dashoffset:{L};animation:ln {D}s cubic-bezier(.45,.05,.3,1) infinite}}"
    f"@keyframes ar{{0%,{pct(LT1-0.6)}%{{opacity:0}}{pct(LT1+0.6)}%,100%{{opacity:1}}}}.ar{{animation:ar {D}s linear infinite}}"
)
rm.append(f".ln{{stroke-dashoffset:0}}.ar{{opacity:1}}")
area = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" {pts[-1][0]:.1f},{GY1} {pts[0][0]:.1f},{GY1}"
body.append(f'<polygon class="ar" points="{area}" fill="{PEN}" fill-opacity="0.10"/>')
body.append(
    f'<polyline class="ln" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{PEN}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
)
cum = 0
for i, (x, y) in enumerate(pts):
    frac = cum / sum(seg)
    td = LT0 + (LT1 - LT0) * frac * 0.92 + 0.15
    css.append(
        f"@keyframes p{i}{{0%,{pct(td)}%{{opacity:0}}{pct(td+0.3)}%,100%{{opacity:1}}}}.p{i}{{animation:p{i} {D}s linear infinite}}"
    )
    rm.append(f".p{i}{{opacity:1}}")
    last = i == n - 1
    body.append(f'<circle class="p{i}" cx="{x:.1f}" cy="{y:.1f}" r="{5 if last else 3.5}" fill="{PEN if last else INK}" stroke="{PEN}" stroke-width="2"/>')
    if i < n - 1:
        cum += seg[i]
lx, ly = pts[-1]
body.append(f'<text class="p{n-1}" x="{lx:.1f}" y="{ly-14:.1f}" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="15" fill="{PAPER}">{MONTHLY[-1]}</text>')

css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}" + "".join(rm) + "}")

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
  <title id="t">Athul Krishna by the numbers</title>
  <desc id="d">Animated counters, skill bars and a line graph of sites shipped per month.</desc>
  <style>
{chr(10).join(css)}
  </style>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{INK}" stroke="{LINE}"/>
  <g class="all">
{chr(10).join(body)}
  </g>
</svg>
'''
open(f"{OUT}/stats.svg", "w", encoding="utf-8").write(svg)
print("ok")
