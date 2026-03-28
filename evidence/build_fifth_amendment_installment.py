from pathlib import Path
import re, json, hashlib
from bs4 import BeautifulSoup
from datetime import datetime, timezone

ATTACHMENT_PATH = Path("FalseInfo.txt")
STATEMENT = (
    "No loss is a loss and I did what 98% of people are afraid to do. "
    "Litigate and fight for myself and now I am being transparent on the issues that they hide from. "
    "I was within my constitutional rights the entire time and never gave them full details of my life. "
    "No warrant can force the contents of what is in your mind."
)

def main() -> None:
    raw = ATTACHMENT_PATH.read_text(encoding="utf-8", errors="replace")
    sha256 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()

    soup = BeautifulSoup(raw, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else None

    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    visible_text = soup.get_text("\n", strip=True)
    visible_lines = [ln.strip() for ln in visible_text.splitlines() if ln.strip()]

    patterns = [
        r"Vermont Judiciary Public Portal",
        r"Welcome,\s*Justin Ames",
        r"Smart Search",
        r"Search Results",
        r"Details",
        r"Gamache,\s*Justin Ames",
    ]
    indicators = []
    for pat in patterns:
        m = re.search(pat, raw, flags=re.I)
        if m:
            indicators.append(m.group(0))

    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "repository_target": "ArchiveOfMerit/verified-academic-record",
        "branch_target": "FIFTH-AMENDMENT-INSTALLMENT",
        "attachment": {
            "filename": ATTACHMENT_PATH.name,
            "sha256": sha256,
            "md5": md5,
            "detected_type": "saved HTML portal page",
            "title": title,
            "indicators_found": indicators,
        },
        "statement": STATEMENT,
        "interpretive_notes": [
            "The attachment is a raw saved portal page, not a finalized court order or narrative affidavit.",
            "Preserve the source artifact separately from authored interpretation.",
        ],
        "visible_text_preview": "\n".join(visible_lines[:40]),
    }

    Path("fifth_amendment_installment_evidence.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("Wrote fifth_amendment_installment_evidence.json")

if __name__ == "__main__":
    main()
