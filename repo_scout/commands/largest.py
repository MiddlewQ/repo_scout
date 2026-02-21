import os, sqlite3

from repo_scout.database.nodes import largest_files
from repo_scout.database.init_db import init_db
from repo_scout.repo_root import resolve_repo_root, db_path_to_root

def run_largest(*, repo: str | None, file_count: int, ignore: set[str] | None = None, depth: int | None = None, verbose: bool = False):
    

    repo_root = resolve_repo_root(repo)
    if verbose:
        print(f"Repo root: {repo_root}")

    # Exit if database doesn't exist yet
    db_path = db_path_to_root(repo_root)
    if not os.path.exists(db_path):
        raise RuntimeError("Could not find database")
    
    conn = init_db(db_path)
    try: 
        files = largest_files(conn, file_count) 

        if verbose: 
            print(f"Found {len(files)} files.")

        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

    print(files)
    