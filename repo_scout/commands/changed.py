from dataclasses import dataclass
from typing import Literal

from repo_scout.repo_root import resolve_repo_root, db_path_to_root
from repo_scout.database.init_db import init_db
from repo_scout.database.scan_runs import begin_scan_run
from repo_scout.database.nodes import insert_or_update_node, file_count, node_by_path, mark_unseen_nodes_deleted, has_previous_scan
from repo_scout.database.model import Node

from repo_scout.scan.scan_repo import walk_repo, scannode_to_node

@dataclass(slots=True)
class ChangedResult:
    baseline_created: bool
    created: list[Node]
    modified: list[Node]
    deleted: list[Node]

def run_changed(
    repo: str, 
    ignore: set[str] | None = None,
    depth: int | None = None,
    verbose: bool = False,
) -> ChangedResult:
    result = ChangedResult(
        baseline_created=False,
        created=[],
        modified=[],
        deleted=[]
    )

    repo_root = resolve_repo_root(repo)

    scannodes = walk_repo(repo_root, ignore, depth)

    db_path = db_path_to_root(repo_root)    
    conn = init_db(db_path)
    try:
        # Scan file system        
        had_previous_snapshot = has_previous_scan(conn)
        scan_id = begin_scan_run(conn)

        created: list[Node]  = []
        modified: list[Node] = []
        deleted: list[Node]  = []

        for node in scannodes:
            node = scannode_to_node(node, scan_id)

            if had_previous_snapshot:
                old_node = node_by_path(conn, node.path)

                # Created or re-created
                if old_node is None or old_node.deleted:
                    created.append(node)
                # Modified
                elif old_node.last_modified != node.last_modified:
                    modified.append(node)
            
            insert_or_update_node(conn, node)

        if had_previous_snapshot:
            deleted = mark_unseen_nodes_deleted(conn, scan_id)
        
        if verbose:
            num_files = file_count(conn)
            print(f"Finished scan {scan_id}, Found {num_files} files.")
        
        conn.commit()

        return ChangedResult(
            baseline_created=not had_previous_snapshot,
            created=created,
            modified=modified,
            deleted=deleted
        )

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()