ffrom __future__ import annotations

import json
import smtplib
from dataclasses import dataclass, asdict
from email.message import EmailMessage
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup


# =========================
# USER CONFIGURATION
# =========================

INPUT_HTML = Path("/mnt/data/Pasted text(11).txt")
OUTPUT_DIR = Path("/mnt/data/justia_block_request")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Preferred human destination:
# Justia Support page has a category for blocking a Justia link from search engines.
# Because Justia does not publicly expose a dedicated API endpoint for that request path,
# this script generates a ready-to-send message and can optionally send via YOUR email account.
JUSTIA_SUPPORT_URL = "https://support.justia.com/"

# If you know the correct recipient email, put it here.
# Otherwise leave as None and use the generated text through the support form manually.
JUSTIA_EMAIL: Optional[str] = None

# Optional SMTP sending configuration.
SMTP_HOST: Optional[str] = None      # e.g. "smtp.gmail.com"
SMTP_PORT: int = 587
SMTP_USERNAME: Optional[str] = None
SMTP_PASSWORD: Optional[str] = None
SMTP_USE_TLS: bool = True

SENDER_NAME = "Justin-Ames Gamache"
SENDER_EMAIL = "your_email@example.com"

REQUEST_SUBJECT = "Request to Block Justia Link from Search Engines"
REQUEST_TYPE = "block_from_search_engines"


# =========================
# DATA MODEL
# =========================

@dataclass
class PageEvidence:
    title: str
    meta_description: str
    robots: str
    canonical: str
    og_url: str
    docket_number: str
    case_date: str
    pdf_url: str

@dataclass
class BlockingRequest:
    requester_name: str
    requester_email: str
    request_type: str
    target_url: str
    reason_summary: str
    requested_action: list[str]
    supporting_facts: dict
    source_file: str


# =========================
# EXTRACTION
# =========================

def read_html(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def find_meta(soup: BeautifulSoup, *, name: str | None = None, prop: str | None = None) -> str:
    if name is not None:
        tag = soup.find("meta", attrs={"name": name})
    else:
        tag = soup.find("meta", attrs={"property": prop})
    return tag.get("content", "").strip() if tag else ""


def extract_text_after_label(soup: BeautifulSoup, label: str) -> str:
    text = soup.get_text("\n", strip=True)
    label_lower = label.lower()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for i, line in enumerate(lines):
        if label_lower in line.lower():
            # handle "Label: value" on same line
            parts = line.split(":", 1)
            if len(parts) == 2 and parts[1].strip():
                return parts[1].strip()
            # handle value on next line
            if i + 1 < len(lines):
                return lines[i + 1].strip()
    return ""


def extract_pdf_url(soup: BeautifulSoup) -> str:
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if ".pdf" in href.lower():
            if href.startswith("//"):
                return "https:" + href
            return href
    return ""


def extract_evidence(path: Path) -> PageEvidence:
    html = read_html(path)
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})
    canonical = canonical_tag.get("href", "").strip() if canonical_tag else ""

    return PageEvidence(
        title=title,
        meta_description=find_meta(soup, name="description"),
        robots=find_meta(soup, name="robots"),
        canonical=canonical,
        og_url=find_meta(soup, prop="og:url"),
        docket_number=extract_text_after_label(soup, "Docket Number"),
        case_date=extract_text_after_label(soup, "Date"),
        pdf_url=extract_pdf_url(soup),
    )


# =========================
# REQUEST GENERATION
# =========================

def build_request(evidence: PageEvidence) -> BlockingRequest:
    target_url = evidence.canonical or evidence.og_url

    return BlockingRequest(
        requester_name=SENDER_NAME,
        requester_email=SENDER_EMAIL,
        request_type=REQUEST_TYPE,
        target_url=target_url,
        reason_summary=(
            "I request that this Justia page be blocked from search engine indexing and "
            "search-result visibility due to ongoing privacy and reputational harm."
        ),
        requested_action=[
            "block the page from search engines",
            "remove or suppress search-result snippets where feasible",
            "review mirror PDF visibility",
            "confirm the request path and any additional documentation needed",
        ],
        supporting_facts={
            "page_title": evidence.title,
            "robots_meta": evidence.robots,
            "canonical_url": evidence.canonical,
            "open_graph_url": evidence.og_url,
            "docket_number": evidence.docket_number,
            "case_date": evidence.case_date,
            "pdf_url": evidence.pdf_url,
        },
        source_file=str(INPUT_HTML),
    )


def build_message_text(req: BlockingRequest) -> str:
    lines = [
        f"Subject: {REQUEST_SUBJECT}",
        "",
        "To Justia Support,",
        "",
        "I am submitting a request to block a Justia link from search engines.",
        "",
        f"Target URL: {req.target_url}",
        f"Requester: {req.requester_name}",
        f"Contact Email: {req.requester_email}",
        "",
        "Requested Action:",
    ]
    lines.extend([f"- {item}" for item in req.requested_action])
    lines.extend([
        "",
        "Reason Summary:",
        req.reason_summary,
        "",
        "Supporting Facts:",
    ])
    for key, value in req.supporting_facts.items():
        lines.append(f"- {key}: {value}")
    lines.extend([
        "",
        "Please confirm receipt and advise whether any additional documentation is required.",
        "",
        "Sincerely,",
        req.requester_name,
    ])
    return "\n".join(lines)


def save_outputs(req: BlockingRequest, message_text: str) -> tuple[Path, Path]:
    json_path = OUTPUT_DIR / "justia_block_request.json"
    txt_path = OUTPUT_DIR / "justia_block_request.txt"

    json_path.write_text(json.dumps(asdict(req), indent=2), encoding="utf-8")
    txt_path.write_text(message_text, encoding="utf-8")
    return json_path, txt_path


# =========================
# OPTIONAL SMTP SENDING
# =========================

def send_email_via_smtp(
    recipient: str,
    subject: str,
    body: str,
    sender_name: str,
    sender_email: str,
) -> None:
    if not all([SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD]):
        raise RuntimeError("SMTP is not configured. Fill SMTP_HOST, SMTP_USERNAME, and SMTP_PASSWORD.")

    msg = EmailMessage()
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        if SMTP_USE_TLS:
            server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)


# =========================
# MAIN
# =========================

def main() -> None:
    evidence = extract_evidence(INPUT_HTML)
    req = build_request(evidence)
    message_text = build_message_text(req)
    json_path, txt_path = save_outputs(req, message_text)

    print("Created request packet:")
    print(f"  JSON: {json_path}")
    print(f"  Text: {txt_path}")
    print(f"  Support page: {JUSTIA_SUPPORT_URL}")

    if JUSTIA_EMAIL:
        print(f"Attempting SMTP send to: {JUSTIA_EMAIL}")
        send_email_via_smtp(
            recipient=JUSTIA_EMAIL,
            subject=REQUEST_SUBJECT,
            body=message_text,
            sender_name=SENDER_NAME,
            sender_email=SENDER_EMAIL,
        )
        print("Email sent.")
    else:
        print("No Justia email configured. Use the generated text with the Justia support form.")


if __name__ == "__main__":
    main()
