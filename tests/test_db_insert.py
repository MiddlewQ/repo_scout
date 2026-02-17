from repo_scout.database.init_db import init_db
from repo_scout.database.scan_runs import begin_scan_run
from repo_scout.database.nodes import walk_and_insert, nodes
from repo_scout.scan.scan_repo import fs_tree

filesystem = fs_tree(".", ignore=set(["__pycache__", ".git", ".venv"]))

conn = init_db()
try:
    with conn:
        run_id = begin_scan_run(conn)
        walk_and_insert(conn, filesystem, run_id)

    nodes = nodes(conn)
    print("Node data:")
    for row in nodes:
        print(row)
finally:
    conn.close()