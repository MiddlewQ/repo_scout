import argparse, os, sys
from typing import Any


from .repo_root import *
from .database.nodes import *
from .commands.scan import run_scan
from .commands.largest import run_largest

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

    add_scan_subcommand(subparsers)
    add_largest_subcommand(subparsers)
    add_changed_subcommand(subparsers)
    add_duped_subcommand(subparsers)

    return parser

def add_scan_subcommand(subparsers):
    p = subparsers.add_parser("scan", help="Scan repository for files to store in database")
    p.add_argument("--depth", type=int, default=None, help="Limits the depth of the file search in the repository")
    p.add_argument("--ignore", type=list, default=[], help="Directories ignored by the repository scout") 
    p.set_defaults(func=handle_scan)

def handle_scan(args):
    return run_scan(
        repo=args.repo,
        ignore=set(args.ignore),
        depth=args.depth,
        verbose=args.verbose 
    )
def add_largest_subcommand(subparsers):
    p = subparsers.add_parser("largest", help="Gives information about the largest file in the filesystem")
    p.add_argument("--ignore", type=lambda s: s.split("|"))
    p.add_argument("-n", "--count", type=int, default=1, help="How many files you want to return")
    # p.set_defaults(func=)

def handle_largest(args):
    
    return run_largest(
        repo=args.repo,
        scan_id=args.scan_id,
        file_count=args.file_count,
        ignore=set(args.ignore),
        depth=None,
        verbose=args.verbose
    )

def add_changed_subcommand(subparsers):
    p = subparsers.add_parser("changed", help="Tell you which files have changed since the last scan")
    p.add_argument("--ignore", type=lambda s: s.split("|"))
    # p.set_defaults(func=)

def add_duped_subcommand(subparsers):
    p = subparsers.add_parser("duped", help="Gives information about which files share duplicate hashes")
    p.add_argument("--ignore", type=lambda s: s.split("|"))
    # p.set_defaults(func=)

def add_clear_subcommand(subparsers):
    p = subparsers.add_parser("clear", help="Clear old scans from the database.")
    p.add_argument("--before", type=float)
    # p.set_defaults(func=)

# def main():

#     parser = init_parser()
#     args = parser.parse_args()

#     if args.verbose:
#         print(args)

#     if args.command is None:
#         parser.print_help()
#         sys.exit(0)

#     elif args.command == "scan":
#         scan_id = run_scan(
#             repo=args.repo,
#             ignore=set(args.ignore),
#             depth=args.depth,
#             verbose=args.verbose 
#         )

#     elif args.command == "changed":
#         # TODO: implement
#         pass
#     elif args.command == "largest":
#         # TODO: Implement
#         pass
#     elif args.command == "duped":
#         # TODO: Implement
#         pass
#     else:
#         print("Unexpected command, try again.")

