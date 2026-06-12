"""Prépare la photo du hero : recadre le bandeau bas (logo vidéaste),
convertit en WebP optimisé → app/static/img/hero.webp.

Usage : python scripts/prep_hero.py app/static/img/hero-source.png
"""
import sys
from pathlib import Path

from PIL import Image

src = Path(sys.argv[1])
img = Image.open(src).convert("RGB")
w, h = img.size
img = img.crop((0, 0, w, int(h * 0.91)))          # coupe ~9 % en bas (filigrane)
if img.width > 1920:                               # jamais d'upscale
    r = 1920 / img.width
    img = img.resize((1920, int(img.height * r)), Image.LANCZOS)
out = Path("app/static/img/hero.webp")
img.save(out, "WEBP", quality=82, method=6)
print(f"{out} — {img.size[0]}x{img.size[1]}, {out.stat().st_size // 1024} Ko")
