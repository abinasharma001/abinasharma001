"""
make_ascii_svg.py

Generate an animated SVG portrait from a preprocessed image.

Pipeline:

photo.jpg
    │
    ▼
prep_photo.py
    │
    ▼
source-prepped.png
    │
    ▼
ascii_engine.py
    │
    ▼
ASCII rows
    │
    ▼
svg_engine.py
    │
    ▼
portrait.svg
"""

from pathlib import Path

from ascii_engine import render_ascii, save_txt
from svg_engine import build_svg


IMAGE_PATH = Path("assets/photos/source-prepped.png")

ASCII_PREVIEW = Path("assets/photos/ascii_preview.txt")

OUTPUT_SVG = Path("assets/svg/portrait.svg")

TITLE = "abinash@github:~$ ./portrait.sh"


def main():

    if not IMAGE_PATH.exists():
        raise FileNotFoundError(
            f"Image not found:\n{IMAGE_PATH}"
        )

    print("Converting image to ASCII...")

    rows = render_ascii(str(IMAGE_PATH))

    save_txt(rows, ASCII_PREVIEW)

    print(f"ASCII preview saved -> {ASCII_PREVIEW}")

    build_svg(
        rows,
        output_path=str(OUTPUT_SVG),
        title=TITLE,
    )

    print(f"SVG written -> {OUTPUT_SVG}")

    print("Done.")


if __name__ == "__main__":
    main()