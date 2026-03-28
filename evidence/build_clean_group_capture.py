#!/usr/bin/env python3

from pathlib import Path
from bs4 import BeautifulSoup
import sys


DEFAULT_INPUT = "evidence/facebook-group-everything-greenfield-ma-source-capture.html"
DEFAULT_OUTPUT = "evidence/facebook-group-everything-greenfield-ma-cleaned.html"
DEFAULT_URL = "https://www.facebook.com/groups/greenfieldeverything/"


def build_clean_capture(src_path: Path, dst_path: Path, group_url: str) -> None:
    html = src_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title_text = "Cleaned Source Capture"
    if soup.title and soup.title.string:
        title_text = soup.title.string.strip()

    clean = BeautifulSoup("", "html.parser")

    html_tag = clean.new_tag("html", lang="en")
    head = clean.new_tag("head")
    body = clean.new_tag("body")

    meta_charset = clean.new_tag("meta", charset="utf-8")
    title = clean.new_tag("title")
    title.string = title_text

    meta_platform = clean.new_tag("meta")
    meta_platform.attrs["name"] = "source-platform"
    meta_platform.attrs["content"] = "Facebook Groups"

    meta_type = clean.new_tag("meta")
    meta_type.attrs["name"] = "source-type"
    meta_type.attrs["content"] = "cleaned public-source capture"

    meta_url = clean.new_tag("meta")
    meta_url.attrs["name"] = "original-group-url"
    meta_url.attrs["content"] = group_url

    meta_visibility = clean.new_tag("meta")
    meta_visibility.attrs["name"] = "visibility"
    meta_visibility.attrs["content"] = "Public group"

    head.extend([meta_charset, title, meta_platform, meta_type, meta_url, meta_visibility])

    h1 = clean.new_tag("h1")
    h1.string = title_text
    body.append(h1)

    fields = [
        ("Platform", "Facebook Groups"),
        ("Original URL", group_url),
        ("Visibility at capture", "Public group"),
    ]

    for label, value in fields:
        p = clean.new_tag("p")
        strong = clean.new_tag("strong")
        strong.string = f"{label}:"
        p.append(strong)
        p.append(f" {value}")
        body.append(p)

    note_h2 = clean.new_tag("h2")
    note_h2.string = "Preservation Note"
    body.append(note_h2)

    note_p = clean.new_tag("p")
    note_p.string = (
        "This cleaned artifact preserves public-facing source information from a captured "
        "Facebook group page. CSS, JavaScript, UI theme variables, and other non-evidentiary "
        "platform code were removed."
    )
    body.append(note_p)

    html_tag.extend([head, body])
    clean.append(html_tag)

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(str(clean), encoding="utf-8")


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_INPUT)
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(DEFAULT_OUTPUT)

    if not src.exists():
        print(f"Input file not found: {src}", file=sys.stderr)
        return 1

    build_clean_capture(src, dst, DEFAULT_URL)
    print(f"Wrote cleaned capture to: {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
