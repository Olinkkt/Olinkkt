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
    i += text(56, 332, "I build keyboard-first tools and web apps with TypeScript and Rust.", 17, MUTE)
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
    # status pill
    px, py = 640, 316
    i += glass(px, py, 214, 36, 18, .08)
    i += (f'<circle cx="{px+20}" cy="{py+18}" r="5" fill="#3ddc84"/>'
          f'<circle cx="{px+20}" cy="{py+18}" r="5" fill="none" stroke="#3ddc84" stroke-width="2">'
          f'<animate attributeName="r" values="5;12" dur="1.8s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values=".9;0" dur="1.8s" repeatCount="indefinite"/></circle>')
    i += text(px + 36, py + 23, "Open for freelance work", 13, INK, 600, MONO)
    save("hero", frame(u, H, i, "#7c5cff", "#d9ccff", blobs), W, H)


# ---------------------------------------------------------------- projects
def tags(x, y, items, col):
    s = ""
    for t in items:
        w = int(len(t) * 7.6) + 24
        s += (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{col}" fill-opacity=".14" '
              f'stroke="{col}" stroke-opacity=".45"/>')
        s += text(x + 12, y + 17, t, 12, INK, 600, MONO)
        x += w + 8
    return s


def project(name, idx, title, lines, tg, hue_a, hue_b, art):
    H, u = 250, name[:2]
    blobs = [blob(u, 760, 60, 150, hue_a, -50, 40, 15), blob(u, 600, 240, 110, hue_b, 60, -20, 18, .5)]
    i = text(56, 64, f"{idx}  /  PROJECT", 12, MUTE, 600, MONO, 3)
    i += text(52, 116, title, 46, INK, 800, SANS, -2)
    for n, ln in enumerate(lines):
        i += text(56, 150 + n * 22, ln, 15, MUTE)
    i += tags(56, 196, tg, hue_a)
    i += art
    i += text(W - 48, 224, f"github.com/Olinkkt/{name}  →", 12, INK, 600, MONO, 0, "end", .75)
    save(f"project-{name}", frame(u, H, i, hue_a, hue_b, blobs), W, H)


def float_g(inner, dy=6, dur=4):
    return (f'<g>{inner}<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;0 {-dy};0 0" dur="{dur}s" repeatCount="indefinite"/></g>')


def art_crm():
    x0, y0, s = 560, 44, ""
    cols = (("Lead", 3), ("Active", 2), ("Paid", 2))
    for c, (lab, n) in enumerate(cols):
        x = x0 + c * 98
        s += glass(x, y0, 88, 150, 12, .05)
        s += text(x + 12, y0 + 22, lab.upper(), 10, MUTE, 700, MONO, 1.5)
        for k in range(n):
            card = glass(x + 8, y0 + 34 + k * 36, 72, 28, 8, .1)
            card += f'<rect x="{x+16}" y="{y0+44+k*36}" width="{30+k*9}" height="4" rx="2" fill="#fff" opacity=".7"/>'
            card += f'<rect x="{x+16}" y="{y0+52+k*36}" width="22" height="3" rx="1.5" fill="#a78bfa"/>'
            s += float_g(card, 3, 3 + c + k * .7) if (c, k) == (1, 0) else card
    s += glass(x0 + 196 - 60, y0 - 32, 74, 24, 12, .12)
    s += text(x0 + 196 - 23, y0 - 16, "⌘ K", 11, INK, 700, MONO, 0, "middle")
    return s


PET = ["....KKKK....", "..KKYYYYKK..", ".KYYYYYYYYK.", "KYYKYYYYKYYK", "KYYKYYYYKYYK",
       "KYYYYYYYYYYK", "KYPYYYYYYPYK", "KYYYYKKYYYYK", ".KYYYYYYYYK.", "..KKYYYYKK..",
       "..K.K..K.K.."]


def art_tama():
    p, x0, y0 = 9, 640, 52
    col = {"K": "#1a1205", "Y": "#ffc44d", "P": "#ff7a90"}
    px = "".join(f'<rect x="{x0+c*p}" y="{y0+r*p}" width="{p}" height="{p}" fill="{col[ch]}"/>'
                 for r, row in enumerate(PET) for c, ch in enumerate(row) if ch in col)
    s = f'<ellipse cx="{x0+54}" cy="{y0+110}" rx="46" ry="6" fill="#000" opacity=".45"/>'
    s += float_g(px, 8, 1.6)
    for k, (lab, v) in enumerate((("FOOD", 4), ("JOY", 3), ("ZZZ", 5))):
        y = 60 + k * 30
        s += text(780, y + 9, lab, 10, INK, 700, MONO, 1.5)
        for b in range(5):
            on = b < v
            s += (f'<rect x="{820+b*12}" y="{y}" width="9" height="10" rx="1" '
                  f'fill="{"#ffc44d" if on else "#ffffff"}" opacity="{1 if on else .12}"/>')
    return s


def art_slop():
    x0, y0, s = 600, 40, ""
    tiles = (("#e21b3c", "tri"), ("#1368ce", "dia"), ("#d89e00", "cir"), ("#26890c", "sq"))
    for k, (c, shp) in enumerate(tiles):
        x, y = x0 + (k % 2) * 124, y0 + (k // 2) * 62
        s += f'<rect x="{x}" y="{y}" width="116" height="54" rx="10" fill="{c}"/>'
        cx, cy = x + 26, y + 27
        s += {"tri": f'<path d="M{cx},{cy-10} l11,19 h-22z" fill="#fff"/>',
              "dia": f'<path d="M{cx},{cy-11} l11,11 -11,11 -11,-11z" fill="#fff"/>',
              "cir": f'<circle cx="{cx}" cy="{cy}" r="10" fill="#fff"/>',
              "sq": f'<rect x="{cx-9}" y="{cy-9}" width="18" height="18" fill="#fff"/>'}[shp]
        s += f'<rect x="{x+46}" y="{y+24}" width="{48-k*6}" height="6" rx="3" fill="#fff" opacity=".85"/>'
    s += glass(x0 + 50, y0 + 130, 140, 34, 17, .1)
    s += text(x0 + 120, y0 + 152, "PIN  482 913", 14, INK, 700, MONO, 2, "middle")
    return s


# ---------------------------------------------------------------- stack
def stack():
    H, u = 210, "st"
    blobs = [blob(u, 150, 200, 140, "#3178c6", 60, -20, 16, .5), blob(u, 760, 20, 140, "#f74c00", -60, 30, 18, .4)]
    i = text(56, 60, "STACK", 12, MUTE, 600, MONO, 3)
    i += text(W - 56, 60, "daily drivers", 12, MUTE, 600, MONO, 0, "end")
    items = (("TS", "TypeScript", "#5b9dff"), ("RS", "Rust", "#f74c00"), ("PY", "Python", "#ffd43b"),
             ("N", "Next.js", "#ffffff"), ("$_", "Shell", "#4eaa25"))
    tw, gap = 148, 15
    for k, (ab, lab, c) in enumerate(items):
        x = 56 + k * (tw + gap)
        i += glass(x, 86, tw, 92, 16, .05)
        i += (f'<circle cx="{x+34}" cy="132" r="20" fill="{c}" opacity=".18"/>'
              f'<circle cx="{x+34}" cy="132" r="20" fill="none" stroke="{c}" stroke-opacity=".7"/>')
        i += text(x + 34, 137, ab, 13, c, 800, MONO, 0, "middle")
        i += text(x + 62, 137, lab, 14, INK, 700) if len(lab) < 10 else text(x + 60, 137, lab, 13.5, INK, 700)
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


def button(key, glyph, label, col):
    bw, h = 210, 48
    b = (f'<defs><linearGradient id="k" x1="0" x2="1"><stop offset="0" stop-color="{col}" stop-opacity=".28"/>'
         f'<stop offset="1" stop-color="{col}" stop-opacity=".06"/></linearGradient></defs>')
    b += f'<rect x=".5" y=".5" width="{bw-1}" height="{h-1}" rx="24" fill="{BG}"/>'
    b += f'<rect x=".5" y=".5" width="{bw-1}" height="{h-1}" rx="24" fill="url(#k)" stroke="{col}" stroke-opacity=".5"/>'
    b += text(30, 30, glyph, 15, col, 800, MONO, 0, "middle")
    b += text(50, 29, label, 13, INK, 600, MONO)
    save(f"btn-{key}", b, bw, h)


def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.svg"):
        f.unlink()
    hero()
    project("freelancer-crm", "01", "freelancer-crm",
            ["Keyboard-first, local-first CRM for solo", "freelancers, with a REST API and MCP for agents."],
            ["TypeScript", "MCP", "local-first"], "#7c5cff", "#22d3ee", art_crm())
    project("tamagotchi", "02", "tama",
            ["A pixel-art pet that lives in a window,", "in your status bar and in your shell."],
            ["Rust", "pixel art", "CLI"], "#ffb020", "#ff4ecd", art_tama())
    project("slophoot", "03", "slophoot",
            ["Self-hosted Kahoot-style quiz. Host opens a", "room, players join live with a PIN."],
            ["TypeScript", "Next.js", "Socket.io"], "#ff4ecd", "#1368ce", art_slop())
    stack()
    contact()
    button("web", "↗", "oliverseidl.dev", "#22d3ee")
    button("in", "in", "LinkedIn", "#3b82f6")
    button("ig-dev", "◎", "@oliverseidl.dev", "#ff4ecd")
    button("ig-me", "◎", "@olinkkt", "#ffb020")
    print("done:", len(list(OUT.glob("*.svg"))), "svgs")


if __name__ == "__main__":
    main()
