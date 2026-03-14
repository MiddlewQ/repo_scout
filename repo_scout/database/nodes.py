import sqlite3
from dataclasses import dataclass

from .model import *

def mark_unseen_nodes_deleted(conn: sqlite3.Connection, scan_id: int):
    statement = """
    UPDATE nodes 
    SET deleted = 1 
    WHERE deleted = 0 
      AND last_seen_run <> ?
    """
    conn.execute(statement, (scan_id, ))

def node_unchanged(
    conn: sqlite3.Connection, 
    path: str, 
    size_bytes: int, 
    last_modified: float
) -> bool:
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
    node: Node
) -> None:
    sql = """
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
    """
    conn.execute(
        sql,
        (node.path, node.parent_path, node.kind, node.file_type, node.size_bytes, node.hash_content, node.last_modified, node.last_seen_run)
    )


def nodes(conn: sqlite3.Connection) -> list[Node]:
    rows = conn.execute("SELECT * FROM nodes ORDER BY path").fetchall()
    return [row_to_node(row) for row in rows]

def file_count(conn: sqlite3.Connection) -> int:
    return conn.execute('SELECT COUNT(*) FROM nodes WHERE kind = "file"').fetchone()[0]

def file_by_scan(
    conn: sqlite3.Connection, 
    scan_id: int
) -> list[Node]:
    rows = conn.execute(
        "SELECT * FROM nodes WHERE last_seen_id = ?", 
        (scan_id, )
    ).fetchall()
    return [row_to_node(row) for row in rows]


def file_by_dir(conn: sqlite3.Connection, path: str) -> list[Node]:
    rows = conn.execute('SELECT * FROM nodes WHERE parent_path = ? ORDER BY path', (path, )).fetchall()
    return [row_to_node(row) for row in rows]

def largest_files(
    conn: sqlite3.Connection, 
    file_count: int = 5, 
    ignore: set[str] | None = None
) -> list[FileNode]:
    sql = """
    SELECT path, size_bytes
    FROM nodes
    WHERE kind = ?
      AND deleted = 0 
    """

    params: list[object] = ["file"]
    
    if ignore:
        ignore_sql, ignore_params = build_ignore_filter(ignore)
        sql += ignore_sql
        params.extend(ignore_params)

    sql += "ORDER BY size_bytes DESC LIMIT ?"
    params.append(file_count)
    rows = conn.execute(sql, params).fetchall()
    return [row_to_filenode(row) for row in rows]

def max_depth(conn: sqlite3.Connection):
    return 1

def clear_nodes(conn: sqlite3.Connection) -> int:
    conn.execute("DELETE FROM nodes")
    return conn.execute("SELECT changes()").fetchone()[0]
    
def hash_dupes(
    conn: sqlite3.Connection, 
    ignore: set | None = None, 
    include_empty: bool = False
) -> list[HashDupe]:
    sql = """
    SELECT hash, 
           COUNT(*) AS c 
    FROM nodes 
    WHERE kind='file'
    """

    params: list[object] = []

    if ignore:
        sql_ignore, params_ignore = build_ignore_filter(ignore)
        sql += "\n" + sql_ignore
        params.extend(params_ignore)

    if not include_empty:
        sql += "  AND size_bytes <> 0 "

    sql += """
      AND deleted=0 
      AND hash IS NOT NULL 
    GROUP BY hash 
    HAVING c > 1;
    """

    rows = conn.execute(sql, params).fetchall()
    return [row_to_hash_dupe(row) for row in rows]

def filepaths_by_hash(
    conn: sqlite3.Connection, 
    hash: str
) -> list[str]:
    sql = """
    SELECT path
    FROM nodes
    WHERE hash = ?
    """

    return [row["path"] for row in conn.execute(sql, (hash,)).fetchall()]


def build_ignore_filter(
    ignore: set[str]
) -> tuple[str, list[str]]:
    sql = ""
    params = []
    for raw in sorted(ignore):
        item = raw.strip()

        if item.startswith("./"):
            item = item[2:]
        item = item.lstrip("/") 

        if not item:
            continue

        if item.endswith("/"): # Ignore directory
            dir = item.rstrip("/")
            sql += "  AND path NOT LIKE ? AND path NOT LIKE ?\n    "
            params.append(f"{dir}/%")
            params.append(f"%/{dir}/%")
        elif "/" in item: # Ignore path
            sql += "  AND path != ? AND path NOT LIKE ?\n    "
            params.append(f"%{item}")
            params.append(f"%/{item}")
        else: # Ignore file
            sql += "  AND NOT (path = ? OR path LIKE ?)\n    "
            params.append(f"{item}")
            params.append(f"%/{item}")
    return sql, params