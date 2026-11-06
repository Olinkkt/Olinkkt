#!/usr/bin/env python3
"""Generate every SVG in assets/. Run: python3 scripts/build.py"""
import re
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = "-apple-system, 'Segoe UI', 'Inter', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"
W = 900
BG = "#07070c"
INK = "#f5f3ff"
MUTE = "#a09cb8"
DIM = "#5d5a73"


def defs(uid, hue_a, hue_b):
    return f'''<defs>
<clipPath id="c{uid}"><rect width="{W}" height="100%" rx="24"/></clipPath>
<filter id="b{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="n{uid}"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0"/></filter>
<pattern id="g{uid}" width="36" height="36" patternUnits="userSpaceOnUse">
<path d="M36 0H0V36" fill="none" stroke="#fff" stroke-opacity=".045"/></pattern>
<linearGradient id="t{uid}" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="{hue_b}"/></linearGradient>
<linearGradient id="e{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/>
<stop offset=".5" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="{hue_a}" stop-opacity=".35"/></linearGradient>
</defs>'''


def blob(uid, cx, cy, r, color, dx, dy, dur, op=.75):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{op}" filter="url(#b{uid})">'
            f'<animate attributeName="cx" values="{cx};{cx+dx};{cx}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cy" values="{cy};{cy+dy};{cy}" dur="{dur*1.3:.1f}s" repeatCount="indefinite"/></circle>')


def frame(uid, H, inner, hue_a, hue_b, blobs):
    body = defs(uid, hue_a, hue_b)
    body += f'<g clip-path="url(#c{uid})"><rect width="{W}" height="{H}" fill="{BG}"/>'
    body += "".join(blobs)
    body += f'<rect width="{W}" height="{H}" fill="url(#g{uid})"/>'
    body += f'<rect width="{W}" height="{H}" filter="url(#n{uid})" opacity=".07"/>'
    body += inner + "</g>"
    body += f'<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="23.5" fill="none" stroke="url(#e{uid})" stroke-width="1.5"/>'
    return body


def save(name, body, width, height):
    body = re.sub(r'<animate[^>]*/>', '', body)
    (OUT / f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">{body}</svg>')


def text(x, y, s, size, fill=INK, weight=400, font=SANS, ls=0, anchor="start", op=1):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{ls}" fill="{fill}" text-anchor="{anchor}" opacity="{op}">{escape(s)}</text>')


def glass(x, y, w, h, r=14, op=.06):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" fill-opacity="{op}" '
            f'stroke="#fff" stroke-opacity=".12"/>')


SRC = Path(__file__).resolve().parent / "src"


def logo(name, x, y, size, color):
    """Official brand mark from simple-icons (24x24 viewBox)."""
    d = re.search(r' d="([^"]+)"', (SRC / f"{name}.svg").read_text()).group(1)
    return f'<path transform="translate({x} {y}) scale({size/24})" d="{d}" fill="{color}"/>'


def sprite(name, x, y, px):
    """Real tama sprite, one rect per pixel."""
    import subprocess
    txt = subprocess.run(["magick", str(SRC / f"{name}.png"), "txt:-"],
                         capture_output=True, text=True, check=True).stdout
    out = []
    for m in re.finditer(r"^(\d+),(\d+): \(([\d.]+),([\d.]+),([\d.]+),([\d.]+)\)", txt, re.M):
        cx, cy, r, g, b, a = m.groups()
        if float(a) < 128:
            continue
        out.append(f'<rect x="{x+int(cx)*px}" y="{y+int(cy)*px}" width="{px}" height="{px}" '
                   f'fill="#{int(float(r)):02x}{int(float(g)):02x}{int(float(b)):02x}"/>')
    return "".join(out)


# ---------------------------------------------------------------- hero
def hero():
    H, u = 380, "h"
    blobs = [blob(u, 720, 90, 170, "#7c5cff", -60, 40, 14),
             blob(u, 830, 300, 150, "#ff4ecd", -40, -50, 17, .6),
             blob(u, 560, 330, 120, "#22d3ee", 70, -30, 19, .45)]
    i = text(56, 92, "STUDENT  ·  SOFTWARE ENGINEER  ·  PRAGUE, CZ", 13, MUTE, 600, MONO, 3)
    i += (f'<text x="52" y="196" font-family="{SANS}" font-size="104" font-weight="800" '
          f'letter-spacing="-5" fill="url(#t{u})">Oliver</text>')
    i += (f'<text x="52" y="290" font-family="{SANS}" font-size="104" font-weight="800" '
          f'letter-spacing="-5" fill="url(#t{u})">Seidl<tspan fill="#ff4ecd">.</tspan></text>')
    i += text(56, 332, "I build web app tools, realtime websocket apps and games in Rust.", 17, MUTE)
    # orbit
    cx, cy = 715, 190
    for rx, ry, op in ((150, 54, .16), (112, 40, .12), (74, 26, .1)):
        i += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#fff" stroke-opacity="{op}" transform="rotate(-18 {cx} {cy})"/>'
    for rx, ry, ang, col in ((150, 54, 200, "#ff4ecd"), (112, 40, 300, "#22d3ee"), (74, 26, 60, "#ffffff")):
        import math
        dx, dy = rx * math.cos(math.radians(ang)), ry * math.sin(math.radians(ang))
        i += (f'<g transform="rotate(-18 {cx} {cy})"><circle cx="{cx+dx:.1f}" cy="{cy+dy:.1f}" r="5" fill="{col}"/></g>')
    i += f'<circle cx="{cx}" cy="{cy}" r="16" fill="#fff" opacity=".95"/>'
    i += f'<circle cx="{cx}" cy="{cy}" r="34" fill="#fff" opacity=".08"/>'
    save("hero", frame(u, H, i, "#7c5cff", "#d9ccff", blobs), W, H)


# ---------------------------------------------------------------- projects
TAG_LOGO = {"TypeScript": "typescript", "Rust": "rust", "Next.js": "nextdotjs",
            "Socket.io": "socketdotio", "MCP": "mcp"}


def tags(x, y, items, col):
    s = ""
    for t in items:
        ic = TAG_LOGO.get(t)
        w = int(len(t) * 7.6) + 24 + (20 if ic else 0)
        s += (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{col}" fill-opacity=".14" '
              f'stroke="{col}" stroke-opacity=".45"/>')
        tx = x + 12
        if ic:
            s += logo(ic, x + 11, y + 6, 14, INK)
            tx += 20
        s += text(tx, y + 17, t, 12, INK, 600, MONO)
        x += w + 8
    return s


def project(name, idx, title, lines, tg, hue_a, hue_b, art, kind="PROJECT"):
    H, u = 290, name[:2]
    blobs = [blob(u, 760, 60, 150, hue_a, -50, 40, 15), blob(u, 600, 240, 110, hue_b, 60, -20, 18, .5)]
    i = text(56, 64, f"{idx}  /  {kind}", 12, MUTE, 600, MONO, 3)
    i += text(52, 116, title, 46, INK, 800, SANS, -2)
    for n, ln in enumerate(lines):
        i += text(56, 150 + n * 22, ln, 15, MUTE)
    i += tags(56, 196, tg, hue_a)
    i += art
    i += text(56, 246, f"github.com/Olinkkt/{name}  →", 12, INK, 600, MONO, 0, "start", .75)
    save(f"project-{name}", frame(u, H, i, hue_a, hue_b, blobs), W, H)


def float_g(inner, dy=6, dur=4):
    return (f'<g>{inner}<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;0 {-dy};0 0" dur="{dur}s" repeatCount="indefinite"/></g>')


def art_crm():
    x0, y0, s = 552, 70, ""
    cols = (("Lead", 3), ("Active", 2), ("Paid", 2))
    for c, (lab, n) in enumerate(cols):
        x = x0 + c * 104
        s += glass(x, y0, 88, 150, 12, .05)
        s += text(x + 12, y0 + 22, lab.upper(), 10, MUTE, 700, MONO, 1.5)
        for k in range(n):
            card = glass(x + 8, y0 + 34 + k * 36, 72, 28, 8, .1)
            card += f'<rect x="{x+16}" y="{y0+44+k*36}" width="{30+k*9}" height="4" rx="2" fill="#fff" opacity=".7"/>'
            card += f'<rect x="{x+16}" y="{y0+52+k*36}" width="22" height="3" rx="1.5" fill="#a78bfa"/>'
            s += float_g(card, 3, 3 + c + k * .7) if (c, k) == (1, 0) else card
    return s


def art_tama():
    p, x0, y0 = 3, 586, 58
    s = f'<ellipse cx="{x0+72}" cy="{y0+146}" rx="50" ry="7" fill="#000" opacity=".45"/>'
    s += sprite("mametchi", x0, y0, p)
    for k, (lab, v) in enumerate((("FOOD", 4), ("JOY", 5), ("ZZZ", 3))):
        y = 108 + k * 30
        s += text(758, y + 9, lab, 10, INK, 700, MONO, 1.5)
        for b in range(5):
            on = b < v
            s += (f'<rect x="{800+b*12}" y="{y}" width="9" height="10" rx="1" '
                  f'fill="{"#5cb85c" if on else "#ffffff"}" opacity="{1 if on else .14}"/>')
    return s


def art_slop():
    x0, y0, s = 566, 80, ""
    tiles = (("#e21b3c", "tri"), ("#1368ce", "dia"), ("#d89e00", "cir"), ("#26890c", "sq"))
    for k, (c, shp) in enumerate(tiles):
        x, y = x0 + (k % 2) * 146, y0 + (k // 2) * 72
        s += f'<rect x="{x}" y="{y}" width="132" height="58" rx="12" fill="{c}"/>'
        cx, cy = x + 28, y + 29
        s += {"tri": f'<path d="M{cx},{cy-10} l11,19 h-22z" fill="#fff"/>',
              "dia": f'<path d="M{cx},{cy-11} l11,11 -11,11 -11,-11z" fill="#fff"/>',
              "cir": f'<circle cx="{cx}" cy="{cy}" r="10" fill="#fff"/>',
              "sq": f'<rect x="{cx-9}" y="{cy-9}" width="18" height="18" fill="#fff"/>'}[shp]
        s += f'<rect x="{x+50}" y="{y+26}" width="{48-k*6}" height="6" rx="3" fill="#fff" opacity=".85"/>'
    return s


# ---------------------------------------------------------------- stack
def stack():
    H, u = 210, "st"
    blobs = [blob(u, 150, 200, 140, "#3178c6", 60, -20, 16, .5), blob(u, 760, 20, 140, "#f74c00", -60, 30, 18, .4)]
    i = text(56, 60, "STACK", 12, MUTE, 600, MONO, 3)
    i += text(W - 56, 60, "daily drivers", 12, MUTE, 600, MONO, 0, "end")
    items = (("typescript", "TypeScript", "#3178c6"), ("rust", "Rust", "#f74c00"),
             ("python", "Python", "#ffd43b"), ("nextdotjs", "Next.js", "#ffffff"), ("gnubash", "Shell", "#4eaa25"))
    tw, gap = 148, 12
    for k, (ic, lab, c) in enumerate(items):
        x = 56 + k * (tw + gap)
        i += glass(x, 84, tw, 100, 16, .05)
        col = "#ffffff" if ic in ("nextdotjs", "rust") else ("#5b9dff" if ic == "typescript" else c)
        i += logo(ic, x + tw / 2 - 19, 100, 38, col)
        i += text(x + tw / 2, 165, lab, 14, INK, 700, SANS, 0, "middle")
    save("stack", frame(u, H, i, "#3178c6", "#ffffff", blobs), W, H)


# ---------------------------------------------------------------- contact
def contact():
    H, u = 230, "ct"
    blobs = [blob(u, 450, 260, 200, "#7c5cff", 80, -20, 15, .6),
             blob(u, 120, 0, 120, "#ff4ecd", 40, 30, 18, .45), blob(u, 820, 40, 120, "#22d3ee", -40, 30, 17, .4)]
    i = text(W / 2, 64, "CONTACT", 12, MUTE, 600, MONO, 3, "middle")
    i += (f'<text x="{W/2}" y="128" text-anchor="middle" font-family="{SANS}" font-size="52" '
          f'font-weight="800" letter-spacing="-2" fill="url(#t{u})">Got a project? Write me.</text>')
    i += text(W / 2, 176, "kontakt@oliverseidl.dev", 18, INK, 600, MONO, 0, "middle")
    i += text(W / 2, 202, "click to send an email", 12, MUTE, 600, MONO, 0, "middle")
    save("contact", frame(u, H, i, "#7c5cff", "#ffd1f3", blobs), W, H)


def button(key, glyph, label, col, ic, lpad, rpad):
    bw, h = 225, 48
    rw = bw - lpad - rpad
    b = (f'<defs><linearGradient id="k" x1="0" x2="1"><stop offset="0" stop-color="{col}" stop-opacity=".28"/>'
         f'<stop offset="1" stop-color="{col}" stop-opacity=".06"/></linearGradient></defs>')
    b += f'<rect x="{lpad+.5}" y=".5" width="{rw-1}" height="{h-1}" rx="24" fill="{BG}"/>'
    b += f'<rect x="{lpad+.5}" y=".5" width="{rw-1}" height="{h-1}" rx="24" fill="url(#k)" stroke="{col}" stroke-opacity=".5"/>'
    tw = int(len(label) * 7.8) + (26 if ic else 22)
    x0 = lpad + (rw - tw) / 2
    if ic:
        b += logo(ic, x0, 15, 18, col)
    else:
        b += text(x0 + 9, 30, glyph, 15, col, 800, MONO, 0, "middle")
    b += text(x0 + 26, 29, label, 13, INK, 600, MONO)
    save(f"btn-{key}", b, bw, h)


def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.svg"):
        f.unlink()
    hero()
    project("freelancer-crm", "01", "freelancer-crm",
            ["Keyboard-first, local-first CRM for solo", "freelancers, with a REST API and MCP for agents."],
            ["TypeScript", "MCP", "local-first"], "#7c5cff", "#22d3ee", art_crm(), "WEB APP  ·  TOOL")
    project("tamagotchi", "02", "tama",
            ["A pixel-art pet that lives in a window,", "in your status bar and in your shell."],
            ["Rust", "game", "pixel art"], "#5cb85c", "#f5d061", art_tama(), "GAME  ·  RUST")
    project("slophoot", "03", "slophoot",
            ["Self-hosted Kahoot-style quiz. Host opens a", "room, players join live with a PIN."],
            ["TypeScript", "Next.js", "Socket.io", "websockets"], "#ff4ecd", "#1368ce", art_slop(), "REALTIME  ·  WEBSOCKETS")
    stack()
    contact()
    button("web", "↗", "oliverseidl.dev", "#22d3ee", None, 0, 6)
    button("in", "", "LinkedIn", "#3b82f6", "linkedin", 6, 6)
    button("ig-dev", "", "@oliverseidl.dev", "#ff4ecd", "instagram", 6, 6)
    button("ig-me", "", "@olinkkt", "#ffb020", "instagram", 6, 0)
    print("done:", len(list(OUT.glob("*.svg"))), "svgs")


if __name__ == "__main__":
    main()
