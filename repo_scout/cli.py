import argparse

from repo_root import resolve_repo_root

def main():
    parser = argparse.ArgumentParser(description="Repository Scout")
    parser.add_argument("-f", "--files", action="store_true")
    parser.add_argument("-l", "--level", nargs="?", type=int, const=4)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enables verbose output")
    args = parser.parse_args()
    print(args)


