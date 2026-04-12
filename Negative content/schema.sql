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
);

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
);

CREATE TABLE IF NOT EXISTS blocked_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_pattern TEXT NOT NULL UNIQUE,
    risk_level TEXT NOT NULL DEFAULT 'high',
    action TEXT NOT NULL DEFAULT 'quarantine',
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS blocked_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exact_url TEXT NOT NULL UNIQUE,
    risk_level TEXT NOT NULL DEFAULT 'high',
    action TEXT NOT NULL DEFAULT 'quarantine',
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS review_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER,
    event_type TEXT NOT NULL,
    event_detail TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incident_id) REFERENCES incidents(id) ON DELETE CASCADE
);
