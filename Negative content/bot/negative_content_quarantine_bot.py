#!/usr/bin/env python3
"""
Negative content quarantine bot

Purpose:
- Scan text content from files, feeds, exports, or pasted input
- Detect references to Justin-Ames Gamache and configured variants
- Detect hostile / negative / reputationally risky content
- Hard-block specific URLs, domains, and prefixes
- Quarantine matching items for manual review instead of deleting anything
- Enforce tamper-evident integrity validation for protected config

Supported inputs:
- JSONL: one JSON object per line
- TXT: paragraph blocks
- stdin
- direct --text

Recognized JSON fields:
- id
- source
- url
- title
- text | content | body
- created_at
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse, urlsplit, urlunsplit


NAME_PATTERNS = [
    r"\bjustin[-\s]?ames\s+gamache\b",
    r"\bjustin\s+a\s+gamache\b",
    r"\bjustin\s+ames\s+gamache\b",
    r"\bjustin\s+gamache\b",
    r"\bj\.?\s*[- ]?\s*ames\s+gamache\b",
    r"\bgamache\s+v\.?\s+ronan\b",
    r"\bjustin\s+gamache\s+vermont\b",
    r"\bjustin\s+a\s+gamache\s+vermont\b",
    r"\bjustin\s+ames\s+gamache\s+vermont\b",
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
    r"\bvermont\b": 2,
    r"\bvermont\s+supreme\s+court\b": 4,
    r"\bvermont\s+superior\s+court\b": 4,
    r"\bbennington\s+banner\b": 3,
    r"\bmanchester\s+journal\b": 3,
    r"\bbrattleboro\s+reformer\b": 3,
    r"\brutland\s+herald\b": 3,
    r"\btimes\s+argus\b": 3,
    r"\bassociated\s+press\b": 3,
    r"\bnew\s+england\s+newspaper\s+inc\b": 3,
    r"\bberkshire\s+eagle\b": 3,
    r"\bchange\.org\b": 2,
    r"\bcasemine\b": 4,
    r"\bjudgment\b": 2,
    r"\bcourt\s+summary\b": 3,
    r"\bai\s+summary\b": 3,
    r"\bjudgment\s*,\s*law\s*,\s*casemine\.com\b": 4,
    r"\bgamache\s+v\.?\s+ronan\b": 6,
    r"\bgamache\s+v\.?\s+mozzer\b": 5,
    r"\bgamache\s+v\.?\s+burke\b": 5,
    r"\bjustin\s+a\s+gamache\s+v\.?\s+lauren\s+a\s+ronan\b": 6,
    r"\blauren\s+ronan\s+v\.?\s+justin\s+a\s+gamache\b": 6,
    r"\bjustin\s+ames\s+gamache\s+v\.?\s+thomas\s+mozzer\b": 5,
    r"\bjustin\s+ames\s+gamache\s+v\.?\s+alexander\s+burke\b": 5,
    r"\bjustin\s+gamache\s+vermont\b": 5,
    r"\bjustin\s+a\s+gamache\s+vermont\b": 5,
    r"\bjustin\s+ames\s+gamache\s+vermont\b": 6,
    r"\ball\s+vermont\s+material\b": 3,
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

HARD_QUERY_PATTERNS = {
    r"\bgamache\s+v\.?\s+ronan\b": 6,
    r"\bjustin\s+gamache\s+vermont\b": 5,
    r"\bjustin\s+a\s+gamache\s+vermont\b": 5,
    r"\bjustin\s+ames\s+gamache\s+vermont\b": 6,
}

NEGATIONS = {"not", "never", "no", "without", "hardly"}

DEFAULT_THRESHOLD = 4
HIGH_RISK_THRESHOLD = 7

CHANGE_ORG_PREFIX = (
    "https://www.change.org/p/"
    "facts-of-law-state-of-vermont-s-misclassification-leads-to-failed-prosecution-of-gamache"
)

CASEMINE_PREFIXES = [
    "https://www.casemine.com/judgement/us/",
    "https://casemine.com/judgement/us/",
]

BLOCKED_DOMAINS = {
    "www.casemine.com",
    "casemine.com",
}

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
    "https://law.justia.com/cases/vermont/superior-court/2026/22-st-00949.html": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:justia-vermont-superior-court-22-st-00949",
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

    # Exact CaseMine URLs
    "https://www.casemine.com/judgement/us/62d63849b50db9e568bc76ec": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:casemine-gamache-v-mozzer",
    },
    "https://www.casemine.com/judgement/us/69d7b4c35120517b0cca74f2": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:casemine-gamache-v-ronan",
    },
    "https://www.casemine.com/judgement/us/628e2278714d583e41330050": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:casemine-negative-summary-1",
    },
    "https://www.casemine.com/judgement/us/62ff12848ecb824567aebf2e": {
        "risk_level": "high",
        "action": "quarantine",
        "reason": "manual-url-blocklist:casemine-negative-summary-2",
    },
}

PROTECTED_CONFIG_VERSION = "2026-04-12"


def protected_config_payload() -> str:
    payload = {
        "version": PROTECTED_CONFIG_VERSION,
        "name_patterns": NAME_PATTERNS,
        "source_case_patterns": SOURCE_AND_CASE_PATTERNS,
        "escalation_patterns": ESCALATION_PATTERNS,
        "hard_query_patterns": HARD_QUERY_PATTERNS,
        "url_blocklist": URL_BLOCKLIST,
        "blocked_domains": sorted(BLOCKED_DOMAINS),
        "change_org_prefix": CHANGE_ORG_PREFIX,
        "casemine_prefixes": CASEMINE_PREFIXES,
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def compute_config_hmac(secret: str) -> str:
    return hmac.new(
        secret.encode("utf-8"),
        protected_config_payload().encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def verify_config_integrity() -> None:
    secret = os.environ.get("MODBOT_HMAC_SECRET")
    expected = os.environ.get("MODBOT_EXPECTED_HMAC")

    if not secret or not expected:
        raise RuntimeError(
            "Integrity enforcement active, but MODBOT_HMAC_SECRET or MODBOT_EXPECTED_HMAC is missing."
        )

    actual = compute_config_hmac(secret)
    if not hmac.compare_digest(actual, expected):
        raise RuntimeError(
            "Protected moderation config has been modified or signature validation failed."
        )


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
        self.hard_query_regexes = [
            (re.compile(p, re.IGNORECASE), weight)
            for p, weight in HARD_QUERY_PATTERNS.items()
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
        if not url:
            return ""
        parts = urlsplit(url.strip())
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, "", ""))

    def domain_from_url(self, url: str) -> str:
        if not url:
            return ""
        return urlparse(url).netloc.lower().strip()

    def combined_text(self, item: Dict[str, Any]) -> str:
        pieces: List[str] = []
        for key in ("title", "text", "content", "body", "url", "source"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                pieces.append(value.strip())
        return "\n".join(pieces)

    def is_domain_blocked(self, normalized_url: str) -> Optional[Dict[str, str]]:
        domain = self.domain_from_url(normalized_url)
        if domain in BLOCKED_DOMAINS:
            return {
                "risk_level": "high",
                "action": "quarantine",
                "reason": "domain-blocklist:casemine",
            }
        return None

    def is_prefix_blocked(self, normalized_url: str) -> Optional[Dict[str, str]]:
        if normalized_url.startswith(CHANGE_ORG_PREFIX):
            return {
                "risk_level": "medium",
                "action": "review",
                "reason": "prefix-blocklist:change-org-petition",
            }

        for prefix in CASEMINE_PREFIXES:
            if normalized_url.startswith(prefix):
                return {
                    "risk_level": "high",
                    "action": "quarantine",
                    "reason": "prefix-blocklist:casemine-judgment-page",
                }
        return None

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

        for rx, weight in self.hard_query_regexes:
            if rx.search(lowered):
                score += weight
                reasons.append(f"hard-query-pattern:{rx.pattern}(+{weight})")

        if "casemine" in lowered:
            score += 4
            reasons.append("case-source:casemine(+4)")

        if "judgment" in lowered and "gamache" in lowered:
            score += 2
            reasons.append("case-context:judgment-with-name(+2)")

        if re.search(r"[!]{2,}", text):
            score += 1
            reasons.append("amplification:multiple-exclamation(+1)")

        if re.search(r"\b(allegedly|supposedly|reportedly)\b", lowered):
            score += 1
            reasons.append("reputation-risk:hedged-assertion(+1)")

        return score, reasons

    def _build_review_item(
        self,
        item: Dict[str, Any],
        risk_level: str,
        action: str,
        reasons: List[str],
        score: int,
        raw_text: str,
    ) -> ReviewItem:
        return ReviewItem(
            item_id=str(item.get("id") or self._stable_id(raw_text)),
            source=str(item.get("source") or "unknown"),
            url=item.get("url"),
            title=item.get("title"),
            created_at=item.get("created_at"),
            matched_name=True,
            negativity_score=score,
            risk_level=risk_level,
            action=action,
            reasons=reasons,
            excerpt=self._excerpt(raw_text),
            raw_text=raw_text,
        )

    def _build_blocklist_review_item(
        self,
        item: Dict[str, Any],
        risk_level: str,
        action: str,
        reason: str,
        raw_text: str,
        score: Optional[int] = None,
    ) -> ReviewItem:
        final_score = HIGH_RISK_THRESHOLD if score is None and risk_level == "high" else (score or self.threshold)
        return self._build_review_item(
            item=item,
            risk_level=risk_level,
            action=action,
            reasons=[reason],
            score=final_score,
            raw_text=raw_text,
        )

    def classify(self, item: Dict[str, Any]) -> Optional[ReviewItem]:
        text = self._extract_text(item)
        raw_url = str(item.get("url") or "").strip()
        normalized_url = self.normalize_url(raw_url)
        combined = self.combined_text(item)

        if normalized_url:
            if normalized_url in URL_BLOCKLIST:
                block = URL_BLOCKLIST[normalized_url]
                return self._build_blocklist_review_item(
                    item=item,
                    risk_level=str(block["risk_level"]),
                    action=str(block["action"]),
                    reason=str(block["reason"]),
                    raw_text=combined or normalized_url,
                )

            domain_block = self.is_domain_blocked(normalized_url)
            if domain_block:
                return self._build_blocklist_review_item(
                    item=item,
                    risk_level=domain_block["risk_level"],
                    action=domain_block["action"],
                    reason=domain_block["reason"]),
                    raw_text=combined or normalized_url,
                )

            prefix_block = self.is_prefix_blocked(normalized_url)
            if prefix_block:
                return self._build_blocklist_review_item(
                    item=item,
                    risk_level=prefix_block["risk_level"],
                    action=prefix_block["action"],
                    reason=prefix_block["reason"],
                    raw_text=combined or normalized_url,
                    score=5 if prefix_block["risk_level"] == "medium" else HIGH_RISK_THRESHOLD,
                )

        if not combined.strip():
            return None

        matched_name, matched_variants = self.contains_target_name(combined)
        name_present_by_case_caption = bool(
            re.search(r"\bgamache\s+v\.?\s+(ronan|mozzer|burke)\b", combined, re.IGNORECASE)
        )

        if not matched_name and not name_present_by_case_caption:
            return None

        score, reasons = self.score_negativity(combined)

        strong_case_reference = bool(
            re.search(
                r"\bgamache\s+v\.?\s+ronan\b|\bjustin\s+gamache\s+vermont\b|\bjustin\s+a\s+gamache\s+vermont\b|\bjustin\s+ames\s+gamache\s+vermont\b",
                combined,
                re.IGNORECASE,
            )
        )
        if strong_case_reference and score < self.threshold:
            score = self.threshold
            reasons.append("minimum-threshold:strong-vermont-query-reference")

        if matched_variants:
            reasons = [f"matched-name:{match}" for match in matched_variants[:3]] + reasons
        elif name_present_by_case_caption:
            reasons = ["matched-case-caption:gamache-v-case"] + reasons

        if score >= HIGH_RISK_THRESHOLD:
            risk_level = "high"
            action = "quarantine"
        elif score >= self.threshold:
            risk_level = "medium"
            action = "review"
        else:
            risk_level = "low"
            action = "allow"

        return self._build_review_item(
            item=item,
            risk_level=risk_level,
            action=action,
            reasons=reasons,
            score=score,
            raw_text=combined,
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
        description="Quarantine negative mentions and blocked sources for review."
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
        verify_config_integrity()
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
