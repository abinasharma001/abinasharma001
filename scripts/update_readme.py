"""Update the Credly badges block in README.md from badges.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

README_PATH = Path("README.md")
BADGES_JSON_PATH = Path("badges.json")
START_MARKER = "<!-- CREDLY_BADGES_START -->"
END_MARKER = "<!-- CREDLY_BADGES_END -->"


def _as_text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _first_non_empty(*values: Any) -> str:
    for value in values:
        text = _as_text(value)
        if text:
            return text
    return ""


def _extract_year(badge: dict[str, Any]) -> str:
    for key in ("issued_at_date", "issued_at", "issued_on", "created_at"):
        value = _as_text(badge.get(key))
        if len(value) >= 4:
            return value[:4]
    return ""


def _extract_issuer(badge: dict[str, Any]) -> str:
    issuer = badge.get("issuer")
    if isinstance(issuer, dict):
        entities = issuer.get("entities")
        if isinstance(entities, list) and entities:
            entity = entities[0]
            if isinstance(entity, dict):
                nested_entity = entity.get("entity")
                if isinstance(nested_entity, dict):
                    name = _first_non_empty(nested_entity.get("name"), nested_entity.get("slug"))
                    if name:
                        return name
        return _first_non_empty(issuer.get("name"), issuer.get("slug"))
    return ""


def _extract_url(badge: dict[str, Any]) -> str:
    template = badge.get("badge_template") if isinstance(badge.get("badge_template"), dict) else {}
    return _first_non_empty(
        badge.get("url"),
        badge.get("public_url"),
        badge.get("badge_url"),
        template.get("url"),
    )


def _extract_image_url(badge: dict[str, Any]) -> str:
    image = badge.get("image") if isinstance(badge.get("image"), dict) else {}
    template = badge.get("badge_template") if isinstance(badge.get("badge_template"), dict) else {}
    template_image = template.get("image") if isinstance(template.get("image"), dict) else {}

    return _first_non_empty(
        badge.get("image_url"),
        image.get("url"),
        image.get("public_url"),
        template.get("image_url"),
        template_image.get("url"),
    )


def _extract_title(badge: dict[str, Any]) -> str:
    issuer = _extract_issuer(badge)
    year = _extract_year(badge)
    issued_by = f"issued by {issuer}" if issuer else "issued"
    if year:
        issued_by = f"{issued_by} ({year})"
    return issued_by


def _extract_badges(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
    raise ValueError("Unsupported badges.json structure")


def _build_badges_block(badges: list[dict[str, Any]]) -> str:
    lines = [
        '<div style="',
        '  display: flex;',
        '  flex-wrap: wrap;',
        '  gap: 16px;',
        '  align-items: center;',
        '">',
    ]

    for badge in badges:
        badge_url = _extract_url(badge)
        image_url = _extract_image_url(badge)
        if not badge_url or not image_url:
            continue

        title = _extract_title(badge)
        lines.extend(
            [
                f'  <a href="{badge_url}" target="_blank" title="{title}"',
                '     style="text-decoration:none;">',
                f'    <img src="{image_url}" width="90" alt="" />',
                '  </a>',
            ]
        )

    lines.append("</div>")
    return "\n".join(lines)


def main() -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    payload = json.loads(BADGES_JSON_PATH.read_text(encoding="utf-8"))
    badges = _extract_badges(payload)

    start = readme.find(START_MARKER)
    end = readme.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        raise ValueError("README markers for Credly badges were not found")

    generated_block = _build_badges_block(badges)

    replacement = (
        f"{START_MARKER}\n\n"
        f"{generated_block}\n\n"
        f"{END_MARKER}"
    )

    before = readme[:start]
    after = readme[end + len(END_MARKER) :]
    updated = before + replacement + after
    README_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
