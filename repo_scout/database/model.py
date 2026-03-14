import sqlite3
from dataclasses import dataclass

from repo_scout.scan.model import ScanNode

@dataclass(frozen=True, slots=True)
class Node:
    path: str
    parent_path: str
    kind: str
    
    hash_content: str | None
    file_type: str | None
    size_bytes: int | None
    last_modified: float
    
    deleted: bool
    last_seen_run: int

def row_to_node(row: sqlite3.Row) -> Node:
    return Node(
        path=row["path"],
        parent_path=row["parent_path"],
        kind=row["kind"],

        hash_content=row["hash"],
        file_type=row["file_type"],
        size_bytes=row["size_bytes"],
        last_modified=row["last_modified"],

        deleted=row["deleted"],
        last_seen_run=row["last_seen_run"]
    )

@dataclass(frozen=True)
class FileNode:
    path: str
    parent_path: str

    hash: str
    size_bytes: int
    file_type: str | None
    last_modified: float
    
    deleted: bool 
    last_seen_run: int

def row_to_filenode(row: sqlite3.Row) -> FileNode:
    return FileNode(
        path=row["path"],
        parent_path=row["parent_path"],
        
        hash=row["hash"],
        file_type=row["file_type"],
        size_bytes=row["size_bytes"],
        last_modified=row["last_modified"],

        deleted=row["deleted"],
        last_seen_run=row["last_seen_run"]
    )

@dataclass(frozen=True)
class ModifiedFileNode:
    path: str
    old_size: int
    new_size: int
    old_hash: str
    new_hash: str
    old_mtime: float
    new_mtime: float

def row_to_modified_filenode(old_row: sqlite3.Row, new_row: sqlite3.Row):
    return ModifiedFileNode(
        path=new_row["path"],
        old_size=old_row["size_bytes"],
        new_size=new_row["size_bytes"],
        old_hash=old_row["hash"],
        new_hash=new_row["hash"],
        old_mtime=old_row["last_modified"],
        new_mtime=new_row["last_modified"]
    )

@dataclass(frozen=True, slots=True)
class HashDupe:
    hash: str
    count: int

def row_to_hash_dupe(row: sqlite3.Row) -> HashDupe:
    return HashDupe(hash=row["hash"], count=row["c"])

