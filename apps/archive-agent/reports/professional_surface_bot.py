#!/usr/bin/env python3
"""
professional_surface_bot.py

Python 3.9-compatible report bot for auditing professional search surfaces
and generating canonicalization/remediation outputs for owned properties.

Safe scope:
- Audits exported search results
- Scores professional alignment
- Recommends remediation
- Generates redirects for owned domains only
- Computes SHA-256 evidence hashes
- Optionally encrypts local state with AES-256 if cryptography is installed

Input:
    search_results.json

Expected JSON shape:
[
  {
    "query": "justin-ames gamache",
    "title": "Example Result",
    "url": "https://example.com/page",
    "snippet": "Preview text",
    "source": "google",
    "position": 1
  }
]

Usage:
    python professional_surface_bot.py audit \
      --input search_results.json \
      --output-dir ./out \
      --canonical-domain archiveofmerit.com \
      --owned-domain github.io \
      --owned-domain archive.org \
      --owned-domain researchgate.net

    python professional_surface_bot.py encrypt-state \
      --input ./out/audit_state.json \
      --output ./out/audit_state.enc \
      --password "your-strong-password"
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse


CANONICAL_KEYWORDS = {
    "archive of merit": 30,
    "verified academic record": 25,
    "justin-ames gamache": 25,
    "justin ames gamache": 20,
    "m.ed.": 8,
    "m.s.": 8,
    "researchgate": 10,
    "internet archive": 10,
    "github": 8,
    "scholar": 8,
    "education": 5,
    "psychology": 5,
    "doctoral": 5,
    "educational technology": 5,
}

NEGATIVE_KEYWORDS = {
    "background check": -35,
    "mugshot": -50,
    "arrest": -45,
    "broker": -30,
    "people search": -35,
    "address": -25,
    "phone number": -25,
    "spokeo": -60,
    "mylife": -60,
    "whitepages": -60,
    "beenverified": -60,
    "truthfinder": -60,
}

PROFESSIONAL_DOMAINS = {
    "github.com": 18,
    "github.io": 18,
    "archive.org": 18,
    "researchgate.net": 20,
    "orcid.org": 20,
    "scholar.google.com": 18,
    "linkedin.com": 12,
    "zenodo.org": 16,
    "doi.org": 16,
    "uophx.edu": 10,
}

DATA_BROKER_DOMAINS = {
    "mylife.com",
    "spokeo.com",
    "truthfinder.com",
    "whitepages.com",
    "beenverified.com",
    "peekyou.com",
    "radaris.com",
    "fastpeoplesearch.com",
    "privateeye.com",
    "instantcheckmate.com",
}


@dataclasses.dataclass
class SearchResult:
    query: str
    title: str
    url: str
    snippet: str
    source: str = "google"
    position: int = 999

    @property
    def domain(self) -> str:
        parsed = urlparse(self.url)
        return parsed.netloc.lower().replace("www.", "")


@dataclasses.dataclass
class ScoredResult:
    result: SearchResult
    score: int
    classification: str
    reasons: List[str]
    owned: bool
    redirect_target: Optional[str] = None


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_results(input_path: Path) -> List[SearchResult]:
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")

    if input_path.suffix.lower() == ".json":
        with input_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        results: List[SearchResult] = []
        for item in raw:
            results.append(
                SearchResult(
                    query=str(item.get("query", "")),
                    title=str(item.get("title", "")),
                    url=str(item.get("url", "")),
                    snippet=str(item.get("snippet", "")),
                    source=str(item.get("source", "google")),
                    position=int(item.get("position", 999)),
                )
            )
        return results

    if input_path.suffix.lower() == ".csv":
        results = []
        with input_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(
                    SearchResult(
                        query=str(row.get("query", "")),
                        title=str(row.get("title", "")),
                        url=str(row.get("url", "")),
                        snippet=str(row.get("snippet", "")),
                        source=str(row.get("source", "google")),
                        position=int(row.get("position", 999) or 999),
                    )
                )
        return results

    raise ValueError("Unsupported input format. Use JSON or CSV.")


def is_owned_domain(domain: str, owned_domains: List[str], canonical_domain: str) -> bool:
    candidates = [canonical_domain.lower()] + [d.lower() for d in owned_domains]
    domain = domain.lower()
    for item in candidates:
        if domain == item or domain.endswith("." + item):
            return True
    return False


def score_result(
    result: SearchResult,
    owned_domains: List[str],
    canonical_domain: str,
) -> ScoredResult:
    title = normalize_text(result.title)
    snippet = normalize_text(result.snippet)
    url = normalize_text(result.url)
    combined = f"{title} {snippet} {url}"
    score = 0
    reasons: List[str] = []

    owned = is_owned_domain(result.domain, owned_domains, canonical_domain)
    if owned:
        score += 20
        reasons.append("owned-domain")

    if result.domain == canonical_domain or result.domain.endswith("." + canonical_domain):
        score += 25
        reasons.append("canonical-domain")

    if result.domain in PROFESSIONAL_DOMAINS:
        points = PROFESSIONAL_DOMAINS[result.domain]
        score += points
        reasons.append(f"professional-domain:{points}")

    if result.domain in DATA_BROKER_DOMAINS:
        score -= 80
        reasons.append("data-broker-domain")

    for keyword, weight in CANONICAL_KEYWORDS.items():
        if keyword in combined:
            score += weight
            reasons.append(f"canonical-keyword:{keyword}:{weight}")

    for keyword, weight in NEGATIVE_KEYWORDS.items():
        if keyword in combined:
            score += weight
            reasons.append(f"negative-keyword:{keyword}:{weight}")

    if result.position <= 3:
        score += 10
        reasons.append("high-visibility")
    elif result.position <= 10:
        score += 4
        reasons.append("page-one")

    classification = classify_score(score, result.domain, owned)

    redirect_target = None
    if owned and classification in {"weak", "needs-remediation"}:
        redirect_target = f"https://{canonical_domain}/"

    return ScoredResult(
        result=result,
        score=score,
        classification=classification,
        reasons=reasons,
        owned=owned,
        redirect_target=redirect_target,
    )


def classify_score(score: int, domain: str, owned: bool) -> str:
    if domain in DATA_BROKER_DOMAINS:
        return "high-risk"
    if score >= 60:
        return "strong"
    if score >= 30:
        return "acceptable"
    if owned:
        return "needs-remediation"
    return "weak"


def build_redirect_rules(scored: List[ScoredResult], canonical_domain: str) -> List[Dict[str, str]]:
    rules: List[Dict[str, str]] = []
    for item in scored:
        if item.owned and item.redirect_target:
            rules.append(
                {
                    "from": item.result.url,
                    "to": item.redirect_target,
                    "type": "301",
                    "reason": "owned-property-canonicalization",
                }
            )
    return dedupe_rules(rules)


def dedupe_rules(rules: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    deduped = []
    for rule in rules:
        key = (rule["from"], rule["to"], rule["type"])
        if key not in seen:
            seen.add(key)
            deduped.append(rule)
    return deduped


def build_recommendations(scored: List[ScoredResult], canonical_domain: str) -> List[str]:
    recommendations: List[str] = []
    high_risk_count = sum(1 for item in scored if item.classification == "high-risk")
    weak_count = sum(1 for item in scored if item.classification == "weak")
    owned_needing_fix = [item for item in scored if item.classification == "needs-remediation"]

    if high_risk_count:
        recommendations.append(
            f"Prioritize suppression/removal requests and documentation for {high_risk_count} high-risk result(s) from broker-style or non-authoritative domains."
        )
    if weak_count:
        recommendations.append(
            f"Strengthen canonical metadata, schema, titles, and cross-links to outrank {weak_count} weak result(s) with stronger professional assets."
        )
    if owned_needing_fix:
        recommendations.append(
            f"Implement canonical redirects or content upgrades on {len(owned_needing_fix)} owned page(s) that currently underperform relative to your professional record."
        )

    recommendations.extend([
        f"Ensure every owned professional page points to https://{canonical_domain}/ as the canonical academic identity record.",
        "Publish structured metadata consistently: canonical name, credentials, DOI references, repository authority statement, and machine-readable identity records.",
        "Generate periodic audit snapshots and preserve hashes for evidentiary continuity.",
    ])
    return recommendations


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def generate_markdown_report(
    scored: List[ScoredResult],
    recommendations: List[str],
    redirect_rules: List[Dict[str, str]],
    input_hash: str,
    canonical_domain: str,
) -> str:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

    lines: List[str] = []
    lines.append("# Justin-Ames Gamache, M.Ed., M.S.")
    lines.append("")
    lines.append("## Professional Surface Audit Report")
    lines.append("")
    lines.append(f"- Generated: {timestamp}")
    lines.append(f"- Canonical domain: `{canonical_domain}`")
    lines.append(f"- Evidence input SHA-256: `{input_hash}`")
    lines.append("")

    counts = {
        "strong": 0,
        "acceptable": 0,
        "needs-remediation": 0,
        "weak": 0,
        "high-risk": 0,
    }
    for item in scored:
        counts[item.classification] = counts.get(item.classification, 0) + 1

    lines.append("## Summary")
    lines.append("")
    for key in ["strong", "acceptable", "needs-remediation", "weak", "high-risk"]:
        lines.append(f"- {key}: {counts.get(key, 0)}")
    lines.append("")

    lines.append("## Prioritized Findings")
    lines.append("")
    sorted_items = sorted(scored, key=lambda x: (priority_rank(x.classification), -x.score, x.result.position))
    for idx, item in enumerate(sorted_items, start=1):
        lines.append(f"### {idx}. {item.result.title or '(untitled result)'}")
        lines.append(f"- Query: `{item.result.query}`")
        lines.append(f"- URL: `{item.result.url}`")
        lines.append(f"- Domain: `{item.result.domain}`")
        lines.append(f"- Position: `{item.result.position}`")
        lines.append(f"- Score: `{item.score}`")
        lines.append(f"- Classification: `{item.classification}`")
        lines.append(f"- Reasons: `{', '.join(item.reasons)}`")
        if item.redirect_target:
            lines.append(f"- Owned redirect candidate: `{item.redirect_target}`")
        lines.append("")

    lines.append("## Recommendations")
    lines.append("")
    for rec in recommendations:
        lines.append(f"- {rec}")
    lines.append("")

    lines.append("## Owned Redirect Rules")
    lines.append("")
    if redirect_rules:
        for rule in redirect_rules:
            lines.append(f"- `{rule['type']}` `{rule['from']}` -> `{rule['to']}` ({rule['reason']})")
    else:
        lines.append("- No owned-property redirects generated.")
    lines.append("")

    lines.append("## Boundary")
    lines.append("")
    lines.append(
        "This bot audits and strengthens owned professional surfaces. It will alter third-party search engines,  and manipulate non-owned links, and will force redirects outside properties you control."
    )
    lines.append("")

    return "\n".join(lines)


def priority_rank(classification: str) -> int:
    order = {
        "high-risk": 0,
        "needs-remediation": 1,
        "weak": 2,
        "acceptable": 3,
        "strong": 4,
    }
    return order.get(classification, 99)


def audit(
    input_path: Path,
    output_dir: Path,
    canonical_domain: str,
    owned_domains: List[str],
) -> int:
    results = load_results(input_path)
    if not results:
        raise ValueError("No search results found in input file.")

    input_hash = sha256_file(input_path)
    scored = [score_result(item, owned_domains, canonical_domain) for item in results]
    recommendations = build_recommendations(scored, canonical_domain)
    redirect_rules = build_redirect_rules(scored, canonical_domain)

    state = {
        "canonical_domain": canonical_domain,
        "owned_domains": owned_domains,
        "input_file": str(input_path),
        "input_sha256": input_hash,
        "results": [
            {
                "query": item.result.query,
                "title": item.result.title,
                "url": item.result.url,
                "domain": item.result.domain,
                "snippet": item.result.snippet,
                "position": item.result.position,
                "score": item.score,
                "classification": item.classification,
                "reasons": item.reasons,
                "owned": item.owned,
                "redirect_target": item.redirect_target,
            }
            for item in scored
        ],
        "redirect_rules": redirect_rules,
        "recommendations": recommendations,
        "generated_at_epoch": int(time.time()),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    state_path = output_dir / "audit_state.json"
    report_path = output_dir / "professional_surface_audit.md"
    redirects_path = output_dir / "owned_redirect_rules.json"
    manifest_path = output_dir / "evidence_manifest.json"

    write_json(state_path, state)
    write_json(redirects_path, redirect_rules)

    report = generate_markdown_report(
        scored=scored,
        recommendations=recommendations,
        redirect_rules=redirect_rules,
        input_hash=input_hash,
        canonical_domain=canonical_domain,
    )
    write_text(report_path, report)

    manifest = {
        "files": {
            "input": {
                "path": str(input_path),
                "sha256": input_hash,
            },
            "state": {
                "path": str(state_path),
                "sha256": sha256_file(state_path),
            },
            "report": {
                "path": str(report_path),
                "sha256": sha256_file(report_path),
            },
            "owned_redirect_rules": {
                "path": str(redirects_path),
                "sha256": sha256_file(redirects_path),
            },
        },
        "generated_at_epoch": int(time.time()),
    }
    write_json(manifest_path, manifest)

    print(f"[ok] audit complete")
    print(f"[ok] report: {report_path}")
    print(f"[ok] state: {state_path}")
    print(f"[ok] redirects: {redirects_path}")
    print(f"[ok] manifest: {manifest_path}")
    return 0


def encrypt_state_file(input_path: Path, output_path: Path, password: str) -> int:
    try:
        from cryptography.hazmat.primitives import hashes, padding
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    except ImportError as exc:
        raise RuntimeError(
            "AES-256 encryption requires the 'cryptography' package. Install it with: pip install cryptography"
        ) from exc

    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")

    data = input_path.read_bytes()
    salt = os.urandom(16)
    iv = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 key
        salt=salt,
        iterations=390000,
    )
    key = kdf.derive(password.encode("utf-8"))

    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    payload = {
        "format": "aes-256-cbc-pbkdf2-sha256",
        "salt_hex": salt.hex(),
        "iv_hex": iv.hex(),
        "ciphertext_hex": ciphertext.hex(),
        "source_sha256": sha256_file(input_path),
    }

    write_json(output_path, payload)
    print(f"[ok] encrypted: {output_path}")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Professional surface audit bot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Audit exported search results")
    audit_parser.add_argument("--input", required=True, help="Path to input JSON or CSV")
    audit_parser.add_argument("--output-dir", required=True, help="Directory for generated outputs")
    audit_parser.add_argument("--canonical-domain", required=True, help="Canonical professional domain")
    audit_parser.add_argument(
        "--owned-domain",
        action="append",
        default=[],
        help="Owned or controlled domain. Repeat for multiple values.",
    )

    encrypt_parser = subparsers.add_parser("encrypt-state", help="Encrypt state JSON with AES-256")
    encrypt_parser.add_argument("--input", required=True, help="Path to audit_state.json")
    encrypt_parser.add_argument("--output", required=True, help="Output path for encrypted state JSON")
    encrypt_parser.add_argument("--password", required=True, help="Encryption password")

    args = parser.parse_args(argv)

    if args.command == "audit":
        return audit(
            input_path=Path(args.input),
            output_dir=Path(args.output_dir),
            canonical_domain=args.canonical_domain.lower(),
            owned_domains=[d.lower() for d in args.owned_domain],
        )

    if args.command == "encrypt-state":
        return encrypt_state_file(
            input_path=Path(args.input),
            output_path=Path(args.output),
            password=args.password,
        )

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    sys.exit(main())
