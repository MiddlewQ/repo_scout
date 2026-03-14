import os
from typing import Iterator, Literal

from repo_scout.database.model import Node
from .model import ScanNode, os_entry_to_scannode
from .config import *

def walk_repo(
    repo_root: str,
    curr_dir: str,
    ignore: set[str] | None,
    depth: int | None = None
) -> Iterator[ScanNode]:
    if depth is not None and depth <= 0:
        return

    if ignore is None:
        ignore = set(DEFAULT_IGNORE_NAMES)
    else:
        ignore |= DEFAULT_IGNORE_NAMES

    yield from walk_repo_helper(repo_root, repo_root, ignore, depth)    


def walk_repo_helper(
    repo_root: str,
    curr_dir: str,
    ignore: set[str],
    depth: int | None 
) -> Iterator[ScanNode]:
    if depth is not None and depth <= 0:
        return

    with os.scandir(curr_dir) as entries:
        for entry in entries:
            if entry.name in ignore:
                continue
            node  = os_entry_to_scannode(entry, repo_root)
            yield node

            if entry.is_dir(follow_symlinks=False):
                next_depth = None if depth is None else depth - 1
                yield from walk_repo_helper(repo_root, entry.path, ignore, next_depth)

def scannode_to_node(scan_node: ScanNode, scan_id: int) -> Node:
    return Node(
        path=scan_node.path,
        parent_path=scan_node.parent_path if scan_node.parent_path is not None else "",
        kind=scan_node.kind,
        hash_content=scan_node.content_hash,
        file_type=scan_node.file_type,
        size_bytes=scan_node.size_bytes,
        last_modified=scan_node.last_modified if scan_node.last_modified is not None else 0.0,
        deleted=False,
        last_seen_run=scan_id
    )

