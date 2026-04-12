from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

html_path = Path("Pasted text(9).txt")
html = html_path.read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")

def get_meta(name=None, prop=None):
    if name:
        tag = soup.find("meta", attrs={"name": name})
    else:
        tag = soup.find("meta", attrs={"property": prop})
    return tag.get("content", "").strip() if tag else ""

title = soup.title.get_text(" ", strip=True) if soup.title else ""
canonical = ""
canonical_tag = soup.find("link", attrs={"rel": "canonical"})
if canonical_tag:
    canonical = canonical_tag.get("href", "").strip()

download_pdf = ""
for a in soup.find_all("a", href=True):
    href = a["href"]
    if ".pdf" in href.lower():
        download_pdf = href.strip()
        break

text = soup.get_text("\n", strip=True)

def extract_label(label):
    pattern = rf"{re.escape(label)}\s*(.+)"
    m = re.search(pattern, text)
    return m.group(1).strip() if m else ""

report = {
    "title": title,
    "meta_description": get_meta(name="description"),
    "robots": get_meta(name="robots"),
    "og_title": get_meta(prop="og:title"),
    "og_description": get_meta(prop="og:description"),
    "og_url": get_meta(prop="og:url"),
    "canonical": canonical,
    "page_type": get_meta(name="page-type"),
    "full_name": extract_label("Full Name:"),
    "docket_number": extract_label("Docket Number:"),
    "date": extract_label("Date:"),
    "pdf_url": download_pdf,
}

print(json.dumps(report, indent=2))
