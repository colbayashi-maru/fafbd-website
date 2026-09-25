#!/usr/bin/env python3
"""
Derives every logo and icon the site serves from the four supplied brand files.

    python3 tools/make-assets.py

`brand/` holds the files as the designer supplied them and is never edited.
Everything in `public/assets/` that carries the mark is generated from them by
this script, so there is no hand-traced art anywhere and a brand revision is a
matter of replacing the source file and re-running this.

The supplied files are all drawn for light grounds — the mark and wordmark are
the brand's dark slate, #2B3439. The site's header and footer are that same
slate, so this script derives the reversed variants by recolouring, which is
the only change it makes to the artwork.

The PNG rasters need headless Chrome and a local server; see the README. This
script writes the SVGs only.
"""

import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join(HERE, 'brand')
OUT = os.path.join(HERE, 'public', 'assets')

# The two colours in every supplied file.
SLATE = '#2b3439'      # as written in the source files (lower case)
GOLD = '#f0b743'

# What they become on a dark ground. The gold is left exactly as supplied —
# it reads at 6.99:1 on the brand slate, so there is no reason to touch it.
SLATE_REVERSED = '#FFFFFF'


def read(name):
    with open(os.path.join(BRAND, name), encoding='utf-8') as fh:
        return fh.read()


def write(name, text):
    path = os.path.join(OUT, name)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print(f'  {name:<34} {len(text):>7,}b')


def reverse(svg):
    """Recolour a light-ground file for a dark ground. Gold is untouched."""
    out = re.sub(SLATE, SLATE_REVERSED, svg, flags=re.I)
    if out == svg:
        raise SystemExit('no slate found — has the brand file changed colour?')
    return out


def viewbox(svg):
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    return float(m.group(1)), float(m.group(2))


def favicon(mark):
    """
    The mark alone on its own slate ground, padded into a square.

    A round icon mask crops a circle out of the square, and the mark is very
    wide — 2.7:1 — so it is scaled to leave a margin on all four sides rather
    than fitted edge to edge. The gold stays gold and the dark strokes of the
    A become white, because the ground behind them is now dark.
    """
    w, h = viewbox(mark)
    box, pad = 512, 40
    scale = (box - pad * 2) / w
    dx, dy = pad, (box - h * scale) / 2

    inner = re.search(r'<g id="Layer_1-2".*?</g>\s*</svg>', mark, re.S).group(0)
    inner = inner[:inner.rindex('</svg>')].rstrip()

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {box} {box}"'
        ' role="img" aria-label="First Asset Financial">\n'
        f'  <rect width="{box}" height="{box}" rx="64" fill="#2B3439"/>\n'
        f'  <g transform="translate({dx} {dy:.2f}) scale({scale:.5f})">\n'
        f'    <style>.cls-1{{fill:{GOLD.upper()}}}.cls-2{{fill:#FFFFFF}}</style>\n'
        f'    {inner}\n'
        '  </g>\n'
        '</svg>\n'
    )


def main():
    lockup = read('faf-lockup.svg')
    full = read('faf-lockup-with-memberships.svg')
    mark = read('faf-mark.svg')
    wordmark = read('faf-wordmark.svg')

    print('Deriving from brand/ into public/assets/')

    # What the site actually uses: the lockup without the membership line,
    # reversed for the slate header and footer.
    write('faf-lockup-reversed.svg', reverse(lockup))
    write('faf-lockup.svg', lockup)

    # The full lockup, for anything wide enough to read the membership line.
    # The social card uses the reversed one.
    write('faf-lockup-full-reversed.svg', reverse(full))
    write('faf-lockup-full.svg', full)

    # The mark and wordmark on their own, kept for print and future use.
    write('faf-mark.svg', mark)
    write('faf-mark-reversed.svg', reverse(mark))
    write('faf-wordmark.svg', wordmark)

    write('favicon.svg', favicon(mark))

    for name, svg in [('faf-lockup.svg', lockup), ('faf-lockup-full.svg', full),
                      ('faf-mark.svg', mark)]:
        w, h = viewbox(svg)
        print(f'  {name:<34} aspect {w / h:.3f}:1')


if __name__ == '__main__':
    main()
