import os, sqlite3


def walk_and_insert(conn: sqlite3.Connection, filesystem: dict, scan_id: int, parent_path: str | None = None):        
    for name, node in filesystem.items():
        if name == "__error__":
            continue

        insert_node (
            conn=conn,
            path=node["path"],
            parent_path=parent_path,
            kind=node["kind"],
            file_type=node["file_type"],
            last_modified=node["last_modified"],
            last_seen_run=scan_id,
            hash=node["hash"],
            size_bytes=node["size_bytes"],
        )
        if node["kind"] == "dir":
            walk_and_insert(conn=conn, 
                            filesystem=node.get("children", {}), 
                            parent_path=node["path"], 
                            scan_id=scan_id)

def mark_unseen_nodes_deleted(conn: sqlite3.Connection, scan_id: int):
    statement = """
    UPDATE nodes 
    SET deleted = 1 
    WHERE deleted = 0 
      AND last_seen_run <> ?
    """
    conn.execute(statement, (scan_id, ))


def node_unchanged(conn: sqlite3.Connection, path: str, size_bytes: int, last_modified: float) -> bool:
    statement = """
    SELECT 1
    FROM nodes
    WHERE path = ?
      AND size_bytes = ?
      AND last_modified = ?
    LIMIT 1
    """
    return conn.execute(statement, (path, size_bytes, last_modified)).fetchone()[0] is not None


def insert_node(
    conn: sqlite3.Connection, 
    path: str, 
    parent_path: str | None, 
    kind: str, 
    file_type: str | None, 
    last_modified: float | None, 
    last_seen_run: int, 
    hash: str | None = None, 
    size_bytes: int | None = None
) -> None:
    conn.execute(
        """
        INSERT INTO nodes(path, parent_path, kind, file_type, size_bytes, hash, last_modified, last_seen_run, deleted) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        ON CONFLICT(path) DO UPDATE SET
            parent_path   = excluded.parent_path,
            kind          = excluded.kind,
            file_type     = excluded.file_type,
            size_bytes    = excluded.size_bytes,
            hash          = excluded.hash,
            last_modified = excluded.last_modified,
            last_seen_run = excluded.last_seen_run,
            deleted       = 0
        """,
        (path, parent_path, kind, file_type, size_bytes, hash, last_modified, last_seen_run)
    )

def nodes(conn: sqlite3.Connection):
    return conn.execute("SELECT * FROM nodes ORDER BY path").fetchall()

def file_count(conn: sqlite3.Connection):
    return conn.execute('SELECT COUNT(*) FROM nodes WHERE kind = "file"').fetchone()[0]

def file_by_scan(conn: sqlite3.Connection, scan_id: int) -> list:
    return conn.execute(
        "SELECT * FROM nodes WHERE last_seen_id = ?", 
        (scan_id, )
    ).fetchall()

def file_by_dir(conn: sqlite3.Connection, path: str) -> list:
    return conn.execute('SELECT * FROM nodes WHERE parent_path = ? ORDER BY path', (path, )).fetchall()

def largest_files(conn: sqlite3.Connection, run_id: int | None = None, file_count: int = 1):
    statement = """"
    SELECT *
    FROM nodes
    WHERE kind = "file"
    """

    params: list[object] = []

    if run_id is not None:
        statement += "AND run_id = ?"
        params.append(run_id)
    
    statement += "ORDER BY size_bytes DESC LIMIT ?"
    params.append(file_count)

    return conn.execute('SELECT * FROM nodes WHERE kind="file" ORDER BY size_bytes DESC LIMIT ?', params).fetchall()

def max_depth(conn: sqlite3.Connection):
    return 1


