import os, sqlite3

def init_db(db_path: str = ":memory", schema_dir: str = "./schema"):
    sql_files = [
        os.path.join(schema_dir)
        for name in os.listdir(schema_dir)
        if name.endswith("sql") and os.path.isfile(os.path.join(schema_dir, name))
    ]
    sql_files.sort()
    if not sql_files:
        raise FileNotFoundError(f"No .sql files found in {schema_dir}")
    
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        with conn:
            for path in sql_files:
                with open(path, "r", encoding="utf-8") as f:
                    conn.executescript(f.read())
    finally:
        conn.close()

def insert_file(conn):

    pass