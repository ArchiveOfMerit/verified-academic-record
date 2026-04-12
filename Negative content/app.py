import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path("records.db")


def utc_now() -> str:
    return datetime.utcnow().isoformat()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_date TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            source_type TEXT NOT NULL,
            source_reference TEXT,
            risk_level TEXT NOT NULL DEFAULT 'medium',
            matched_name INTEGER NOT NULL DEFAULT 0,
            negativity_score INTEGER NOT NULL DEFAULT 0,
            action TEXT NOT NULL DEFAULT 'review',
            query_text TEXT,
            case_reference TEXT,
            jurisdiction TEXT DEFAULT 'Vermont',
            is_quarantined INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exhibits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id INTEGER NOT NULL,
            exhibit_label TEXT NOT NULL,
            description TEXT NOT NULL,
            file_path TEXT,
            file_hash TEXT,
            file_type TEXT,
            evidence_source_url TEXT,
            risk_level TEXT NOT NULL DEFAULT 'medium',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (incident_id) REFERENCES incidents(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS blocked_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_pattern TEXT NOT NULL UNIQUE,
            risk_level TEXT NOT NULL DEFAULT 'high',
            action TEXT NOT NULL DEFAULT 'quarantine',
            reason TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS blocked_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exact_url TEXT NOT NULL UNIQUE,
            risk_level TEXT NOT NULL DEFAULT 'high',
            action TEXT NOT NULL DEFAULT 'quarantine',
            reason TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS review_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id INTEGER,
            event_type TEXT NOT NULL,
            event_detail TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (incident_id) REFERENCES incidents(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def sha256_file(file_path: str) -> str:
    path = Path(file_path)
    if not file_path or not path.exists():
        return ""

    hasher = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def add_incident(
    incident_date: str,
    title: str,
    summary: str,
    source_type: str,
    source_reference: str = "",
    risk_level: str = "medium",
    matched_name: bool = False,
    negativity_score: int = 0,
    action: str = "review",
    query_text: str = "",
    case_reference: str = "",
    jurisdiction: str = "Vermont",
    is_quarantined: bool = False
) -> int:
    conn = get_connection()
    cur = conn.cursor()

    created_at = utc_now()

    cur.execute("""
        INSERT INTO incidents (
            incident_date,
            title,
            summary,
            source_type,
            source_reference,
            risk_level,
            matched_name,
            negativity_score,
            action,
            query_text,
            case_reference,
            jurisdiction,
            is_quarantined,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        incident_date,
        title,
        summary,
        source_type,
        source_reference,
        risk_level,
        int(matched_name),
        negativity_score,
        action,
        query_text,
        case_reference,
        jurisdiction,
        int(is_quarantined),
        created_at,
        created_at
    ))

    incident_id = cur.lastrowid

    cur.execute("""
        INSERT INTO review_audit_log (
            incident_id,
            event_type,
            event_detail,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        incident_id,
        "incident_created",
        f"{risk_level}:{action}",
        created_at
    ))

    conn.commit()
    conn.close()
    return incident_id


def add_exhibit(
    incident_id: int,
    exhibit_label: str,
    description: str,
    file_path: str = "",
    file_type: str = "",
    evidence_source_url: str = "",
    risk_level: str = "medium"
) -> int:
    conn = get_connection()
    cur = conn.cursor()

    created_at = utc_now()
    file_hash = sha256_file(file_path)

    cur.execute("""
        INSERT INTO exhibits (
            incident_id,
            exhibit_label,
            description,
            file_path,
            file_hash,
            file_type,
            evidence_source_url,
            risk_level,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        incident_id,
        exhibit_label,
        description,
        file_path,
        file_hash,
        file_type,
        evidence_source_url,
        risk_level,
        created_at,
        created_at
    ))

    exhibit_id = cur.lastrowid
    conn.commit()
    conn.close()
    return exhibit_id


def add_blocked_query(
    query_pattern: str,
    reason: str,
    risk_level: str = "high",
    action: str = "quarantine"
) -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO blocked_queries (
            query_pattern,
            risk_level,
            action,
            reason
        )
        VALUES (?, ?, ?, ?)
    """, (query_pattern, risk_level, action, reason))

    conn.commit()
    conn.close()


def add_blocked_url(
    exact_url: str,
    reason: str,
    risk_level: str = "high",
    action: str = "quarantine"
) -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO blocked_urls (
            exact_url,
            risk_level,
            action,
            reason
        )
        VALUES (?, ?, ?, ?)
    """, (exact_url, risk_level, action, reason))

    conn.commit()
    conn.close()


def list_incidents() -> list[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM incidents
        ORDER BY incident_date ASC, id ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()

    add_blocked_query(
        query_pattern=r"gamache v ronan",
        reason="manual-query-blocklist:vermont-case-caption"
    )

    add_blocked_query(
        query_pattern=r"justin ames gamache vermont",
        reason="manual-query-blocklist:vermont-name-query"
    )

    add_blocked_url(
        exact_url="https://law.justia.com/cases/vermont/superior-court/2026/22-st-00949.html",
        reason="manual-url-blocklist:justia-vermont-superior-court-22-st-00949"
    )

    sample_id = add_incident(
        incident_date="2013-08-17",
        title="Repeated contact concerning resolved matter",
        summary=(
            "Documented repeated contact involving Gamache v Ronan and "
            "Justin Ames Gamache Vermont query monitoring."
        ),
        source_type="public_record",
        source_reference="Exhibit A / public filing",
        risk_level="high",
        matched_name=True,
        negativity_score=8,
        action="quarantine",
        query_text="justin ames gamache vermont",
        case_reference="Gamache v Ronan",
        is_quarantined=True
    )

    add_exhibit(
        incident_id=sample_id,
        exhibit_label="Exhibit A",
        description="Public record associated with the incident.",
        file_path="docs/exhibit_a.pdf",
        file_type="application/pdf",
        evidence_source_url="https://law.justia.com/cases/vermont/superior-court/2026/22-st-00949.html",
        risk_level="high"
    )

    for row in list_incidents():
        print(dict(row))
