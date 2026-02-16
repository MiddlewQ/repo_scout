import os, sqlite3

def get_nodes(conn: sqlite3.Connection):
    return conn.execute("SELECT * FROM nodes ORDER BY path").fetchall()

def walk_and_insert(conn: sqlite3.Connection, filesystem: dict, last_seen_run: int, parent_path: str | None = None):        
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
            last_seen_run=last_seen_run,
            size_bytes=node["size_bytes"],
        )
        if node["kind"] == "dir":
            walk_and_insert(conn=conn, 
                            filesystem=node.get("children", {}), 
                            parent_path=node["path"], 
                            last_seen_run=last_seen_run)

def insert_node(conn: sqlite3.Connection, path, parent_path, kind, file_type, last_modified, last_seen_run, size_bytes = None):
    conn.execute(
        """
        INSERT INTO nodes(path, parent_path, kind, file_type, size_bytes, last_modified, last_seen_run) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(path) DO UPDATE SET
            parent_path   = excluded.parent_path,
            kind          = excluded.kind,
            file_type     = excluded.file_type,
            size_bytes    = excluded.size_bytes,
            last_modified = excluded.last_modified,
            last_seen_run = excluded.last_seen_run
        """,
        (path, parent_path, kind, file_type, size_bytes, last_modified, last_seen_run)
    )




