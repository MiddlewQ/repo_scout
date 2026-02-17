import argparse, os, sys
from typing import Any


from .repo_root import *
from .database.init_db import init_db
from .database.nodes import *
from .database.scan_runs import *
from .scan.scan_repo import fs_tree

def ensure_repo_scout_dir(repo_root: str) -> str:
    dir = os.path.join(repo_root, ".repo_scout")
    os.makedirs(dir, exist_ok=True)
    return dir

def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Repo scout. Scans files in repository for analysis")
    parser.add_argument("--repo", type=str, default=None, help="Repository you want to create index for. Default search for repository root from current directory")
    parser.add_argument("--db", type=str, default=None, help="Database that stores previous scans of the repository. Default searches for database in repo_scout directory in root")
    parser.add_argument("--verbose", action="store_true", help="Enables verbose output")
    subparsers = parser.add_subparsers(dest="command", help="Commands help")

    scan_parser = subparsers.add_parser("scan", help="Scan repository for files to store in database")
    scan_parser.add_argument("--depth", type=int, default=None, help="Limits the depth of the file search in the repository")
    scan_parser.add_argument("--ignore", type=set, help="Directories ignored by the repository scout") 

    largest_parser = subparsers.add_parser("largest", help="Gives information about the largest file in the filesystem")
    changed_parser = subparsers.add_parser("changed", help="Tell you which files have changed since the last scan")
    duped_parser = subparsers.add_parser("duped", help="Gives information about which files share duplicate hashes")

    return parser


def scan_command(args):
    repo_root = resolve_repo_root(args.repo)
    if args.verbose:
        print(f"Repo root: {repo_root}")
    filesystem = fs_tree(repo_root, args.ignore, args.depth)

    db_path = db_path_to_root(repo_root)
    conn = init_db(db_path)
    try:
        scan_id = begin_scan_run(conn)
        walk_and_insert(conn, filesystem, scan_id)
        if args.verbose:
            num_nodes = file_count(conn)


            print(f"Finished scan {scan_id}. Found {num_nodes} files.")
    finally:
        conn.commit()
        conn.close()


def main():

    parser = init_parser()
    args = parser.parse_args()

    if args.verbose:
        print(args)
    
    if args.command == "scan":
        scan_command(args)

    elif args.command == "changed":
        # TODO: implement
        pass
    elif args.command == "largest":
        # TODO: Implement
        pass
    elif args.command == "duped":
        # TODO: Implement
        pass
    return 

    if args.verbose:
        print(args)
    try:
        repo_root = resolve_repo_root(args.repo)
        ensure_repo_scout_dir(repo_root)
        db_path = db_path_to_root(repo_root)
        filesystem=fs_tree(repo_root, ignore=args.ignore, depth=args.depth)
        
        conn = init_db(db_path)
        run_id = begin_scan_run(conn)
        walk_and_insert(conn, filesystem=filesystem, last_seen_run=run_id)
        output = nodes(conn),
        for row in output:
            print(row)
        
         
    except Exception as e: 
        print("Error raised:", type(e).__name__, e)
        sys.exit(1)
