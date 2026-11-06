#!/usr/bin/env python3
"""Generate every SVG in assets/ (dark + light). Run: python3 scripts/build.py"""
import json
import subprocess
from datetime import date
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0e0e10", panel="#16161a", line="#2a2a31", text="#f3f1ee",
                 mute="#9a9aa4", accent="#ff6a3d", on_accent="#0e0e10",
                 heat=["#1d1d22", "#5a2a1c", "#9c3f24", "#d9552f", "#ff6a3d"]),
    "light": dict(bg="#f7f4ef", panel="#ffffff", line="#ddd8cf", text="#17171a",
                  mute="#6b6b75", accent="#e2511f", on_accent="#ffffff",
                  heat=["#e9e4da", "#f6c9b8", "#f0976f", "#e2511f", "#b83a10"]),
}

CW = 0.6  # mono glyph width ratio


def w(text, size):
    return int(len(text) * size * CW)


def save(name, theme, body, width, height):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img">{body}</svg>')
    (OUT / f"{name}-{theme}.svg").write_text(svg)


def hero(t):
    W, H = 900, 260
    b = f'<rect width="{W}" height="{H}" rx="20" fill="{t["bg"]}" stroke="{t["line"]}"/>'
    b += f'<rect x="40" y="48" width="44" height="6" rx="3" fill="{t["accent"]}"/>'
    b += (f'<text x="40" y="118" font-family="{SANS}" font-size="56" font-weight="800" '
          f'letter-spacing="-2" fill="{t["text"]}">Oliver Seidl</text>')
    b += (f'<text x="40" y="154" font-family="{FONT}" font-size="18" fill="{t["accent"]}">'
          f'Student &amp; Software Engineer · Prague</text>')
    b += (f'<text x="40" y="190" font-family="{SANS}" font-size="17" fill="{t["mute"]}">'
          f'I build keyboard-first tools and web apps with TypeScript and Rust.</text>')
    label = "Open for freelance work"
    pw = w(label, 14) + 48
    b += f'<rect x="40" y="210" width="{pw}" height="30" rx="15" fill="{t["panel"]}" stroke="{t["line"]}"/>'
    b += f'<circle cx="58" cy="225" r="5" fill="#3ddc84"/>'
    b += f'<text x="72" y="230" font-family="{FONT}" font-size="14" fill="{t["text"]}">{label}</text>'
    # decorative prompt block
    b += (f'<text x="{W-40}" y="62" text-anchor="end" font-family="{FONT}" font-size="14" '
          f'fill="{t["mute"]}" opacity="0.7">~/oliver $ whoami</text>')
    save("hero", t["name"], b, W, H)


def wrap(text, width_chars):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width_chars and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


PROJECTS = [
    ("freelancer-crm", "TypeScript",
     "Keyboard-first, local-first CRM and project tracker for solo freelancers, with a REST API and MCP for AI agents."),
    ("tamagotchi", "Rust",
     "A pixel-art tamagotchi that lives in a window, in your status bar and in your shell."),
    ("slophoot", "TypeScript",
     "Self-hosted Kahoot-style quiz. A host opens a room, players join live with a PIN."),
]


def card(t, name, lang, desc):
    W, H = 290, 190
    b = f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["panel"]}" stroke="{t["line"]}"/>'
    b += f'<rect x="24" y="26" width="28" height="4" rx="2" fill="{t["accent"]}"/>'
    b += (f'<text x="24" y="62" font-family="{FONT}" font-size="19" font-weight="700" '
          f'fill="{t["text"]}">{escape(name)}</text>')
    for i, line in enumerate(wrap(desc, 34)[:4]):
        b += (f'<text x="24" y="{90 + i*20}" font-family="{SANS}" font-size="13" '
              f'fill="{t["mute"]}">{escape(line)}</text>')
    b += f'<circle cx="30" cy="{H-24}" r="5" fill="{t["accent"]}"/>'
    b += (f'<text x="42" y="{H-20}" font-family="{FONT}" font-size="12" '
          f'fill="{t["text"]}">{lang}</text>')
    b += (f'<text x="{W-24}" y="{H-20}" text-anchor="end" font-family="{FONT}" '
          f'font-size="12" fill="{t["accent"]}">view repo →</text>')
    save(f"card-{name}", t["name"], b, W, H)


def pills(t, name, items, height=36, size=14, gap=10, pad=18):
    x, b = 0, ""
    for label in items:
        pw = w(label, size) + pad * 2
        b += (f'<rect x="{x+.5}" y=".5" width="{pw-1}" height="{height-1}" rx="{height/2}" '
              f'fill="{t["panel"]}" stroke="{t["line"]}"/>')
        b += (f'<text x="{x+pad}" y="{height/2+size*0.35}" font-family="{FONT}" '
              f'font-size="{size}" fill="{t["text"]}">{escape(label)}</text>')
        x += pw + gap
    save(name, t["name"], b, x - gap, height)


def button(t, key, label):
    size, h, pad = 14, 40, 22
    bw = w(label, size) + pad * 2
    b = f'<rect width="{bw}" height="{h}" rx="20" fill="{t["accent"]}"/>'
    b += (f'<text x="{bw/2}" y="{h/2+5}" text-anchor="middle" font-family="{FONT}" '
          f'font-size="{size}" font-weight="700" fill="{t["on_accent"]}">{escape(label)}</text>')
    save(f"btn-{key}", t["name"], b, bw, h)


def activity(t, days):
    cell, gap, left, top = 11, 3, 40, 52
    weeks = [days[i:i+7] for i in range(0, len(days), 7)]
    W = left + len(weeks) * (cell + gap) + 30
    H = top + 7 * (cell + gap) + 40
    total = sum(d["contributionCount"] for d in days)
    counts = sorted(d["contributionCount"] for d in days if d["contributionCount"])
    q = [counts[int(len(counts) * p)] for p in (0.25, 0.5, 0.75)] if counts else [1, 2, 3]

    def level(c):
        if c == 0:
            return 0
        return 1 + sum(c > x for x in q)

    b = f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["bg"]}" stroke="{t["line"]}"/>'
    b += (f'<text x="{left}" y="34" font-family="{FONT}" font-size="14" fill="{t["text"]}">'
          f'<tspan font-weight="700" fill="{t["accent"]}">{total}</tspan> contributions in the last year</text>')
    for wi, wk in enumerate(weeks):
        for di, d in enumerate(wk):
            x = left + wi * (cell + gap)
            y = top + di * (cell + gap)
            b += (f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" '
                  f'fill="{t["heat"][level(d["contributionCount"])]}"/>')
    for di, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        b += (f'<text x="{left-8}" y="{top + di*(cell+gap) + 10}" text-anchor="end" '
              f'font-family="{FONT}" font-size="10" fill="{t["mute"]}">{lab}</text>')
    lx = W - 30 - 5 * (cell + gap) - 70
    b += f'<text x="{lx}" y="{H-14}" font-family="{FONT}" font-size="10" fill="{t["mute"]}">less</text>'
    for i, c in enumerate(t["heat"]):
        b += f'<rect x="{lx + 30 + i*(cell+gap)}" y="{H-24}" width="{cell}" height="{cell}" rx="3" fill="{c}"/>'
    b += (f'<text x="{lx + 30 + 5*(cell+gap) + 4}" y="{H-14}" font-family="{FONT}" '
          f'font-size="10" fill="{t["mute"]}">more</text>')
    save("activity", t["name"], b, W, H)


def fetch_days():
    q = ('{viewer{contributionsCollection{contributionCalendar{weeks{contributionDays'
         '{contributionCount date}}}}}}')
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}"],
                         check=True, capture_output=True, text=True).stdout
    weeks = json.loads(out)["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [d for wk in weeks for d in wk["contributionDays"]]
    while len(days) % 7:  # pad last week
        days.append({"contributionCount": 0, "date": str(date.today())})
    return days


def main():
    OUT.mkdir(exist_ok=True)
    days = fetch_days()
    for name, t in THEMES.items():
        t = {**t, "name": name}
        hero(t)
        for p in PROJECTS:
            card(t, *p)
        pills(t, "stack", ["TypeScript", "Rust", "Python", "Next.js", "Shell"])
        activity(t, days)
        button(t, "mail", "✉  Email")
        button(t, "web", "↗  oliverseidl.dev")
        button(t, "in", "in  LinkedIn")
        button(t, "ig-dev", "◎  @oliverseidl.dev")
        button(t, "ig-me", "◎  @olinkkt")
    print("done:", len(list(OUT.glob("*.svg"))), "svgs")


if __name__ == "__main__":
    main()
