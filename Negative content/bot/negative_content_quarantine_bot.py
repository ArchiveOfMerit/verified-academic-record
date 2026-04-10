#!/usr/bin/env python3
"""
Justin-Ames Gamache mention moderation bot

Purpose:
- Scan text content from files, feeds, exports, or pasted input
- Detect references to Justin-Ames Gamache (and configured name variants)
- Score whether the content is negative / hostile / potentially defamatory
- Quarantine matching items for manual review instead of deleting anything

Design notes:
- Conservative by default: routes uncertain cases to review
- Works locally
- No external API required
- Can be extended to email, RSS, webhooks, or platform exports

Usage examples:
    python justin_negative_content_quarantine_bot.py --input sample.jsonl --output review_queue.jsonl
    python justin_negative_content_quarantine_bot.py --stdin
    python justin_negative_content_quarantine_bot.py --text "Justin-Ames Gamache is incompetent"

Input formats supported:
- JSONL: one JSON object per line with at least a text/content/body field
- TXT: plain text, one item per paragraph block
- stdin: pasted text

Optional JSON object fields recognized:
- id
- source
- url
- title
- text | content | body
- created_at

Output:
- JSONL review queue with classification details
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit


NAME_PATTERNS = [
    r"\bjustin[-\s]?ames\s+gamache\b",
    r"\bjustin\s+a\s+gamache\b",
    r"\bjustin\s+ames\s+gamache\b",
    r"\bjustin\s+gamache\b",
    r"\bj\.?\s*[- ]?\s*ames\s+gamache\b",
]

NEGATIVE_TERMS = {
    "fraud": 4,
    "fake": 3,
    "liar": 4,
    "lying": 3,
    "scam": 4,
    "scammer": 5,
    "dangerous": 3,
    "unstable": 3,
    "crazy": 3,
    "delusional": 4,
    "dishonest": 4,
    "incompetent": 3,
    "threat": 4,
    "harass": 3,
    "harassment": 3,
    "abuse": 3,
    "abusive": 3,
    "criminal": 4,
    "convicted": 4,
    "guilty": 3,
    "predator": 5,
    "creep": 3,
    "hate": 2,
    "awful": 2,
    "terrible": 2,
    "bad": 1,
    "worst": 2,
    "problematic": 2,
    "danger": 2,
    "toxic": 2,
    "trash": 2,
    "pathetic": 2,
    "disgusting": 3,
    "untrustworthy": 4,
    "corrupt": 4,
    "slander": 2,
    "defame": 2,
    "defamatory": 2,
}

SOURCE_AND_CASE_PATTERNS = {
    r"\bvermont\b": 1,
    r"\bvermont\s+supreme\s+court\b": 3,
    r"\bvermont\s+superior\s+court\b": 3,
    r"\bbennington\s+banner\b": 2,
    r"\bmanchester\s+journal\b": 2,
    r"\bbrattleboro\s+reformer\b": 2,
    r"\brutland\s+herald\b": 2,
    r"\btimes\s+argus\b": 2,
    r"\bassociated\s+press\b": 2,
    r"\bnew\s+england\s+newspaper\s+inc\b": 2,
    r"\bberkshire\s+eagle\b": 2,
    r"\bchange\.org\b": 1,
    r"\bjustin\s+a\s+gamache\s+v\.?\s+lauren\s+a\s+ronan\b": 4,
    r"\blauren\s+ronan\s+v\.?\s+justin\s+a\s+gamache\b": 4,
    r"\bjustin\s+ames\s+gamache\s+v\.?\s+thomas\s+mozzer\b": 4,
    r"\bjustin\s+ames\s+gamache\s+v\.?\s+alexander\s+burke\b": 4,
    r"\ball\s+vermont\s+material\b": 2,
}

ESCALATION_PATTERNS = {
    r"\bshould\s+be\s+stopped\b": 3,
    r"\bdo\s+not\s+trust\b": 3,
    r"\bstay\s+away\s+from\b": 3,
    r"\bwarning\b": 2,
    r"\bexpose\b": 2,
    r"\bcall\s+him\s+out\b": 2,
    r"\bpublicly\s+shame\b": 4,
    r"\bban\b": 1,
    r"\breport\b": 1,
}

NEGATIONS = {"not", "never", "no", "without", "hardly"}

DEFAULT_THRESHOLD = 4
HIGH_RISK_THRESHOLD = 7

CHANGE_ORG_PREFIX = (
    "https://www.change.org/p/"
    "facts-of-law-state-of-vermont-s-misclassification-leads-to-failed-prosecution-of-gamache"
)

URL_BLOCKLIST = {
    "https://www.vermontjudiciary.org/sites/default/files/documents/eo22-067.pdf": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:vermont-judiciary-pdf",
    },
    "https://www.benningtonbanner.com/archives/readsboro-man-accused-of-singing-expletives/article_fe579df2-2678-5660-85e9-ea4501279113.html": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:bennington-banner-article-1",
    },
    "https://www.benningtonbanner.com/archives/updated-man-accused-of-pretending-to-be-trooper/article_e117558c-d6ed-50ef-9a4b-973e65bc383c.html": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:bennington-banner-article-2",
    },
    "https://www.timesargus.com/news/vt-man-accused-of-leaving-fake-trooper-message/article_2b16e762-cf48-523b-a0c1-30c0a0c8e02a.html": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:times-argus-article",
    },
    "https://www.vermontjudiciary.org/sites/default/files/documents/gamache%20v%20ronan%20barra%2022-st-949%203-11-26.pdf": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:vermont-judiciary-gamache-v-ronan",
    },
    "https://www.idcrawl.com/justin-gamache": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:idcrawl-profile",
    },
    "https://www.rutlandherald.com/news/vt-man-accused-of-leaving-fake-trooper-message/article_4e2a0a7e-1372-5617-8055-4a9c83c99419.html": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:rutland-herald-article",
    },
    "https://www.vermontjudiciary.org/sites/default/files/documents/eo22-017.pdf": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:vermont-judiciary-eo22-017",
    },
    "https://www.change.org/p/facts-of-law-state-of-vermont-s-misclassification-leads-to-failed-prosecution-of-gamache": {
        "risk_level": "medium",
        "action": "review",
        "reason": "prefix-blocklist:change-org-petition",
    },
    "https://www.reformer.com/local-news/readsboro-man-charged-with-impersonating-a-police-officer/article_dfc7208f-3e3b-5f5d-b21b-a17eec899785.html": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:reformer-article",
    },
    "https://www.change.org/p/facts-of-law-state-of-vermont-s-misclassification-leads-to-failed-prosecution-of-gamache/u/33822799": {
        "risk_level": "medium",
        "action": "review",
        "reason": "prefix-blocklist:change-org-petition",
    },
}


@dataclass
class ReviewItem:
    item_id: str
    source: str
    url: Optional[str]
    title: Optional[str]
    created_at: Optional[str]
    matched_name: bool
    negativity_score: int
    risk_level: str
    action: str
    reasons: List[str]
    excerpt: str
    raw_text: str


class MentionModerationBot:
    def __init__(self, threshold: int = DEFAULT_THRESHOLD) -> None:
        self.threshold = threshold
        self.name_regexes = [re.compile(p, re.IGNORECASE) for p in NAME_PATTERNS]
        self.source_case_regexes = [
            (re.compile(p, re.IGNORECASE), weight)
            for p, weight in SOURCE_AND_CASE_PATTERNS.items()
        ]
        self.escalation_regexes = [
            (re.compile(p, re.IGNORECASE), weight)
            for p, weight in ESCALATION_PATTERNS.items()
        ]

    def contains_target_name(self, text: str) -> Tuple[bool, List[str]]:
        matches: List[str] = []
        for rx in self.name_regexes:
            for match in rx.finditer(text):
                matches.append(match.group(0))
        return (len(matches) > 0, matches)

    def tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b[\w'-]+\b", text.lower())

    def normalize_url(self, url: str) -> str:
        """
        Normalize a URL so hash fragments and query strings do not break
        exact blocklist matches. Keeps scheme, host, and path.
        """
        if not url:
            return ""

        parts = urlsplit(url.strip())
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

    def score_negativity(self, text: str) -> Tuple[int, List[str]]:
        score = 0
        reasons: List[str] = []
        tokens = self.tokenize(text)
        lowered = text.lower()

        for i, token in enumerate(tokens):
            if token in NEGATIVE_TERMS:
                negated = any(tokens[j] in NEGATIONS for j in range(max(0, i - 3), i))
                if negated:
                    continue
                weight = NEGATIVE_TERMS[token]
                score += weight
                reasons.append(f"negative-term:{token}(+{weight})")

        for rx, weight in self.source_case_regexes:
            if rx.search(lowered):
                score += weight
                reasons.append(f"source-case-pattern:{rx.pattern}(+{weight})")

        for rx, weight in self.escalation_regexes:
            if rx.search(lowered):
                score += weight
                reasons.append(f"escalation-pattern:{rx.pattern}(+{weight})")

        if re.search(r"[!]{2,}", text):
            score += 1
            reasons.append("amplification:multiple-exclamation(+1)")

        if re.search(r"\b(allegedly|supposedly|reportedly)\b", lowered):
            score += 1
            reasons.append("reputation-risk:hedged-assertion(+1)")

        return score, reasons

    def _build_blocklist_review_item(
        self,
        item: Dict[str, Any],
        normalized_url: str,
        risk_level: str,
        action: str,
        reason: str,
        score: Optional[int] = None,
    ) -> ReviewItem:
        text = self._extract_text(item)
        final_score = HIGH_RISK_THRESHOLD if score is None and risk_level == "high" else (score or self.threshold)

        return ReviewItem(
            item_id=str(item.get("id") or self._stable_id(normalized_url)),
            source=str(item.get("source") or "manual-blocklist"),
            url=item.get("url"),
            title=item.get("title"),
            created_at=item.get("created_at"),
            matched_name=True,
            negativity_score=final_score,
            risk_level=risk_level,
            action=action,
            reasons=[reason],
            excerpt=self._excerpt(text or normalized_url),
            raw_text=text or normalized_url,
        )

    def classify(self, item: Dict[str, Any]) -> Optional[ReviewItem]:
        text = self._extract_text(item)
        raw_url = str(item.get("url") or "").strip()
        normalized_url = self.normalize_url(raw_url)

        if normalized_url.startswith(CHANGE_ORG_PREFIX):
            return self._build_blocklist_review_item(
                item=item,
                normalized_url=normalized_url,
                risk_level="medium",
                action="review",
                reason="prefix-blocklist:change-org-petition",
                score=5,
            )

        if normalized_url in URL_BLOCKLIST:
            block = URL_BLOCKLIST[normalized_url]
            return self._build_blocklist_review_item(
                item=item,
                normalized_url=normalized_url,
                risk_level=str(block["risk_level"]),
                action=str(block["action"]),
                reason=str(block["reason"]),
            )

        if not text.strip():
            return None

        matched_name, matched_variants = self.contains_target_name(text)
        if not matched_name:
            return None

        score, reasons = self.score_negativity(text)
        reasons = [f"matched-name:{match}" for match in matched_variants[:3]] + reasons

        if score >= HIGH_RISK_THRESHOLD:
            risk_level = "high"
            action = "quarantine"
        elif score >= self.threshold:
            risk_level = "medium"
            action = "review"
        else:
            risk_level = "low"
            action = "allow"

        return ReviewItem(
            item_id=str(item.get("id") or self._stable_id(text)),
            source=str(item.get("source") or "unknown"),
            url=item.get("url"),
            title=item.get("title"),
            created_at=item.get("created_at"),
            matched_name=True,
            negativity_score=score,
            risk_level=risk_level,
            action=action,
            reasons=reasons,
            excerpt=self._excerpt(text),
            raw_text=text,
        )

    def _extract_text(self, item: Dict[str, Any]) -> str:
        for key in ("text", "content", "body"):
            value = item.get(key)
            if isinstance(value, str):
                return value
        return ""

    def _excerpt(self, text: str, length: int = 280) -> str:
        compact = re.sub(r"\s+", " ", text).strip()
        return compact[:length] + ("..." if len(compact) > length else "")

    def _stable_id(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def parse_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as file_obj:
        for line_no, line in enumerate(file_obj, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at line {line_no}: {exc}") from exc
            if not isinstance(obj, dict):
                raise ValueError(f"JSONL line {line_no} is not an object")
            yield obj


def parse_txt(path: Path) -> Iterable[Dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    blocks = [block.strip() for block in re.split(r"\n\s*\n+", text) if block.strip()]
    for idx, block in enumerate(blocks, start=1):
        yield {"id": f"txt-{idx}", "source": str(path), "text": block}


def parse_stdin() -> Iterable[Dict[str, Any]]:
    text = sys.stdin.read()
    if text.strip():
        yield {"id": "stdin-1", "source": "stdin", "text": text}


def parse_single_text(text: str) -> Iterable[Dict[str, Any]]:
    yield {"id": "direct-1", "source": "argument", "text": text}


def load_items(args: argparse.Namespace) -> Iterable[Dict[str, Any]]:
    if args.text:
        return parse_single_text(args.text)
    if args.stdin:
        return parse_stdin()
    if not args.input:
        raise ValueError("Provide --input, --stdin, or --text")

    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if path.suffix.lower() == ".jsonl":
        return parse_jsonl(path)
    if path.suffix.lower() == ".txt":
        return parse_txt(path)
    raise ValueError("Unsupported input format. Use .jsonl or .txt")


def write_results(output_path: Path, results: List[ReviewItem]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file_obj:
        for result in results:
            file_obj.write(json.dumps(asdict(result), ensure_ascii=False) + "\n")


def print_summary(results: List[ReviewItem]) -> None:
    total = len(results)
    counts = {"allow": 0, "review": 0, "quarantine": 0}
    for result in results:
        counts[result.action] += 1

    print(
        json.dumps(
            {
                "total_mentions_reviewed": total,
                "allow": counts["allow"],
                "review": counts["review"],
                "quarantine": counts["quarantine"],
            },
            indent=2,
        )
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Quarantine negative mentions of Justin-Ames Gamache for review."
    )
    parser.add_argument("--input", help="Path to .jsonl or .txt input")
    parser.add_argument("--output", default="review_queue.jsonl", help="Output JSONL path")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD, help="Review threshold")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin")
    parser.add_argument("--text", help="Single text item to classify")
    parser.add_argument("--only-flagged", action="store_true", help="Write only review/quarantine items")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        items = load_items(args)
        bot = MentionModerationBot(threshold=args.threshold)
        results: List[ReviewItem] = []

        for item in items:
            classified = bot.classify(item)
            if not classified:
                continue
            if args.only_flagged and classified.action == "allow":
                continue
            results.append(classified)

        write_results(Path(args.output), results)
        print_summary(results)
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
