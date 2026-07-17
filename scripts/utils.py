"""
=========================================================
Utility functions for GitHub Profile Generator
Author : Abinash Sharma
=========================================================
"""

from pathlib import Path
import html

from config import Theme


# ==========================================================
# SVG
# ==========================================================

SVG_NS = "http://www.w3.org/2000/svg"


def svg_header(width: int, height: int) -> str:
    """Create SVG opening tag."""

    return (
        f'<svg xmlns="{SVG_NS}" '
        f'width="{width}" '
        f'height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )


def svg_footer() -> str:
    """Close SVG."""

    return "</svg>"


# ==========================================================
# ESCAPE
# ==========================================================

def escape(text: str) -> str:
    """Escape XML characters."""

    return html.escape(text)


# ==========================================================
# COLORS
# ==========================================================

def gradient():
    """GitHub dark gradient."""

    return f"""
<defs>

<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">

<stop offset="0%" stop-color="{Theme.BACKGROUND_SECONDARY}"/>

<stop offset="100%" stop-color="{Theme.BACKGROUND}"/>

</linearGradient>

</defs>
"""


# ==========================================================
# WINDOW
# ==========================================================

def terminal_window(width, height, radius=12):

    return f"""
<rect
width="{width}"
height="{height}"
rx="{radius}"
fill="url(#bg)"/>

<rect
x="0.5"
y="0.5"
width="{width-1}"
height="{height-1}"
rx="{radius}"
fill="none"
stroke="{Theme.FRAME}"
stroke-width="1"/>
"""


def title_bar(width, height=30):

    return f"""
<line
x1="0"
y1="{height}"
x2="{width}"
y2="{height}"
stroke="{Theme.FRAME}"/>
"""


# ==========================================================
# TERMINAL BUTTONS
# ==========================================================

def terminal_buttons(x=20, y=15):

    colors = [

        Theme.TERMINAL_RED,

        Theme.TERMINAL_YELLOW,

        Theme.TERMINAL_GREEN

    ]

    svg = ""

    for i, color in enumerate(colors):

        svg += (

            f'<circle '
            f'cx="{x + i * 16}" '
            f'cy="{y}" '
            f'r="5" '
            f'fill="{color}"/>'

        )

    return svg


# ==========================================================
# TEXT
# ==========================================================

def text(
        x,
        y,
        value,
        color,
        size,
        anchor="start",
        weight="normal",
):

    value = escape(value)

    return (
        f'<text '
        f'x="{x}" '
        f'y="{y}" '
        f'fill="{color}" '
        f'font-size="{size}" '
        f'font-weight="{weight}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'text-anchor="{anchor}">'
        f'{value}'
        f'</text>'
    )


# ==========================================================
# LINE
# ==========================================================

def line(x1, y1, x2, y2, color):

    return (
        f'<line '
        f'x1="{x1}" '
        f'y1="{y1}" '
        f'x2="{x2}" '
        f'y2="{y2}" '
        f'stroke="{color}"/>'
    )


# ==========================================================
# SAVE
# ==========================================================

def save_svg(path: Path, svg: str):

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"✓ Saved {path}")
