from importlib.resources import files
import os, sqlite3

def init_db(db_path: str = ":memory:") -> sqlite3.Connection:
    if db_path != ":memory:":
        parent = os.path.dirname(db_path)
        os.makedirs(parent, exist_ok=True)
    
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    
    schema_dir = files("repo_scout").joinpath("schema")


    sql_files = [
        entry
        for entry in schema_dir.iterdir()
        if entry.is_file() and entry.name.endswith(".sql")
    ]
    sql_files.sort(key=lambda entry: entry.name)

    if not sql_files:
        raise FileNotFoundError(f"No .sql files found in {schema_dir}")
    
    with conn:
        for sql_file in sql_files:
            conn.executescript(sql_file.read_text(encoding="utf-8"))
    return conn

