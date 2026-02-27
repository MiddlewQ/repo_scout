import os

from repo_scout.repo_root import resolve_repo_root, db_path_to_root
from repo_scout.database.nodes import hash_dupes, filepaths_by_hash
from repo_scout.database.init_db import init_db

def run_dupes(repo: str, ignore: set[str] | None = None, include_empty: bool = False, verbose: bool = False):
    repo_root = resolve_repo_root(repo)
    if verbose:
        print(f"Repo root: {repo_root}")
    
    db_path = db_path_to_root(repo_root)
    if not os.path.exists(db_path):
        raise RuntimeError("could not find database")

    conn = init_db(db_path)
    try:
        duplicate_hash_counts = hash_dupes(conn, ignore, include_empty)
        if verbose:
            print(f"Found {len(duplicate_hash_counts)} duplicate hash(es)")

        duplicate_files_by_hash = {
            d.hash: filepaths_by_hash(conn, d.hash)
            for d in duplicate_hash_counts
        }

    except Exception as e:
        print(e)
        raise
    finally:
        conn.close()

    return duplicate_files_by_hash


