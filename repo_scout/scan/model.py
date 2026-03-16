import os
from dataclasses import dataclass
from typing import Literal

from .file_type import detect_file_type
from .hash_content import hash_file_content


@dataclass(frozen=True, slots=True)
class ScanNode:
    path: str
    parent_path: str | None
    kind: Literal["file", "dir"]
    file_type: str | None
    size_bytes: int | None
    last_modified: float | None
    content_hash: str | None

def os_entry_to_scannode(entry: os.DirEntry, root: str, hash_content: bool = False) -> ScanNode:
    stats = entry.stat(follow_symlinks=False)
    relative_path = os.path.relpath(entry.path, root)
    parent_path = os.path.dirname(relative_path)
    last_modified = stats.st_mtime
    if not parent_path:
        parent_path = None

    is_file = entry.is_file(follow_symlinks=False)
    kind = "file" if is_file else "dir"

    file_type = None
    size_bytes = None
    content_hash = None
    if is_file:
        file_type = detect_file_type(entry.name)
        if hash_content:
            content_hash = hash_file_content(entry.path)
        size_bytes = stats.st_size

    return ScanNode(
        path=relative_path, 
        parent_path=parent_path,
        kind=kind, 
        file_type=file_type, 
        size_bytes=size_bytes, 
        last_modified=last_modified, 
        content_hash=content_hash
    )

