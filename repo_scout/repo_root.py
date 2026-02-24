import os, pathspec

def find_repo_root(curr_dir: str | None = None) -> str | None:
    curr_dir = os.path.abspath(curr_dir or os.getcwd())

    while True:
        if os.path.isdir(os.path.join(curr_dir, ".git")) or os.path.isdir(os.path.join(curr_dir, ".repo_scout")):
            return curr_dir

        parent = os.path.dirname(curr_dir)
        if curr_dir == parent:
            return None
        curr_dir = parent


def resolve_repo_root(repo_arg: str | None = None):
    if repo_arg: 
        root = os.path.abspath(repo_arg)

        if not os.path.isdir(root):
            raise ValueError(f"--repo is not a directory: {root}")
        return root
    
    root = find_repo_root()
    if root is None:
        raise ValueError("Not inside a repo (no .git or .repo_scout found). Use --repo /path/to/repo")
    return root

def db_path_to_root(repo_root: str) -> str:
    return os.path.join(repo_root, ".repo_scout", "index.sqlite")

def load_gitignore(repo_root: str, gitignore_path: str | None = None, verbose: bool = False) -> set[str]:
    
    if gitignore_path is None:
        gitignore_path = os.path.join(repo_root, ".gitignore")

    if not os.path.exists(gitignore_path):
        if verbose:
            print("No gitignore found.")
        return set()

    ignore_list = set()
    try: 
        with open(gitignore_path, mode="r", encoding="utf-8")as f:
            content = f.read()
            for line in content.splitlines():
                ignore_list.add(line)                
    except OSError as e:
        print(e)
        raise

    return ignore_list