import json

BADGES_JSON = "badges.json"
README_FILE = "README.md"

START = "<!-- CREDLY_BADGES_START -->"
END = "<!-- CREDLY_BADGES_END -->"

with open(BADGES_JSON, "r", encoding="utf-8") as f:
    badges = json.load(f)["data"]

cards = []

for badge in badges:
    name = badge.get("name", "")
    image = badge.get("image_url", "")
    url = (badge.get("badge_template", {}).get("url")
    or badge.get("url")
    or "https://www.credly.com/users/abinash-sharma.8f49b107")
    issuer = badge.get("issuer", {}).get("summary", "")
    year = badge.get("issued_at", "")[:4]

    card = f"""
    <a href="{url}" target="_blank" title="{issuer} ({year})"
       style="text-decoration:none;">
      <img src="{image}" width="90" alt="{name}" />
    </a>
    """
    cards.append(card.strip())

html_block = f"""
<div style="
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
">
  {' '.join(cards)}
</div>
"""

with open(README_FILE, "r", encoding="utf-8") as f:
    content = f.read()

if START not in content or END not in content:
    raise RuntimeError("Credly markers not found in README.md")

new_content = (
    content.split(START)[0]
    + START
    + "\n"
    + html_block
    + "\n"
    + END
    + content.split(END)[1]
)

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ README updated with horizontal Credly badges")
