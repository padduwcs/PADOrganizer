"""Regenerate application icons from the square master logo.

Usage: python scripts/build_icons.py   (requires Pillow: pip install pillow)

Reads  assets/logo.png (1024x1024, transparent background)
Writes logo.ico                    Windows executable, installer and window icon
       assets/padorganizer.png     256 px, Linux icon and in-app brand mark
       assets/padorganizer-512.png 512 px, Linux HiDPI icon
"""
from pathlib import Path

from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parent.parent
ICO_SIZES = (16, 20, 24, 32, 40, 48, 64, 128, 256)


def scaled(master, size):
    image = master.resize((size, size), Image.LANCZOS)
    if size <= 48:
        # Small sizes lose edge contrast when the detailed artwork is shrunk.
        image = image.filter(ImageFilter.UnsharpMask(radius=0.6, percent=60, threshold=1))
    return image


def main():
    master = Image.open(ROOT / "assets" / "logo.png").convert("RGBA")
    if master.width != master.height:
        raise SystemExit("assets/logo.png must be square")

    scaled(master, 256).save(ROOT / "assets" / "padorganizer.png", optimize=True)
    scaled(master, 512).save(ROOT / "assets" / "padorganizer-512.png", optimize=True)
    scaled(master, ICO_SIZES[-1]).save(
        ROOT / "logo.ico",
        format="ICO",
        sizes=[(size, size) for size in ICO_SIZES],
        append_images=[scaled(master, size) for size in ICO_SIZES[:-1]],
    )
    print("Icons written: logo.ico, assets/padorganizer.png, assets/padorganizer-512.png")


if __name__ == "__main__":
    main()
