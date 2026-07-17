"""
terminal_card.py

Generate a GitHub-style terminal information card.

Author: Abinash Sharma
"""
import html
from pathlib import Path

# ==========================================================
# Window
# ==========================================================

WIDTH = 920
HEIGHT = 670

PADDING = 26

TITLEBAR = 34

RADIUS = 12

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

FONT_SIZE = 14

LINE_HEIGHT = 30


# ==========================================================
# Colors
# ==========================================================

BACKGROUND = "#0d1117"

BORDER = "#30363d"

TITLE = "#8b949e"

TEXT = "#f0f6fc"

GREEN = "#3fb950"

BLUE = "#58a6ff"

ORANGE = "#ffa657"

GRAY = "#8b949e"

RED = "#ff5f56"

YELLOW = "#ffbd2e"

LIME = "#27c93f"


# ==========================================================
# Profile
# ==========================================================

PROFILE = {

    "username": "abinash@github",

    "command": "neofetch",

    "about": [

        ("Now", "Software Developer"),

        ("Previous", "XR Developer Intern"),

        ("Education", "MCA • 2025"),

        ("Location", "India"),

    ],

    "skills": [

        ("Languages", "Python, JavaScript, C"),

        ("Frontend", "HTML, CSS, React"),

        ("Backend", "FastAPI, Django"),

        ("Cloud", "Azure, AWS, GCP, Oracle"),

        ("AI / ML", "GenAI, RAG, Watsonx"),

    ],

    "highlights": [

        "Developer & Content Creator",

        "AI & Cloud Enthusiast",

        "XR Developer @ NIT Rourkela",

        "Open Source Contributor",

    ]
}
# ==========================================================
# SVG Builder
# ==========================================================

class SVG:

    def __init__(self):

        self.lines = []

    def add(self, text):

        self.lines.append(text)

    def extend(self, items):

        self.lines.extend(items)

    def save(self, output):

        output = Path(output)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            "\n".join(self.lines),
            encoding="utf-8",
        )
        # ==========================================================
# Terminal Window
# ==========================================================

def begin_svg(svg: SVG):

    svg.add(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{WIDTH}" '
        f'height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'font-family="{FONT}">'
    )


def end_svg(svg: SVG):

    svg.add("</svg>")


# ----------------------------------------------------------

def draw_defs(svg: SVG):

    svg.extend([

        "<defs>",

        '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">',

        '<stop offset="0%" stop-color="#111722"/>',

        '<stop offset="100%" stop-color="#0d1117"/>',

        "</linearGradient>",

        "</defs>",

    ])


# ----------------------------------------------------------

def draw_background(svg: SVG):

    svg.add(
        f'<rect '
        f'x="0" '
        f'y="0" '
        f'width="{WIDTH}" '
        f'height="{HEIGHT}" '
        f'rx="{RADIUS}" '
        f'fill="url(#bg)"/>'
    )

    svg.add(
        f'<rect '
        f'x="0.5" '
        f'y="0.5" '
        f'width="{WIDTH-1}" '
        f'height="{HEIGHT-1}" '
        f'rx="{RADIUS}" '
        f'fill="none" '
        f'stroke="{BORDER}" '
        f'stroke-width="1"/>'
    )


# ----------------------------------------------------------

def draw_titlebar(svg: SVG):

    # separator line
    svg.add(
        f'<line '
        f'x1="0" '
        f'y1="{TITLEBAR}" '
        f'x2="{WIDTH}" '
        f'y2="{TITLEBAR}" '
        f'stroke="{BORDER}"/>'
    )

    # macOS buttons
    buttons = [

        (RED, 22),

        (YELLOW, 42),

        (LIME, 62),

    ]

    for color, x in buttons:

        svg.add(
            f'<circle '
            f'cx="{x}" '
            f'cy="{TITLEBAR/2}" '
            f'r="6" '
            f'fill="{color}"/>'
        )

    # terminal title
    title = (
        f'{PROFILE["username"]}: ~$ '
        f'{PROFILE["command"]}'
    )

    svg.add(
        f'<text '
        f'x="{WIDTH/2}" '
        f'y="{TITLEBAR/2+5}" '
        f'font-size="13" '
        f'fill="{TITLE}" '
        f'text-anchor="middle">'
        f'{title}'
        f'</text>'
    )

    # ==========================================================
# Header
# ==========================================================

START_X = 28
VALUE_X = 180

HEADER_Y = 82


def draw_header(svg: SVG):

    svg.add(
        f'<text '
        f'x="{START_X}" '
        f'y="{HEADER_Y}" '
        f'font-size="18" '
        f'font-weight="600">'
    )

    svg.add(f'<tspan fill="{GREEN}">abinash</tspan>')
    svg.add(f'<tspan fill="{TEXT}">@</tspan>')
    svg.add(f'<tspan fill="{BLUE}">github</tspan>')

    svg.add("</text>")

    # divider

    svg.add(
        f'<line '
        f'x="160" '
        f'y1="{HEADER_Y-7}" '
        f'x2="{WIDTH-30}" '
        f'y2="{HEADER_Y-7}" '
        f'stroke="{BORDER}" '
        f'stroke-width="1"/>'
    )

SECTION_START_Y = 120

ROW_HEIGHT = 32

LABEL_X = 28

VALUE_X = 165

STACK_TITLE_Y = 280
STACK_START_Y = 320
HIGHLIGHTS_TITLE_Y = 500
HIGHLIGHTS_START_Y = 535

BULLET_X = 36
TEXT_X = 54
# ==========================================================
# About Section
# ==========================================================

def draw_about(svg: SVG):

    y = SECTION_START_Y

    for label, value in PROFILE["about"]:

        svg.add(
            f'<text '
            f'x="{LABEL_X}" '
            f'y="{y}" '
            f'font-size="{FONT_SIZE}" '
            f'fill="{ORANGE}" '
            f'font-weight="600">'
            f'{label}'
            f'</text>'
        )

        svg.add(
            f'<text '
            f'x="{VALUE_X}" '
            f'y="{y}" '
            f'font-size="{FONT_SIZE}" '
            f'fill="{TEXT}">'
            f'{value}'
            f'</text>'
        )

        y += ROW_HEIGHT

        # ==========================================================
# Stack Section
# ==========================================================

def draw_stack(svg: SVG):

    # Section title
    svg.add(
        f'<text '
        f'x="{LABEL_X}" '
        f'y="{STACK_TITLE_Y}" '
        f'font-size="18" '
        f'font-weight="600" '
        f'fill="{BLUE}">'
        f'− Stack'
        f'</text>'
    )

    # Divider line
    svg.add(
        f'<line '
        f'x="145" '
        f'y1="{STACK_TITLE_Y-7}" '
        f'x2="{WIDTH-30}" '
        f'y2="{STACK_TITLE_Y-7}" '
        f'stroke="{BORDER}" '
        f'stroke-width="1"/>'
    )

    y = STACK_START_Y

    for label, value in PROFILE["skills"]:

        # Left label
        svg.add(
            f'<text '
            f'x="{LABEL_X}" '
            f'y="{y}" '
            f'font-size="{FONT_SIZE}" '
            f'fill="{ORANGE}" '
            f'font-weight="600">'
            f'{label}'
            f'</text>'
        )

        # Right value
        svg.add(
            f'<text '
            f'x="{VALUE_X}" '
            f'y="{y}" '
            f'font-size="{FONT_SIZE}" '
            f'fill="{TEXT}">'
            f'{value}'
            f'</text>'
        )

        y += ROW_HEIGHT

        # ==========================================================
# ==========================================================
# Highlights
# ==========================================================

def draw_highlights(svg: SVG):

    # Section Title
    svg.add(
        f'<text '
        f'x="{LABEL_X}" '
        f'y="{HIGHLIGHTS_TITLE_Y}" '
        f'font-size="18" '
        f'font-weight="600" '
        f'fill="{BLUE}">'
        f'− Highlights'
        f'</text>'
    )

    # Divider Line
    svg.add(
        f'<line '
        f'x="185" '
        f'y1="{HIGHLIGHTS_TITLE_Y - 7}" '
        f'x2="{WIDTH - 30}" '
        f'y2="{HIGHLIGHTS_TITLE_Y - 7}" '
        f'stroke="{BORDER}" '
        f'stroke-width="1"/>'
    )

    y = HIGHLIGHTS_START_Y

    for item in PROFILE["highlights"]:

        # Green Bullet
        svg.add(
            f'<circle '
            f'cx="{BULLET_X}" '
            f'cy="{y - 5}" '
            f'r="4" '
            f'fill="{GREEN}"/>'
        )

        # Highlight Text
        svg.add(
            f'<text '
            f'x="{TEXT_X}" '
            f'y="{y}" '
            f'font-size="{FONT_SIZE}" '
            f'fill="{TEXT}">'
            f'{html.escape(str(item))}'
            f'</text>'
        )

        y += ROW_HEIGHT
    # ==========================================================
# Test
# ==========================================================

svg = SVG()

begin_svg(svg)

draw_defs(svg)

draw_background(svg)

draw_titlebar(svg)

draw_header(svg)

draw_about(svg)

draw_stack(svg)

draw_highlights(svg)

end_svg(svg)

svg.save("assets/svg/info-card.svg")

print("Created assets/svg/info-card.svg")