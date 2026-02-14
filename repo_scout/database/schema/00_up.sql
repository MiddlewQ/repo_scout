CREATE TABLE nodes IF NOT EXISTS(
    path TEXT PRIMARY KEY,
    kind TEXT NOT NULL CHECK(kind in ('file', "dir")),
    parent_path TEXT,
    size_bytes INTEGER,
    last_modified REAL,
    ext TEXT,
    deleted INTEGER NOT NULL DEFAULT 0,
    last_seen_run INTEGER NOT NULL
)