"""
============================================================
Prepare portrait for ASCII conversion

Author : Abinash Sharma
============================================================

Pipeline:

1. Load photo
2. Remove background
3. Crop transparent borders
4. Add 7% transparent padding
5. Resize & center on 800x800 canvas
6. Save source-prepped.png
============================================================
"""

from pathlib import Path

from PIL import Image
from rembg import remove


# ==========================================================
# Paths
# ==========================================================

PHOTO = Path("assets/photos/photo.jpg")
OUTPUT = Path("assets/photos/source-prepped.png")

CANVAS_SIZE = 800
PADDING_PERCENT = 0.07  # 7% padding


# ==========================================================
# Helpers
# ==========================================================

def crop_transparent(image: Image.Image) -> Image.Image:
    """Crop transparent borders."""

    bbox = image.getbbox()

    if bbox:
        return image.crop(bbox)

    return image


def add_padding_and_center(
    image: Image.Image,
    canvas_size: int = CANVAS_SIZE,
    padding_percent: float = PADDING_PERCENT,
) -> Image.Image:
    """
    Add transparent padding and center the portrait
    on a square transparent canvas.
    """

    # ---------- Add padding ----------
    pad = int(max(image.size) * padding_percent)

    padded = Image.new(
        "RGBA",
        (image.width + pad * 2, image.height + pad * 2),
        (0, 0, 0, 0),
    )

    padded.paste(image, (pad, pad), image)

    # ---------- Resize ----------
    scale = min(
        canvas_size / padded.width,
        canvas_size / padded.height,
    )

    new_width = int(padded.width * scale)
    new_height = int(padded.height * scale)

    resized = padded.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )

    # ---------- Create final canvas ----------
    canvas = Image.new(
        "RGBA",
        (canvas_size, canvas_size),
        (0, 0, 0, 0),
    )

    x = (canvas_size - new_width) // 2
    y = (canvas_size - new_height) // 2

    canvas.paste(resized, (x, y), resized)

    return canvas


# ==========================================================
# Main
# ==========================================================

def prepare_photo():

    print("=" * 60)
    print("Preparing portrait...")
    print("=" * 60)

    if not PHOTO.exists():
        raise FileNotFoundError(
            f"Photo not found:\n{PHOTO}"
        )

    print("Loading photo...")

    image = Image.open(PHOTO).convert("RGBA")

    print("Removing background...")

    output = remove(image)

    print("Cropping transparent borders...")

    output = crop_transparent(output)

    print("Adding padding and centering...")

    output = add_padding_and_center(output)

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.save(OUTPUT)

    print()
    print("Done!")
    print(f"Saved to:\n{OUTPUT}")


if __name__ == "__main__":
    prepare_photo()