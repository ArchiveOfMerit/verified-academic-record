from bs4 import BeautifulSoup
from pathlib import Path
import re

INPUT_FILE = Path("/mnt/data/Pasted text(10).txt")
OUTPUT_FILE = Path("/mnt/data/justia_22-ST-00949_local_redaction_2026-04-12_v1.html")

html = INPUT_FILE.read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

# 1) Replace page title
if soup.title:
    soup.title.string = "Redacted Local Record"

# 2) Rewrite robots meta for local copy only
robots = soup.find("meta", attrs={"name": "robots"})
if robots:
    robots["content"] = "noindex, nofollow"

# 3) Remove canonical and direct page identity metadata
for selector in [
    ("link", {"rel": "canonical"}),
    ("meta", {"property": "og:url"}),
    ("meta", {"property": "og:title"}),
    ("meta", {"property": "og:description"}),
    ("meta", {"name": "description"}),
]:
    tag = soup.find(selector[0], attrs=selector[1])
    if tag:
        tag.decompose()

# 4) Remove metadata card, PDF button, iframe, noframes opinion text
for tag in soup.select(".metadata-card, iframe.pdf-iframe, .disclaimer"):
    tag.decompose()

for a in soup.find_all("a", href=True):
    href = a.get("href", "")
    if ".pdf" in href.lower():
        a.decompose()

for nf in soup.find_all("noframes"):
    nf.decompose()

# 5) Remove Justia navigation/sidebar/footer blocks from local copy
for tag in soup.select(
    "header, #primary-sidebar, #footer, .notification-banner, "
    "#newsletter-subscription-aside-widget, #ask-a-lawyer-widget, aside"
):
    tag.decompose()

# 6) Remove external scripts, analytics, recaptcha
for script in soup.find_all("script"):
    src = script.get("src", "")
    text = script.get_text(" ", strip=True)
    if src or "googletagmanager" in text.lower() or "recaptcha" in text.lower():
        script.decompose()

# 7) Optionally remove external stylesheet links for a self-contained plain copy
for link in soup.find_all("link", href=True):
    href = link["href"]
    if href.startswith("http") or href.startswith("//"):
        link.decompose()

# 8) Replace sensitive visible text in text nodes
replacements = {
    r"\bGamache v\.? Ronan\b": "[REDACTED CASE NAME]",
    r"\bJustin-Ames Gamache\b": "[REDACTED NAME]",
    r"\bJustin A Gamache\b": "[REDACTED NAME]",
    r"\bJustin Gamache\b": "[REDACTED NAME]",
    r"\bLauren Ronan\b": "[REDACTED NAME]",
    r"\b22-ST-00949\b": "[REDACTED DOCKET]",
    r"\bApril 8, 2026\b": "[REDACTED DATE]",
    r"\bMarch 11, 2026\b": "[REDACTED DATE]",
}

for text_node in soup.find_all(string=True):
    original = str(text_node)
    updated = original
    for pattern, repl in replacements.items():
        updated = re.sub(pattern, repl, updated, flags=re.IGNORECASE)
    if updated != original:
        text_node.replace_with(updated)

# 9) Replace main heading if still present
h1 = soup.find("h1")
if h1:
    h1.string = "Redacted Local Record"

# 10) Add a clear local-use banner
body = soup.body
if body:
    banner = soup.new_tag("div")
    banner["style"] = (
        "padding:16px;margin:16px;border:2px solid #000;"
        "font-family:Arial,sans-serif;background:#f5f5f5;"
    )
    banner.string = "This is a locally redacted copy for private review only."
    body.insert(0, banner)

OUTPUT_FILE.write_text(str(soup), encoding="utf-8")
print(f"Saved: {OUTPUT_FILE}")
