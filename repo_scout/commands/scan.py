from repo_scout.repo_root import *
from repo_scout.database.init_db import init_db
from repo_scout.database.nodes import walk_and_insert, file_count, mark_unseen_nodes_deleted
from repo_scout.database.scan_runs import begin_scan_run
from repo_scout.scan.scan_repo import fs_tree

def run_scan(*, repo: str | None, ignore: set[str], depth: int | None, verbose: bool) -> int:
    repo_root = resolve_repo_root(repo)
    if verbose:
        print(f"Repo root: {repo_root}")

    filesystem = fs_tree(repo_root, ignore, depth)

    db_path = db_path_to_root(repo_root)
    conn = init_db(db_path)
    try: 
        scan_id = begin_scan_run(conn)
        walk_and_insert(conn, filesystem, scan_id)
        mark_unseen_nodes_deleted(conn, scan_id)

        conn.commit()

        if verbose:
            num_files = file_count(conn)
            print(f"Finished scan {scan_id}, Found {num_files} files.")
        return scan_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()