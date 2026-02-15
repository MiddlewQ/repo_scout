import os, sqlite3

def init_db(db_path: str = ":memory:", schema_dir: str = "./schema") -> sqlite3.Connection:
    sql_files = [
        os.path.join(schema_dir, name)
        for name in os.listdir(schema_dir)
        if name.endswith("sql") and os.path.isfile(os.path.join(schema_dir, name))
    ]
    sql_files.sort()
    if not sql_files:
        raise FileNotFoundError(f"No .sql files found in {schema_dir}")
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    with conn:
        for path in sql_files:
            with open(path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
    return conn

def walk_and_insert(conn: sqlite3.Connection, tree: dict, parent_path: str | None = None, last_seen_run = 1):        
    for name, node in tree.items():
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
                            tree=node.get("children", {}), 
                            parent_path=node["path"], 
                            last_seen_run=last_seen_run)


def insert_node(conn: sqlite3.Connection, path, parent_path, kind, file_type, last_modified, last_seen_run, *, size_bytes = None):
    conn.execute(
        """
        INSERT OR REPLACE INTO nodes(path, parent_path, kind, file_type, size_bytes, last_modified, last_seen_run) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (path, parent_path, kind, file_type, size_bytes, last_modified, last_seen_run)
    )

    conn.commit()



