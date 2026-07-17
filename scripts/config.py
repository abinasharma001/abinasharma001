"""
============================================================
GitHub Profile Generator Configuration
Author : Abinash Sharma
Version : 1.0.0
============================================================

All scripts import settings from this file.

Example:

from config import Profile, Theme, ASCII, Paths
"""

from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

class Paths:
    ROOT = Path(__file__).resolve().parent.parent

    ASSETS = ROOT / "assets"

    PHOTOS = ASSETS / "photos"
    GENERATED = ASSETS / "generated"
    ICONS = ASSETS / "icons"
    FONTS = ASSETS / "fonts"

    PHOTO = PHOTOS / "photo.jpg"
    PREPPED_PHOTO = PHOTOS / "source-prepped.png"

    ASCII_SVG = GENERATED / "portrait.svg"
    INFO_CARD_SVG = GENERATED / "info-card.svg"
    BANNER_SVG = GENERATED / "banner.svg"

    README = ROOT / "README.md"


# ============================================================
# PROFILE
# ============================================================

class Profile:

    NAME = "Abinash Sharma"

    USERNAME = "abinasharma001"

    HOSTNAME = "github"

    ROLE = "Software Developer"

    CURRENT = "Software Developer"

    PREVIOUS = "XR Developer Intern @ NIT Rourkela"

    EDUCATION = "MCA (2025) | MSCB University"

    LOCATION = "India"

    WEBSITE = "https://abinash-sharma.pages.dev"

    GITHUB = "https://github.com/abinasharma001"

    LINKEDIN = "https://linkedin.com/in/contactabinashsharma"

    EMAIL = ""

    ABOUT = (
        "Software Developer passionate about AI, Cloud, "
        "AR/VR and Full Stack Development."
    )


# ============================================================
# TECH STACK
# ============================================================

class Stack:

    FRONTEND = [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Tailwind CSS"
    ]

    BACKEND = [
        "Python",
        "FastAPI",
        "Django",
        "Node.js"
    ]

    AI_ML = [
        "OpenAI",
        "LangChain",
        "RAG",
        "Gemini",
        "Watsonx"
    ]

    CLOUD = [
        "Azure",
        "Oracle Cloud",
        "Google Cloud",
        "AWS",
        "GitHub Actions"
    ]


# ============================================================
# HIGHLIGHTS
# ============================================================

class Highlights:

    ITEMS = [

        "Google IT Support Professional",

        "AR Campus Navigator Developer",

        "AI & Cloud Intern",

        "Open Source Contributor",

        "Content Creator",

        "MCA Graduate (2025)"

    ]


# ============================================================
# TERMINAL SETTINGS
# ============================================================

class Terminal:

    TITLE = "neofetch"

    PROMPT = "abinash@github:~$"

    WHOAMI = "whoami"

    WINDOW_TITLE = "GitHub Profile"

    FONT = (
        "ui-monospace, SFMono-Regular, Menlo, "
        "Consolas, monospace"
    )


# ============================================================
# ASCII SETTINGS
# ============================================================

class ASCII:

    COLS = 100

    ROWS = 55

    CELL_WIDTH = 8

    CELL_HEIGHT = 15

    FONT_SCALE = 0.86

    RAMP = " .`:-=+*cs#%@"

    CONTRAST = 1.05

    BRIGHTNESS = 1.0

    GAMMA = 1.18

    WHITE_FLOOR = 0.80

    SHARPEN = False


# ============================================================
# SVG LAYOUT
# ============================================================

class Layout:

    PADDING = 20

    BORDER_RADIUS = 12

    TITLEBAR_HEIGHT = 30

    STATUSBAR_HEIGHT = 30

    INFO_WIDTH = 600

    INFO_LINE_HEIGHT = 30

    FONT_SIZE = 16

    SMALL_FONT = 13


# ============================================================
# COLORS
# ============================================================

class Theme:

    BACKGROUND = "#0d1117"

    BACKGROUND_SECONDARY = "#111722"

    FRAME = "#30363d"

    TEXT = "#c9d1d9"

    MUTED = "#7d8590"

    GREEN = "#3fb950"

    BLUE = "#58a6ff"

    ORANGE = "#ffb86b"

    RED = "#ff5f56"

    YELLOW = "#ffbd2e"

    TERMINAL_GREEN = "#27c93f"

    TERMINAL_RED = "#ff5f56"

    TERMINAL_YELLOW = "#ffbd2e"


# ============================================================
# ANIMATION
# ============================================================

class Animation:

    ROW_DURATION = 0.11

    STAGGER = 0.11

    CURSOR_BLINK = 1.0

    FADE_DURATION = 0.4


# ============================================================
# BUILD
# ============================================================

class Build:

    VERSION = "1.0.0"

    AUTHOR = "Abinash Sharma"

    LICENSE = "MIT"

    GITHUB_REPOSITORY = "abinasharma001/abinasharma001"
