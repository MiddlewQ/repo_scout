import sqlite3

from repo_scout.repo_root import resolve_repo_root, db_path_to_root
from repo_scout.database.nodes import hash_dupes, filepaths_by_hash
from repo_scout.database.init_db import init_db
from repo_scout.database.scan_runs import begin_scan_run
from repo_scout.scan.scan_repo import fs_tree

def run_changed(
    repo: str, 
    ignore: set[str] | None = None,
    verbose: bool = False
) -> tuple[list, list, list]:
    repo_root = resolve_repo_root(repo)

    filesystem = fs_tree(repo_root, ignore)


    db_path = db_path_to_root(repo_root)    
    conn = init_db(db_path)
    try:
        # Scan file system
        scan_id = begin_scan_run(conn)
        

        pass
    finally:
        conn.close()

    return ([], [], [])