#!/usr/bin/env python3
"""Generate every SVG in assets/ (dark + light). Run: python3 scripts/build.py"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", line="#30363d", text="#f0f6fc",
                 mute="#9198a1", accent="#f3f1ee", on_accent="#0e0e10"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", line="#d0d7de", text="#17171a",
                  mute="#6b6b75", accent="#17171a", on_accent="#ffffff"),
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
    b += f'<rect x="40" y="48" width="32" height="4" rx="2" fill="{t["accent"]}"/>'
    b += (f'<text x="40" y="118" font-family="{SANS}" font-size="56" font-weight="800" '
          f'letter-spacing="-2" fill="{t["text"]}">Oliver Seidl</text>')
    b += (f'<text x="40" y="154" font-family="{FONT}" font-size="16" fill="{t["mute"]}">'
          f'Student &amp; Software Engineer · Prague</text>')
    b += (f'<text x="40" y="190" font-family="{SANS}" font-size="17" fill="{t["mute"]}">'
          f'I build keyboard-first tools and web apps with TypeScript and Rust.</text>')
    label = "Open for freelance work"
    pw = w(label, 14) + 48
    b += f'<rect x="40" y="210" width="{pw}" height="30" rx="15" fill="{t["panel"]}" stroke="{t["line"]}"/>'
    b += f'<circle cx="58" cy="225" r="5" fill="#3ddc84"/>'
    b += f'<text x="72" y="230" font-family="{FONT}" font-size="14" fill="{t["text"]}">{label}</text>'
    save("hero", t["name"], b, W, H)


def main():
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        hero({**t, "name": name})
    print("done:", len(list(OUT.glob("*.svg"))), "svgs")


if __name__ == "__main__":
    main()
