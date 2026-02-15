from repo_scout.database.db import init_db, walk_and_insert
from repo_scout.scan.scan_repo import fs_tree

conn = init_db()

tree = fs_tree(".", ignore=set(["__pycache__", ".git", ".venv"]))

walk_and_insert(conn, tree)

cursor = conn.cursor()
cursor.execute("SELECT * FROM nodes")

output = cursor.fetchall()
print("Node data:")
for row in output:
    print(row)

conn.commit()
conn.close()