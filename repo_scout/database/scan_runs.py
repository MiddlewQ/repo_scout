import sqlite3, time

from .nodes import walk_and_insert

def begin_scan_run(conn: sqlite3.Connection, timestamp: float | None = None) -> int:
    if timestamp is None:
        timestamp = time.time()
    cursor = conn.cursor()
    
    statement = "INSERT INTO scan_runs(started_at) VALUES (?)"

    cursor.execute(statement, (timestamp,))

    if cursor.lastrowid is None:
        raise sqlite3.DatabaseError("Error inserting start of run")
    return cursor.lastrowid

def finalize_scan_run(conn: sqlite3.Connection, scan_id: int):
    
    statement = """
    UPDATE nodes 
    SET deleted = 1 
    WHERE deleted = 0 
      AND last_seen_id <> ?
    """
    conn.execute(statement, (scan_id, ))


def get_runs(conn: sqlite3.Connection):
    return conn.execute("SELECT * from scan_runs ORDER BY id").fetchall() 