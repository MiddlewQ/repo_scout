import sqlite3

from repo_scout.repo_root import resolve_repo_root, db_path_to_root
from repo_scout.database.nodes import hash_dupes, filepaths_by_hash
from repo_scout.database.init_db import init_db

def run_changed(
    repo: str, 
    ignore: set[str] | None = None,
    verbose: bool = False
) -> tuple[list, list, list]:
    repo_root = resolve_repo_root(repo)

    db_path = db_path_to_root(repo_root)    

    conn = init_db(db_path)
    try:
        pass
    finally:
        conn.close()

    return ([], [], [])