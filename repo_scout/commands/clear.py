import os

from repo_scout.database.nodes import clear_nodes
from repo_scout.repo_root import *
from repo_scout.database.init_db import init_db

def run_clear(repo: str, before: float | None = None, after: float | None = None, verbose: bool = False):
    repo_root = resolve_repo_root(repo)
    if verbose:
        print(f"Repo root: {repo_root}")
        print(f"Clearing database")
    
    db_path = db_path_to_root(repo_root)
    if not os.path.exists(db_path):
        raise RuntimeError("could not find database")


    conn = init_db(db_path)
    try:
        removed_total = clear_nodes(conn)
        if verbose:
            print(f"Deleted {removed_total} indexed files")
        
        conn.commit()

    except Exception as e:
        print(e)
        raise
    finally:
        conn.close()
