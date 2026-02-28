import sqlite3
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Node:
    path: str
    parent_path: str
    kind: str
    
    hash: str | None
    file_type: str | None
    size_bytes: int | None
    last_modified: float
    
    deleted: bool
    last_seen_run: int


def row_to_node(row: sqlite3.Row) -> Node:
    return Node(
        path=row["path"],
        parent_path=row["parent_path"],
        kind=row["kind"],

        hash=row["hash"],
        file_type=row["file_type"],
        size_bytes=row["size_bytes"],
        last_modified=row["last_modified"],

        deleted=row["deleted"],
        last_seen_run=row["last_seen_run"]
    )

@dataclass(frozen=True)
class FileNode:
    path: str
    parent_path: str

    hash: str
    size_bytes: int
    file_type: str | None
    last_modified: float
    
    deleted: bool 
    last_seen_run: int

def row_to_filenode(row: sqlite3.Row) -> FileNode:
    return FileNode(
        path=row["path"],
        parent_path=row["parent_path"],
        
        hash=row["hash"],
        file_type=row["file_type"],
        size_bytes=row["size_bytes"],
        last_modified=row["last_modified"],

        deleted=row["deleted"],
        last_seen_run=row["last_seen_run"]
    )

@dataclass(frozen=True)
class ModifiedFileNode:
    path: str
    old_size: int
    new_size: int
    old_hash: str
    new_hash: str
    old_mtime: float
    new_mtime: float

def row_to_modified_filenode(old_row: sqlite3.Row, new_row: sqlite3.Row):
    return ModifiedFileNode(
        path=new_row["path"],
        old_size=old_row["size_bytes"],
        new_size=new_row["size_bytes"],
        old_hash=old_row["hash"],
        new_hash=new_row["hash"],
        old_mtime=old_row["last_modified"],
        new_mtime=new_row["last_modified"]
    )

@dataclass(frozen=True, slots=True)
class HashDupe:
    hash: str
    count: int

def row_to_hash_dupe(row: sqlite3.Row) -> HashDupe:
    return HashDupe(hash=row["hash"], count=row["c"])

def walk_and_insert(
    conn: sqlite3.Connection, 
    filesystem: dict, 
    scan_id: int, 
    parent_path: str | None = None
) -> None:
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
    path: str, 
    parent_path: str | None, 
    kind: str, 
    file_type: str | None, 
    last_modified: float | None, 
    last_seen_run: int, 
    hash: str | None = None, 
    size_bytes: int | None = None
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
        (path, parent_path, kind, file_type, size_bytes, hash, last_modified, last_seen_run)
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