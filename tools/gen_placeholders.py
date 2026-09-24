#!/usr/bin/env python3
"""Generate placeholder kitchen illustrations (SVG) into images/.

Run: python3 tools/gen_placeholders.py
Replace the generated files with real project photos when available.
"""
import os
import random

OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
W, H = 1600, 1000


def shade(hex_color, f):
    """Lighten (f>0) or darken (f<0) a hex color."""
    h = hex_color.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f >= 0:
        r, g, b = (int(c + (255 - c) * f) for c in (r, g, b))
    else:
        r, g, b = (int(c * (1 + f)) for c in (r, g, b))
    return f'#{r:02x}{g:02x}{b:02x}'


def defs(v, uid):
    grain = ''.join(
        f'<path d="M0 {y} Q 20 {y + random.uniform(-3, 3):.1f} 40 {y} T 80 {y}" stroke="{shade(v["cab"], -0.25)}" '
        f'stroke-width="{random.uniform(0.6, 1.6):.1f}" fill="none" opacity="{random.uniform(.25, .55):.2f}"/>'
        for y in range(3, 80, 7)
    )
    marble = ''.join(
        f'<path d="M{random.randint(0, 400)} 0 Q {random.randint(0, 400)} 40 {random.randint(0, 400)} 80" '
        f'stroke="#9aa0a6" stroke-width="{random.uniform(.5, 1.5):.1f}" fill="none" opacity=".45"/>'
        for _ in range(7)
    )
    return f'''<defs>
  <linearGradient id="wall{uid}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{shade(v["wall"], .08)}"/><stop offset="1" stop-color="{shade(v["wall"], -.08)}"/>
  </linearGradient>
  <linearGradient id="floor{uid}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{shade(v["floor"], -.1)}"/><stop offset="1" stop-color="{shade(v["floor"], .08)}"/>
  </linearGradient>
  <linearGradient id="led{uid}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff3d6" stop-opacity=".85"/><stop offset="1" stop-color="#fff3d6" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="gloss{uid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="vig{uid}" cx=".5" cy=".45" r=".75">
    <stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/>
  </radialGradient>
  <radialGradient id="glow{uid}" cx=".5" cy="0" r="1">
    <stop offset="0" stop-color="#ffe7b0" stop-opacity=".55"/><stop offset="1" stop-color="#ffe7b0" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grain{uid}" width="80" height="80" patternUnits="userSpaceOnUse">
    <rect width="80" height="80" fill="{v["cab"]}"/>{grain}
  </pattern>
  <pattern id="marble{uid}" width="400" height="80" patternUnits="userSpaceOnUse">
    <rect width="400" height="80" fill="{v["counter"]}"/>{marble}
  </pattern>
  <pattern id="tile{uid}" width="60" height="30" patternUnits="userSpaceOnUse">
    <rect width="60" height="30" fill="{v["splash"]}"/>
    <path d="M0 30 H60 M0 0 V30" stroke="{shade(v["splash"], -.12)}" stroke-width="1.5"/>
  </pattern>
</defs>'''


def door(x, y, w, h, v, uid, fill, kind='door'):
    """A single cabinet front, styled by v['style']."""
    s = v['style']
    out = [f'<rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="{h - 6}" rx="{2 if s == "modern" else 3}" fill="{fill}"/>']
    edge = shade(v['cab_base'], -.22)
    out.append(f'<rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="{h - 6}" fill="none" stroke="{edge}" stroke-width="1.5"/>')
    if s == 'classic':
        m = 16
        out.append(f'<rect x="{x + m}" y="{y + m}" width="{w - 2 * m}" height="{h - 2 * m}" rx="6" fill="none" stroke="{edge}" stroke-width="3"/>')
        out.append(f'<rect x="{x + m + 7}" y="{y + m + 7}" width="{w - 2 * m - 14}" height="{h - 2 * m - 14}" rx="4" fill="none" stroke="{shade(v["cab_base"], .18)}" stroke-width="1.5"/>')
    elif s == 'neoclassic':
        m = 14
        out.append(f'<rect x="{x + m}" y="{y + m}" width="{w - 2 * m}" height="{h - 2 * m}" fill="none" stroke="{edge}" stroke-width="2.5"/>')
    if v.get('gloss'):
        out.append(f'<rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="{h - 6}" fill="url(#gloss{uid})"/>')
    hc = v['handle']
    if s == 'modern':
        if kind == 'drawer':
            out.append(f'<rect x="{x + w * .3}" y="{y + 8}" width="{w * .4}" height="4" rx="2" fill="{hc}"/>')
        elif not v.get('handleless'):
            out.append(f'<rect x="{x + w - 16}" y="{y + (h * .15 if kind == "upper" else 12)}" width="4" height="{min(60, h * .4)}" rx="2" fill="{hc}"/>')
    else:
        if kind == 'drawer':
            out.append(f'<rect x="{x + w / 2 - 18}" y="{y + h / 2 - 3}" width="36" height="6" rx="3" fill="{hc}"/>')
        else:
            cy = y + h - 30 if kind == 'upper' else y + 30
            out.append(f'<circle cx="{x + w - 26}" cy="{cy}" r="6" fill="{hc}"/>')
            out.append(f'<circle cx="{x + w - 27.5}" cy="{cy - 1.5}" r="2" fill="#fff" opacity=".6"/>')
    return ''.join(out)


def scene(v, uid):
    random.seed(uid)
    cab_fill = f'url(#grain{uid})' if v.get('wood') else v['cab']
    up_fill = f'url(#grain{uid})' if v.get('wood_upper', v.get('wood')) and v['upper'] == v['cab'] else v['upper']
    counter_fill = f'url(#marble{uid})' if v.get('marble') else v['counter']
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">', defs(v, uid)]

    # Wall, floor
    p.append(f'<rect width="{W}" height="{H}" fill="url(#wall{uid})"/>')
    p.append(f'<rect y="820" width="{W}" height="{H - 820}" fill="url(#floor{uid})"/>')
    for i in range(0, W, 160):
        p.append(f'<line x1="{i}" y1="820" x2="{i - 60}" y2="{H}" stroke="{shade(v["floor"], -.18)}" stroke-width="1.5" opacity=".6"/>')

    # Ceiling cornice for classic styles
    if v['style'] != 'modern':
        p.append(f'<rect x="60" y="72" width="1480" height="30" fill="{shade(v["upper"], .05)}"/>')
        p.append(f'<rect x="54" y="66" width="1492" height="10" fill="{shade(v["upper"], -.08)}"/>')
        p.append(f'<rect x="66" y="100" width="1468" height="6" fill="{shade(v["upper"], -.15)}"/>')

    # Backsplash
    p.append(f'<rect x="80" y="380" width="1440" height="160" fill="url(#tile{uid})"/>')

    # Window or open shelves on the left upper
    if v.get('window'):
        p.append(f'<rect x="100" y="140" width="500" height="220" fill="#cfe3ee" stroke="{shade(v["upper"], -.2)}" stroke-width="10"/>')
        p.append(f'<rect x="100" y="140" width="500" height="220" fill="url(#gloss{uid})"/>')
        p.append(f'<line x1="350" y1="140" x2="350" y2="360" stroke="{shade(v["upper"], -.2)}" stroke-width="8"/>')
        p.append('<ellipse cx="220" cy="330" rx="140" ry="40" fill="#8fb39a" opacity=".7"/>')
        left_upper = False
    else:
        left_upper = True

    # Upper cabinets
    for (x0, x1) in ([(80, 640)] if left_upper else []) + [(960, 1520)]:
        if v.get('shelves') and x0 == 960:
            for sy in (180, 280):
                p.append(f'<rect x="{x0 + 20}" y="{sy}" width="{x1 - x0 - 40}" height="12" fill="{shade(v["cab_base"], -.1)}"/>')
            for i, (bx, bh, col) in enumerate([(1000, 60, '#e8e2d6'), (1050, 45, '#c9b89a'), (1120, 70, '#f5f1ea'),
                                               (1300, 50, '#7c8b7a'), (1360, 64, '#e8e2d6'), (1440, 40, '#b88a5c')]):
                p.append(f'<rect x="{bx}" y="{180 - bh}" width="40" height="{bh}" rx="8" fill="{col}"/>')
            for bx in range(1000, 1480, 70):
                p.append(f'<ellipse cx="{bx + 20}" cy="{268}" rx="26" ry="8" fill="#f3efe7" stroke="#d8d0c2"/>')
            continue
        n = round((x1 - x0) / 140)
        w = (x1 - x0) / n
        for i in range(n):
            x = x0 + i * w
            glass = v.get('glass') and i % n in (0, n - 1)
            fill = '#b9cad1' if glass else up_fill
            p.append(door(x, 110, w, 270, v, uid, fill, 'upper'))
            if glass:
                p.append(f'<rect x="{x + 22}" y="130" width="{w - 44}" height="230" fill="url(#gloss{uid})"/>')
                p.append(f'<line x1="{x + 22}" y1="245" x2="{x + w - 22}" y2="245" stroke="{shade(v["cab_base"], -.2)}" stroke-width="3"/>')
    # Under-cabinet LED
    if v.get('led'):
        p.append(f'<rect x="80" y="380" width="1440" height="90" fill="url(#led{uid})"/>')

    # Hood
    hc = v.get('hood', '#c5c9cc')
    if v['style'] == 'modern':
        p.append(f'<rect x="770" y="110" width="60" height="200" fill="{hc}"/>')
        p.append(f'<polygon points="680,310 920,310 900,345 700,345" fill="{shade(hc, -.1)}"/>')
    else:
        p.append(f'<rect x="740" y="102" width="120" height="120" fill="{shade(v["upper"], .02)}"/>')
        p.append(f'<polygon points="740,222 860,222 930,330 670,330" fill="{v["upper"]}" stroke="{shade(v["upper"], -.2)}" stroke-width="2"/>')
        p.append(f'<rect x="660" y="330" width="280" height="22" fill="{shade(v["upper"], -.1)}"/>')

    # Lower cabinets
    p.append(f'<rect x="80" y="800" width="1440" height="20" fill="{shade(v["cab_base"], -.45)}"/>')
    n = 10
    w = 1440 / n
    for i in range(n):
        x = 80 + i * w
        if i in (0, 4, 7):
            for j in range(3):
                p.append(door(x, 560 + j * 80, w, 80, v, uid, cab_fill, 'drawer'))
        elif i == 5:
            p.append(door(x, 560, w, 240, v, uid, cab_fill, 'door'))
            p.append(f'<rect x="{x + 10}" y="{566}" width="{w - 20}" height="36" fill="#1e1f21" opacity=".75"/>')  # oven window
        else:
            p.append(door(x, 560, w, 240, v, uid, cab_fill, 'door'))
    # Countertop
    p.append(f'<rect x="70" y="536" width="1460" height="26" fill="{counter_fill}"/>')
    p.append(f'<rect x="70" y="558" width="1460" height="4" fill="#000" opacity=".15"/>')
    # Cooktop, sink, accessories
    p.append('<rect x="700" y="530" width="200" height="8" rx="2" fill="#1c1c1e"/>')
    p.append(f'<path d="M 330 536 v -60 q 0 -26 26 -26 h 14" stroke="{v["handle"] if v["style"] != "modern" else "#9aa0a6"}" stroke-width="7" fill="none"/>')
    p.append('<rect x="1180" y="486" width="46" height="50" rx="8" fill="#e9e4db"/><path d="M1190 486 q 2 -40 -30 -60 q 35 5 44 60" fill="#6f9a74"/><path d="M1210 486 q 10 -50 40 -64 q -26 30 -28 64" fill="#86b08a"/>')
    p.append('<rect x="1300" y="500" width="70" height="36" rx="6" fill="#d7c3a4"/><rect x="1380" y="470" width="30" height="66" rx="4" fill="#fff" opacity=".8"/>')

    # Island
    if v.get('island'):
        isl = v.get('island_color', v['cab'])
        isl_fill = f'url(#grain{uid})' if v.get('wood') and isl == v['cab'] else isl
        p.append(f'<ellipse cx="800" cy="945" rx="450" ry="22" fill="#000" opacity=".22"/>')
        p.append(f'<rect x="380" y="680" width="840" height="260" fill="{isl_fill}"/>')
        for i in range(6):
            p.append(door(380 + i * 140, 684, 140, 256, v, uid, isl_fill, 'door'))
        p.append(f'<rect x="350" y="654" width="900" height="30" fill="{counter_fill}"/>')
        p.append(f'<rect x="350" y="680" width="900" height="4" fill="#000" opacity=".15"/>')
        if v.get('island_waterfall'):
            p.append(f'<rect x="350" y="654" width="30" height="286" fill="{counter_fill}"/><rect x="1220" y="654" width="30" height="286" fill="{counter_fill}"/>')
        # stools
        for sx in (500, 800, 1100):
            p.append(f'<rect x="{sx - 36}" y="760" width="72" height="18" rx="9" fill="{v.get("stool", "#2b2b2b")}"/>')
            p.append(f'<path d="M{sx - 26} 778 L{sx - 36} 950 M{sx + 26} 778 L{sx + 36} 950" stroke="{v.get("stool", "#2b2b2b")}" stroke-width="6"/>')
            p.append(f'<line x1="{sx - 32}" y1="880" x2="{sx + 32}" y2="880" stroke="{v.get("stool", "#2b2b2b")}" stroke-width="4"/>')

    # Pendant lights
    if v.get('pendants'):
        for lx in (560, 800, 1040):
            p.append(f'<line x1="{lx}" y1="0" x2="{lx}" y2="400" stroke="#222" stroke-width="2"/>')
            p.append(f'<ellipse cx="{lx}" cy="470" rx="120" ry="140" fill="url(#glow{uid})"/>')
            p.append(f'<path d="M{lx - 40} 440 Q {lx} 380 {lx + 40} 440 Z" fill="{v.get("pendant", "#1f1f1f")}"/>')
            p.append(f'<ellipse cx="{lx}" cy="440" rx="40" ry="6" fill="#fff4d1"/>')

    p.append(f'<rect width="{W}" height="{H}" fill="url(#vig{uid})"/>')
    p.append('</svg>')
    return '\n'.join(p)


BASE = dict(style='modern', wall='#ece7df', floor='#b89b7a', splash='#f1ede6', counter='#f4f2ee', handle='#2b2b2b')

VARIANTS = {
    # Hero & feature imagery
    'hero': dict(cab='#9a6b43', upper='#2f3336', wood=True, wood_upper=False, counter='#eeece8', marble=True,
                 splash='#e9e4dc', wall='#d9d4cc', floor='#8a6d52', island=True, island_color='#2f3336',
                 island_waterfall=True, pendants=True, pendant='#b08a5a', led=True, handle='#1a1a1a'),
    'why-us': dict(style='neoclassic', cab='#f3efe8', upper='#f3efe8', counter='#e9e6e1', marble=True,
                   handle='#c9a45c', wall='#e6dfd3', splash='#f7f4ee', glass=True, window=True),
    'cta': dict(cab='#b07a4c', upper='#b07a4c', wood=True, counter='#2d2f31', splash='#3a3d40',
                wall='#2a2d30', floor='#5a4636', led=True, pendants=True, island=True, handleless=True),
    # Gallery
    'g1-modern-gray': dict(cab='#8c9196', upper='#8c9196', counter='#f2f1ee', splash='#e6e3de', handle='#3a3a3a', led=True),
    'g2-classic-oak': dict(style='classic', cab='#b7874f', upper='#b7874f', wood=True, counter='#d9cbb5', marble=True,
                           handle='#8a6a2e', wall='#efe4d2', splash='#eadcc6', glass=True),
    'g3-neoclassic-white': dict(style='neoclassic', cab='#f7f5f1', upper='#f7f5f1', counter='#ecebe8', marble=True,
                                handle='#c9a45c', wall='#e9e3d8', island=True, pendants=True, pendant='#c9a45c', stool='#c9a45c'),
    'g4-modern-black-gloss': dict(cab='#1d1f21', upper='#1d1f21', gloss=True, counter='#f1f0ec', marble=True,
                                  splash='#dcd8d2', handleless=True, island=True, island_waterfall=True, led=True,
                                  wall='#cfcac2', hood='#2a2c2e'),
    'g5-classic-walnut': dict(style='classic', cab='#6e4a2f', upper='#6e4a2f', wood=True, counter='#e3dccf',
                              handle='#c7a15a', wall='#e8dcc8', splash='#e6d8c0', shelves=True),
    'g6-neoclassic-olive': dict(style='neoclassic', cab='#6b7358', upper='#c79a68', counter='#efece6', marble=True,
                                handle='#c9a45c', wall='#ebe4d6', splash='#f3efe7', shelves=True),
    'g7-modern-white': dict(cab='#f6f6f4', upper='#f6f6f4', handleless=True, gloss=True, counter='#d9d6d0',
                            wall='#e3e1dc', splash='#f0efec', window=True, floor='#c9b499'),
    'g8-classic-cream': dict(style='classic', cab='#efe3cc', upper='#efe3cc', counter='#d8c7a6', marble=True,
                             handle='#b08a3e', wall='#e7dccb', splash='#efe6d6', glass=True, island=True),
    'g9-neoclassic-gray': dict(style='neoclassic', cab='#bfc3c4', upper='#d9dbdb', counter='#f3f2ef', marble=True,
                               handle='#b9b9b9', wall='#e4e2de', led=True, glass=True),
    # Testimonials
    't1-riyadh': dict(cab='#5f6468', upper='#e9e7e3', counter='#f2f0ec', marble=True, led=True, island=True,
                      island_color='#9a6b43', pendants=True),
    't2-jeddah': dict(style='neoclassic', cab='#3c4a5a', upper='#f3f1ec', counter='#f1efea', marble=True,
                      handle='#c9a45c', window=True),
    't3-kuwait': dict(cab='#fbfbfa', upper='#fbfbfa', gloss=True, counter='#c9b79c', handleless=True,
                      wall='#ebe8e2', splash='#e5dfd4', shelves=True),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, over in VARIANTS.items():
        v = {**BASE, **over}
        v['cab_base'] = v['cab']
        with open(os.path.join(OUT, f'{name}.svg'), 'w') as f:
            f.write(scene(v, name.replace('-', '')))
        print('wrote', name)


if __name__ == '__main__':
    main()
