import json

from repo_scout.scan.scan_repo import fs_tree
tree = fs_tree(".", ignore=set(["__pycache__", ".git", ".venv"]), depth=2)

print(json.dumps(tree, default=str,indent=4))
# for name, node in tree.items():
    # print(f"name: {node["path"]}")