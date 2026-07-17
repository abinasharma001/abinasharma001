"""
svg_engine.py

Render animated terminal-style SVGs from ASCII text.

Author: Abinash Sharma
"""

from __future__ import annotations

from pathlib import Path
from typing import List
import html

# ==========================================================
# Theme
# ==========================================================

PAD = 20

TITLEBAR_HEIGHT = 32
STATUSBAR_HEIGHT = 30

CELL_WIDTH = 8
CELL_HEIGHT = 15

FONT_SIZE = 13

WINDOW_RADIUS = 12

BACKGROUND_TOP = "#111722"
BACKGROUND_BOTTOM = "#0d1117"

FRAME_COLOR = "#30363d"

TEXT_COLOR = "#c9d1d9"

TITLE_COLOR = "#7d8590"

CURSOR_COLOR = "#58a6ff"

BUTTON_RED = "#ff5f56"
BUTTON_YELLOW = "#ffbd2e"
BUTTON_GREEN = "#27c93f"

ROW_DELAY = 0.08
CURSOR_BLINK = 0.9


# ==========================================================
# Layout
# ==========================================================

class Layout:
    """
    Computes every coordinate used in the SVG.
    """

    def __init__(self, rows: List[str]):

        self.rows = rows

        self.columns = max(len(r) for r in rows)

        self.width = (
            self.columns * CELL_WIDTH
            + PAD * 2
        )

        self.height = (
            TITLEBAR_HEIGHT
            + STATUSBAR_HEIGHT
            + PAD
            + len(rows) * CELL_HEIGHT
            + PAD
        )

    @property
    def ascii_x(self):

        return PAD

    @property
    def ascii_y(self):

        return TITLEBAR_HEIGHT + PAD

    @property
    def status_y(self):

        return self.height - STATUSBAR_HEIGHT / 2


# ==========================================================
# SVG Document Builder
# ==========================================================

class SVGDocument:

    def __init__(self):

        self.parts: List[str] = []

    def add(self, line: str):

        self.parts.append(line)

    def extend(self, lines):

        self.parts.extend(lines)

    def text(self):

        return "\n".join(self.parts)

    def save(self, output_path):

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            self.text(),
            encoding="utf-8",
        )
        # ==========================================================
# SVG Drawing
# ==========================================================

def begin_svg(doc: SVGDocument, layout: Layout):
    """Start the SVG document."""

    doc.add(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{layout.width}" '
        f'height="{layout.height}" '
        f'viewBox="0 0 {layout.width} {layout.height}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">'
    )


def end_svg(doc: SVGDocument):
    """Close the SVG document."""

    doc.add("</svg>")


# ----------------------------------------------------------

def draw_defs(doc: SVGDocument):
    """SVG definitions."""

    doc.extend([
        "<defs>",

        '<linearGradient id="terminal-bg" '
        'x1="0" y1="0" x2="0" y2="1">',

        f'<stop offset="0%" stop-color="{BACKGROUND_TOP}"/>',

        f'<stop offset="100%" stop-color="{BACKGROUND_BOTTOM}"/>',

        "</linearGradient>",

        "</defs>",
    ])


# ----------------------------------------------------------

def draw_background(
    doc: SVGDocument,
    layout: Layout,
):
    """Rounded terminal background."""

    doc.add(
        f'<rect '
        f'x="0" '
        f'y="0" '
        f'width="{layout.width}" '
        f'height="{layout.height}" '
        f'rx="{WINDOW_RADIUS}" '
        f'fill="url(#terminal-bg)"/>'
    )

    doc.add(
        f'<rect '
        f'x="0.5" '
        f'y="0.5" '
        f'width="{layout.width-1}" '
        f'height="{layout.height-1}" '
        f'rx="{WINDOW_RADIUS}" '
        f'fill="none" '
        f'stroke="{FRAME_COLOR}" '
        f'stroke-width="1"/>'
    )


# ----------------------------------------------------------

def draw_titlebar(
    doc: SVGDocument,
    layout: Layout,
    title: str,
):
    """Draw macOS title bar."""

    doc.add(
        f'<line '
        f'x1="0" '
        f'y1="{TITLEBAR_HEIGHT}" '
        f'x2="{layout.width}" '
        f'y2="{TITLEBAR_HEIGHT}" '
        f'stroke="{FRAME_COLOR}"/>'
    )

    colors = (
        BUTTON_RED,
        BUTTON_YELLOW,
        BUTTON_GREEN,
    )

    for index, color in enumerate(colors):

        doc.add(
            f'<circle '
            f'cx="{20 + index*16}" '
            f'cy="{TITLEBAR_HEIGHT/2}" '
            f'r="5" '
            f'fill="{color}"/>'
        )

    doc.add(
        f'<text '
        f'x="{layout.width/2}" '
        f'y="{TITLEBAR_HEIGHT/2 + 4}" '
        f'fill="{TITLE_COLOR}" '
        f'font-size="12" '
        f'text-anchor="middle">'
        f'{html.escape(title)}'
        f'</text>'
    )


# ----------------------------------------------------------

def draw_separator(
    doc: SVGDocument,
    layout: Layout,
):
    """Separate ASCII area from status bar."""

    y = layout.height - STATUSBAR_HEIGHT

    doc.add(
        f'<line '
        f'x1="0" '
        f'y1="{y}" '
        f'x2="{layout.width}" '
        f'y2="{y}" '
        f'stroke="{FRAME_COLOR}"/>'
    )
    # ==========================================================
# ASCII Rendering
# ==========================================================

def escape_svg(text: str) -> str:
    """
    Escape characters that are invalid inside XML text nodes.
    """
    return (
        html.escape(text)
        .replace(" ", "&#160;")  # preserve spaces
    )


# ----------------------------------------------------------

def draw_ascii(
    doc: SVGDocument,
    layout: Layout,
    rows: List[str],
):
    """
    Draw ASCII portrait.
    """

    start_x = layout.ascii_x
    start_y = layout.ascii_y

    doc.add(
        f'<g id="ascii" '
        f'fill="{TEXT_COLOR}" '
        f'font-size="{FONT_SIZE}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">'
    )

    for row_index, row in enumerate(rows):

        y = start_y + row_index * CELL_HEIGHT

        doc.add(
            f'<text '
            f'x="{start_x}" '
            f'y="{y}" '
            f'xml:space="preserve">'
            f'{escape_svg(row)}'
            f'</text>'
        )

    doc.add("</g>")


# ----------------------------------------------------------

def longest_row(rows: List[str]) -> int:
    """
    Return length of the longest ASCII row.
    """

    if not rows:
        return 0

    return max(len(r) for r in rows)


# ----------------------------------------------------------

def ascii_width(rows: List[str]) -> int:
    """
    Width of ASCII block in pixels.
    """

    return longest_row(rows) * CELL_WIDTH


# ----------------------------------------------------------

def ascii_height(rows: List[str]) -> int:
    """
    Height of ASCII block in pixels.
    """

    return len(rows) * CELL_HEIGHT


# ----------------------------------------------------------

def ascii_bounds(layout: Layout, rows: List[str]):
    """
    Return (x, y, width, height) of the ASCII region.
    """

    return (
        layout.ascii_x,
        layout.ascii_y - FONT_SIZE,
        ascii_width(rows),
        ascii_height(rows),
    )
# ==========================================================
# Animation
# ==========================================================

TYPE_SPEED = 3.5      # seconds
CURSOR_WIDTH = 8


def draw_typing_animation(
    doc: SVGDocument,
    layout: Layout,
    rows: List[str],
):
    """
    Reveal the ASCII portrait from left to right using a clipPath.
    """

    x, y, w, h = ascii_bounds(layout, rows)

    doc.extend([
        "<defs>",

        '<clipPath id="typingClip">',

        f'<rect id="typingRect" '
        f'x="{x}" '
        f'y="{y}" '
        f'width="0" '
        f'height="{h + FONT_SIZE}">',

        f'<animate '
        f'attributeName="width" '
        f'from="0" '
        f'to="{w + 20}" '
        f'dur="{TYPE_SPEED}s" '
        f'fill="freeze"/>',

        "</rect>",

        "</clipPath>",

        "</defs>",
    ])


# ----------------------------------------------------------

def begin_ascii_group(doc: SVGDocument):
    """
    Start clipped ASCII group.
    """

    doc.add('<g clip-path="url(#typingClip)">')


def end_ascii_group(doc: SVGDocument):
    """
    Close clipped ASCII group.
    """

    doc.add("</g>")


# ----------------------------------------------------------

def draw_cursor(
    doc: SVGDocument,
    layout: Layout,
    rows: List[str],
):
    """
    Draw animated typing cursor.
    """

    x, y, w, h = ascii_bounds(layout, rows)

    cursor_height = h + FONT_SIZE

    doc.add(
        f'<rect '
        f'x="{x}" '
        f'y="{y}" '
        f'width="{CURSOR_WIDTH}" '
        f'height="{cursor_height}" '
        f'fill="{CURSOR_COLOR}">'
    )

    doc.add(
        f'<animate '
        f'attributeName="x" '
        f'from="{x}" '
        f'to="{x + w}" '
        f'dur="{TYPE_SPEED}s" '
        f'fill="freeze"/>'
    )

    doc.add(
        f'<animate '
        f'attributeName="opacity" '
        f'values="1;0;1;0;1" '
        f'dur="{CURSOR_BLINK}s" '
        f'repeatCount="indefinite"/>'
    )

    doc.add("</rect>")
    # ==========================================================
# Status Bar
# ==========================================================

def draw_statusbar(
    doc: SVGDocument,
    layout: Layout,
):
    """
    Draw the bottom terminal prompt.
    """

    y = layout.status_y

    prompt = "abinash@github:~$"
    command = " whoami"
    output = " Abinash Sharma"

    doc.add(
        f'<text '
        f'x="{PAD}" '
        f'y="{y}" '
        f'font-size="12" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">'
    )

    doc.add(
        f'<tspan fill="#58a6ff">{html.escape(prompt)}</tspan>'
    )

    doc.add(
        f'<tspan fill="#c9d1d9">{html.escape(command)}</tspan>'
    )

    doc.add(
        f'<tspan fill="#7ee787">{html.escape(output)}</tspan>'
    )

    doc.add("</text>")


# ==========================================================
# Public API
# ==========================================================

def build_svg(
    rows: List[str],
    output_path: str = "assets/svg/portrait.svg",
    title: str = "abinash@github:~$ ./portrait.sh",
):
    """
    Build the complete animated terminal SVG.
    """

    layout = Layout(rows)

    doc = SVGDocument()

    begin_svg(doc, layout)

    draw_defs(doc)

    draw_background(doc, layout)

    draw_titlebar(doc, layout, title)

    draw_typing_animation(doc, layout, rows)

    begin_ascii_group(doc)

    draw_ascii(doc, layout, rows)

    end_ascii_group(doc)

    draw_cursor(doc, layout, rows)

    draw_separator(doc, layout)

    draw_statusbar(doc, layout)

    end_svg(doc)

    doc.save(output_path)

    return output_path


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    sample = [
        "      .-''''-.",
        "    .'  .-.  '.",
        "   /   (o o)   \\",
        "  |     \\_/     |",
        "   \\           /",
        "    '.       .'",
        "      '-...-'",
    ]

    output = build_svg(sample)

    print(f"SVG written to: {output}")