import os, tempfile

from repo_scout.repo_root import *

try:
    os.chdir("../")
    root = resolve_repo_root()
    print("resolve_repo_root(repo_scout/database) => ", root)
except Exception as e:
    print("resolve_repo_root() raised:", type(e).__name__, e)

# tests/test_repo_root.py

print("cwd before:", os.getcwd())
d = tempfile.mkdtemp()
print("temp dir:", d)
os.chdir(d)
print("cwd temp:", os.getcwd())
try:
    print("resolve_repo_root() =>", resolve_repo_root())
except Exception as e:
    print("resolve_repo_root() raised:", type(e).__name__, e)
print("resolve_repo_root(temp) =>", resolve_repo_root(d))