DROP TABLE IF EXISTS nodes;

CREATE TABLE IF NOT EXISTS nodes ( 
    path TEXT PRIMARY KEY,
    parent_path TEXT,
    kind TEXT NOT NULL CHECK(kind in ("file", "dir")),
    file_type TEXT,
    size_bytes INTEGER,
    last_modified REAL NOT NULL,
    deleted INTEGER NOT NULL DEFAULT 0,
    last_seen_run INTEGER NOT NULL
)