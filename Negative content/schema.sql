CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_date TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_reference TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exhibits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id INTEGER NOT NULL,
    exhibit_label TEXT NOT NULL,
    description TEXT NOT NULL,
    file_path TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (incident_id) REFERENCES incidents(id)
);
