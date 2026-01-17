import json
from datetime import datetime

BADGES_JSON = "badges.json"
README_FILE = "README.md"

START = "<!-- CREDLY_BADGES_START -->"
END = "<!-- CREDLY_BADGES_END -->"

with open(BADGES_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)["data"]

rows = []
for badge in data:
    name = badge.get("name", "—")
    issuer = badge.get("issuer", {}).get("summary", "—")
    issued_at = badge.get("issued_at", "")
    year = issued_at[:4] if issued_at else "—"
    image = badge.get("image_url", "")
    url = badge.get("url", "#")

    rows.append(
        f"| <img src='{image}' width='80'/> | [{name}]({url}) | {issuer} | {year} |"
    )

table = (
    "| Badge | Name | Issuer | Year |\n"
    "|------|------|--------|------|\n"
    + "\n".join(rows)
)

with open(README_FILE, "r", encoding="utf-8") as f:
    content = f.read()

if START not in content or END not in content:
    raise RuntimeError("Credly markers not found in README.md")

new_content = (
    content.split(START)[0]
    + START
    + "\n"
    + table
    + "\n"
    + END
    + content.split(END)[1]
)

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ README.md updated with Credly badges")
