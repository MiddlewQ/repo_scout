from repo_scout.repo_root import *
from repo_scout.database.init_db import init_db
from repo_scout.database.nodes import file_count, insert_or_update_node, mark_unseen_nodes_deleted
from repo_scout.database.scan_runs import begin_scan_run
from repo_scout.scan.scan_repo import walk_repo, scannode_to_node

def run_scan(*, repo: str | None, ignore: set[str], depth: int | None, verbose: bool) -> int:
    repo_root = resolve_repo_root(repo)
    if verbose:
        print(f"Repo root: {repo_root}")

    nodes = walk_repo(repo_root, ignore, depth)

    db_path = db_path_to_root(repo_root)
    conn = init_db(db_path)
    try: 
        scan_id = begin_scan_run(conn)
        for node in nodes:
            node = scannode_to_node(node, scan_id)
            insert_or_update_node(conn, node)
        mark_unseen_nodes_deleted(conn, scan_id)

        if verbose:
            num_files = file_count(conn)
            print(f"Finished scan {scan_id}, Found {num_files} files.")

        conn.commit()

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    
    return scan_id