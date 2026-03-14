import sqlite3

from repo_scout.repo_root import resolve_repo_root, db_path_to_root
from repo_scout.database.init_db import init_db
from repo_scout.database.scan_runs import begin_scan_run
from repo_scout.database.nodes import insert_node, file_count
from repo_scout.database.model import Node

from repo_scout.scan.scan_repo import walk_repo, scannode_to_node

def run_changed(
    repo: str, 
    ignore: set[str] | None = None,
    depth: bool | None = None,
    verbose: bool = False,
) -> tuple[list[Node], list[Node], list[Node]]:
    repo_root = resolve_repo_root(repo)


    nodes = walk_repo(repo_root, repo_root, ignore, depth)


    db_path = db_path_to_root(repo_root)    
    conn = init_db(db_path)
    try:
        # Scan file system
        scan_id = begin_scan_run(conn)
        for node in nodes:
            node = scannode_to_node(node, scan_id)
            insert_node(conn, node)
    
        if verbose:
            num_files = file_count(conn)
            print(f"Finished scan {scan_id}, Found {num_files} files.")

    finally:
        conn.close()

    return ([], [], [])