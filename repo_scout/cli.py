import argparse, os

from .repo_root import *
from .database.nodes import *
from .commands.scan import run_scan
from .commands.largest import run_largest
from .commands.clear import run_clear
from .commands.dupes import run_dupes
from .commands.changed import run_changed
from .output import format_largest, format_dupes, format_changed

def ensure_repo_scout_dir(repo_root: str) -> str:
    dir = os.path.join(repo_root, ".repo_scout")
    os.makedirs(dir, exist_ok=True)
    return dir

def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Repo scout. Scans files in repository for analysis")
    parser.add_argument("--repo", type=str, default=None, help="Repository you want to create index for. Default search for repository root from current directory")
    parser.add_argument("--db", type=str, default=None, help="Database that stores previous scans of the repository. Default searches for database in repo_scout directory in root")
    parser.add_argument("--verbose", action="store_true", help="Enables verbose output")
    parser.add_argument("--debug", action="store_true", help="Debug prints")
    subparsers = parser.add_subparsers(dest="command", help="Commands help")

    add_scan_subcommand(subparsers)
    add_largest_subcommand(subparsers)
    add_changed_subcommand(subparsers)
    add_dupes_subcommand(subparsers)
    add_clear_subcommand(subparsers)

    return parser

def add_scan_subcommand(subparsers):
    p = subparsers.add_parser("scan", help="Scan repository for files to store in database")
    p.add_argument("--depth", type=int, default=None, help="Limits the depth of the file search in the repository")
    p.add_argument("--ignore", type=lambda s: s.split("|"), default=[])
    # p.add_argument("--ignore", type=list, default=[], help="Directories ignored by the repository scout") 
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
    p.add_argument("-I", "--ignore", nargs="+", default=[], metavar="PATTERN", help="Skip paths. Examples: cli.py utils/ pkg/__init__.py")
    p.add_argument("-n", "--limit", type=int, default=5, help="Limit number of files return, default: 5")
    p.add_argument("--json", action="store_true", help="Output Json instead or readable format")
    p.set_defaults(func=handle_largest)

def handle_largest(args):
    if args.debug:
        print(args.ignore)
    files = run_largest(
        repo=args.repo,
        file_count=args.limit,
        ignore=set(args.ignore),
        depth=None,
        verbose=args.verbose
    )
    format_largest(files)

def add_changed_subcommand(subparsers):
    p = subparsers.add_parser("changed", help="Scans repository, compares to previous state and gives information about which files have been created, updated or removed.")
    p.add_argument("-I", "--ignore", nargs="+", default=[], metavar="PATTERN", help="Skip paths. Examples: cli.py utils/ pkg/__init__.py")
    p.set_defaults(func=handle_changed)

def handle_changed(args):
    result = run_changed(
        repo=args.repo, 
        ignore=set(args.ignore),
        verbose=args.verbose
    )
    format_changed(result)


def add_dupes_subcommand(subparsers):
    p = subparsers.add_parser("dupes", help="Gives information about which files share duplicate hashes")
    p.add_argument("-I", "--ignore", nargs="+", default=[], metavar="PATTERN", help="Skip paths. Examples: cli.py utils/ pkg/__init__.py")
    p.add_argument("--include-empty", action="store_true")
    p.set_defaults(func=handle_dupes)

def handle_dupes(args):
    dupes = run_dupes(
        repo=args.repo,
        ignore=set(args.ignore),
        include_empty=args.include_empty,
        verbose=args.verbose
    )
    format_dupes(dupes)

def add_clear_subcommand(subparsers):
    p = subparsers.add_parser("clear", help="Clear old scans from the database.")
    p.add_argument("--before", type=float, default=None)
    p.add_argument("--after", type=float, default=None)
    p.set_defaults(func=handle_clear)

def handle_clear(args):
    return run_clear(
        repo=args.repo,
        before=args.before,
        after=args.after,
        verbose = args.verbose
    )
