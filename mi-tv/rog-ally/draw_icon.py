"""Draws the ROG Ally tile: an original handheld-console drawing and the name (no ROG logo).

usage: python -I draw_ally_icon.py <res dir>
Writes drawable-xhdpi/banner.png (320x180), drawable-xxxhdpi/banner.png (640x360),
mipmap-xhdpi/ic_launcher.png (96) and mipmap-xxxhdpi/ic_launcher.png (192).
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

RES = sys.argv[1]
RED = (232, 25, 44)
WHITE = (242, 242, 245)
DARK = (20, 21, 28)
S = 4  # supersampling factor, for smooth edges


def font(size):
    for name in ("segoeuib.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", name), size)
        except OSError:
            pass
    return ImageFont.load_default()


def background(w, h):
    img = Image.new("RGB", (w, h))
    px = img.load()
    top, bottom = (16, 17, 23), (30, 10, 14)
    for y in range(h):
        t = y / max(1, h - 1)
        row = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = row
    return img


def console(d, cx, cy, width):
    """Handheld centred on (cx, cy), `width` wide: body, screen, ringed sticks, d-pad, face buttons."""
    w, h = width, width * 0.42
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle((x0, y0, x1, y1), radius=h * 0.42, fill=WHITE)
    # screen
    sw, sh = w * 0.56, h * 0.74
    sx0, sy0 = cx - sw / 2, cy - sh / 2
    d.rounded_rectangle((sx0, sy0, sx0 + sw, sy0 + sh), radius=h * 0.07, fill=DARK)
    d.line((sx0 + sw * 0.62, sy0 + sh * 0.12, sx0 + sw * 0.86, sy0 + sh * 0.12), fill=(60, 30, 36), width=max(1, int(h * 0.025)))
    grip = (w - sw) / 4  # centre of each side panel, measured from the outer edge
    r_stick = h * 0.12
    # left: stick on top, d-pad below; right: face buttons on top, stick below (the Ally's layout)
    lx, rx = x0 + grip + w * 0.02, x1 - grip - w * 0.02
    for (sx, sy) in ((lx, cy - h * 0.18), (rx, cy + h * 0.2)):
        d.ellipse((sx - r_stick * 1.45, sy - r_stick * 1.45, sx + r_stick * 1.45, sy + r_stick * 1.45), outline=RED, width=max(1, int(h * 0.04)))
        d.ellipse((sx - r_stick, sy - r_stick, sx + r_stick, sy + r_stick), fill=DARK)
    px, py, arm, thick = lx, cy + h * 0.22, h * 0.11, h * 0.065
    d.rectangle((px - arm, py - thick / 2, px + arm, py + thick / 2), fill=DARK)
    d.rectangle((px - thick / 2, py - arm, px + thick / 2, py + arm), fill=DARK)
    bx, by, gap, rb = rx, cy - h * 0.18, h * 0.1, h * 0.045
    for (dx, dy) in ((0, -gap), (gap, 0), (0, gap), (-gap, 0)):
        d.ellipse((bx + dx - rb, by + dy - rb, bx + dx + rb, by + dy + rb), fill=DARK)


def banner(w, h):
    big = background(w * S, h * S)
    d = ImageDraw.Draw(big)
    W, H = w * S, h * S
    d.polygon([(W * 0.95, 0), (W * 1.01, 0), (W * 0.89, H), (W * 0.83, H)], fill=(70, 12, 20))   # diagonal accent
    console(d, W * 0.31, H * 0.5, W * 0.46)
    f_rog, f_ally = font(int(H * 0.22)), font(int(H * 0.25))
    tx = W * 0.6
    d.text((tx, H * 0.24), "ROG", font=f_rog, fill=RED)
    d.text((tx, H * 0.47), "Ally", font=f_ally, fill=WHITE)
    return big.resize((w, h), Image.LANCZOS)


def icon(size):
    big = background(size * S, size * S)
    d = ImageDraw.Draw(big)
    console(d, size * S / 2, size * S / 2, size * S * 0.84)
    return big.resize((size, size), Image.LANCZOS)


for folder, img in (("drawable-xhdpi", banner(320, 180)), ("drawable-xxxhdpi", banner(640, 360)),
                    ("mipmap-xhdpi", icon(96)), ("mipmap-xxxhdpi", icon(192))):
    name = "banner.png" if folder.startswith("drawable") else "ic_launcher.png"
    os.makedirs(os.path.join(RES, folder), exist_ok=True)
    img.save(os.path.join(RES, folder, name), optimize=True)
    print(folder, name, img.size)
