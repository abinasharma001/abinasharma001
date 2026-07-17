"""
ascii_engine.py

High-quality ASCII rendering engine.

Responsibilities:
- Load transparent PNG
- Preserve alpha channel
- Enhance image
- Resize with character aspect ratio
- Prepare for ASCII conversion

Author: Abinash Sharma
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from PIL import (
    Image,
    ImageOps,
    ImageEnhance,
    ImageFilter,
)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

ASCII_RAMP = (
    " .'`^\",:;Il!i~+_-?][}{1)(|\\/"
    "tfjrxnuvczXYUJCLQ0OZmwqpdbkhao"
    "*#MW&8%B@$"
)

DEFAULT_COLS = 110

CONTRAST = 1.30
BRIGHTNESS = 1.02
GAMMA = 0.95

WHITE_THRESHOLD = 0.93
ALPHA_THRESHOLD = 20

CHARACTER_ASPECT = 0.55


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def load_image(path: str | Path) -> Image.Image:
    """
    Load an image as RGBA.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    return Image.open(path).convert("RGBA")


def preprocess(image: Image.Image) -> tuple[Image.Image, Image.Image]:
    """
    Enhance the image before ASCII conversion.

    Returns:
        grayscale_image,
        alpha_channel
    """

    alpha = image.getchannel("A")

    background = Image.new(
        "RGBA",
        image.size,
        (255, 255, 255, 255),
    )

    background.alpha_composite(image)

    gray = background.convert("L")

    gray = ImageOps.autocontrast(gray)

    gray = ImageEnhance.Contrast(gray).enhance(
        CONTRAST
    )

    gray = ImageEnhance.Brightness(gray).enhance(
        BRIGHTNESS
    )

    gray = gray.filter(
        ImageFilter.SHARPEN
    )

    return gray, alpha


def resize_images(
    gray: Image.Image,
    alpha: Image.Image,
    cols: int,
) -> tuple[Image.Image, Image.Image]:
    """
    Resize grayscale and alpha channel together.
    """

    rows = int(
        gray.height
        / gray.width
        * cols
        * CHARACTER_ASPECT
    )

    gray = gray.resize(
        (cols, rows),
        Image.Resampling.LANCZOS,
    )

    alpha = alpha.resize(
        (cols, rows),
        Image.Resampling.LANCZOS,
    )

    return gray, alpha
# --------------------------------------------------
# ASCII Conversion
# --------------------------------------------------

def pixel_to_ascii(
    luminance: int,
    alpha: int,
) -> str:
    """
    Convert a single pixel to an ASCII character.
    """

    if alpha < ALPHA_THRESHOLD:
        return " "

    lum = luminance / 255.0

    lum = pow(lum, GAMMA)

    if lum >= WHITE_THRESHOLD:
        return " "

    index = int(
        (1.0 - lum)
        * (len(ASCII_RAMP) - 1)
    )

    index = max(
        0,
        min(index, len(ASCII_RAMP) - 1),
    )

    return ASCII_RAMP[index]


# --------------------------------------------------
# Main Renderer
# --------------------------------------------------

def render_ascii(
    image_path: str | Path,
    cols: int = DEFAULT_COLS,
) -> List[str]:
    """
    Convert an image into ASCII rows.

    Returns
    -------
    list[str]
        ASCII art lines.
    """

    image = load_image(image_path)

    gray, alpha = preprocess(image)

    gray, alpha = resize_images(
        gray,
        alpha,
        cols,
    )

    gray_pixels = gray.load()
    alpha_pixels = alpha.load()

    width, height = gray.size

    rows: List[str] = []

    for y in range(height):

        line = []

        for x in range(width):

            line.append(
                pixel_to_ascii(
                    gray_pixels[x, y],
                    alpha_pixels[x, y],
                )
            )

        rows.append("".join(line))

    return rows


# --------------------------------------------------
# Optional Helper
# --------------------------------------------------

def save_txt(
    rows: List[str],
    output: str | Path,
) -> None:
    """
    Save ASCII rows to a text file.
    """

    output = Path(output)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        "\n".join(rows),
        encoding="utf-8",
    )


# --------------------------------------------------
# Standalone Test
# --------------------------------------------------

if __name__ == "__main__":

    import sys

    image = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "assets/photos/source-prepped.png"
    )

    rows = render_ascii(image)

    for line in rows:
        print(line)

    save_txt(
        rows,
        "assets/photos/ascii_preview.txt",
    )

    print()
    print("=" * 60)
    print("ASCII conversion complete.")
    print("=" * 60)
    print("Preview:")
    print("  assets/photos/ascii_preview.txt")
    print("=" * 60)