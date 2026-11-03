"""Server-drawn share images for published profiles (Open Graph cards for X and Bluesky).

The ridge pattern mirrors apps/arena/public/glyph.js: each value bends the ridges at its own angle.
"""

import io
import math
import os
import pathlib
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

FONTS = pathlib.Path(
    os.environ.get("ARENA_FONTS_DIR")
    or pathlib.Path(__file__).resolve().parents[4] / "apps/arena/fonts"
)
RINGS = 15
PAPER, INK, MUTED, RIDGE = (233, 237, 242), (27, 36, 48), (93, 104, 119), (47, 75, 217)
WIDTH, HEIGHT = 1200, 630


@lru_cache(maxsize=16)
def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def ridge_points(values: list[int | None], ring: int, cx: float, cy: float, scale: float):
    base = (8 + ring * 5.4) * scale
    n = len(values)
    points = []
    for i in range(181):
        t = i / 180 * math.tau
        bend = 0.0
        for k, v in enumerate(values):
            if v is None:
                continue
            theta = k / n * math.tau + ring * 0.035
            d = math.atan2(math.sin(t - theta), math.cos(t - theta))
            width = 0.22 + (k % 3) * 0.05
            amp = 0.25 if v == 0 else v * (1.1 + ring * 0.12)
            bend += amp * math.exp(-(d * d) / (2 * width * width))
        r = base + bend * scale * 2.2
        x = cx + r * math.cos(t) * 0.86
        y = cy + r * math.sin(t) * 1.04 + (ring * 0.25 * scale if math.sin(t) > 0 else 0)
        points.append((x, y))
    return points


def draw_glyph(img: Image.Image, values: list[int | None], box: tuple[int, int, int]) -> None:
    """Draw the print centred in a square box (x, y, size), supersampled for smooth lines."""
    x0, y0, size = box
    ss = 3
    layer = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    scale = size * ss / 200
    for ring in range(RINGS):
        alpha = int(255 * (1 - ring * 0.035))
        width = max(1, round((1.7 - ring * 0.05) * scale))
        pts = ridge_points(values, ring, size * ss / 2, size * ss / 2, scale)
        draw.line(pts, fill=(*RIDGE, alpha), width=width, joint="curve")
    layer = layer.resize((size, size), Image.Resampling.LANCZOS)
    img.paste(layer, (x0, y0), layer)


def wrap(draw: ImageDraw.ImageDraw, text: str, f, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=f) > width and line:
            lines.append(line)
            line = word
        else:
            line = test
    return lines + ([line] if line else [])


def profile_card(profile: dict, names: dict[str, str]) -> bytes:
    """The 1200x630 preview: print on the left; who, where they sit, and the twist on the right."""
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)
    draw_glyph(img, profile["glyph"], (60, 80, 440))
    summary = profile["summary"]
    left, right = 560, WIDTH - 60
    y = 70
    who = profile["display_name"]
    if profile.get("handle"):
        who = (
            f"{who}  @{profile['handle']}"
            if profile["display_name"] != profile["handle"]
            else f"@{who}"
        )
    draw.text((left, y), who[:60], font=font("IBMPlexSansCondensed-Medium.ttf", 30), fill=MUTED)
    y += 56
    for line in wrap(
        draw,
        f"Closest to the {summary['home']}",
        font("IBMPlexSansCondensed-SemiBold.ttf", 56),
        right - left,
    )[:2]:
        draw.text((left, y), line, font=font("IBMPlexSansCondensed-SemiBold.ttf", 56), fill=INK)
        y += 62
    y += 18
    body = font("IBMPlexSansCondensed-Medium.ttf", 30)
    for t in summary["nearest"][:3]:
        draw.text((left, y), str(names.get(t["id"], t["id"])), font=body, fill=INK)
        score = f"{t['k']} of {t['n']}"
        draw.text((right - draw.textlength(score, font=body), y), score, font=body, fill=MUTED)
        y += 42
    twist = (summary.get("signature") or [None])[0]
    if twist:
        y += 16
        verb = "that" if twist["answer"] == 1 else "against"
        line = f"…but sides with the {twist['ally']} {verb} “{twist['text']}”"
        serif = font("Newsreader-Italic.ttf", 28)
        for part in wrap(draw, line, serif, right - left)[:4]:
            draw.text((left, y), part, font=serif, fill=INK)
            y += 36
    foot = "AI Futures Fingerprint, by Dialogos. Answer 24 statements and see where you sit."
    draw.text((40, HEIGHT - 52), foot, font=font("IBMPlexSansCondensed-Medium.ttf", 22), fill=MUTED)
    out = io.BytesIO()
    img.save(out, "PNG", optimize=True)
    return out.getvalue()
