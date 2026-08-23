"""Assemble export/slide-NN.png into export/discussant-slides.pdf (run after `bun run export`).

Playwright captures at deviceScaleFactor 2 (3840x2160); pages are downscaled to 1920x1080
so the PDF stays email-sized (~4 MB) while remaining crisp on a projector.
"""
import glob
from PIL import Image

pngs = sorted(glob.glob("export/slide-*.png"))
assert pngs, "no export/slide-*.png found — run `bun run export` first"
frames = []
for p in pngs:
    im = Image.open(p).convert("RGB")
    if im.size != (1920, 1080):
        im = im.resize((1920, 1080), Image.LANCZOS)
    frames.append(im)
out = "export/discussant-slides.pdf"
frames[0].save(out, save_all=True, append_images=frames[1:], resolution=72.0)
print(f"wrote {out} ({len(frames)} pages)")
