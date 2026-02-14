import json

from repo_scout.scan.scan_repo import fs_tree

print(json.dumps(fs_tree(".", ignore=set(["__pycache__", ".git", ".venv"]), depth=5), default=str,indent=4))
