import os
from typing import Any

from .file_type import file_ext_to_file_type
from .tool_response import response_ok, response_error

def create_dir_info(entry: os.DirEntry, root: str) -> dict:
    stats = entry.stat(follow_symlinks=False)
    relative_path = os.path.relpath(entry.path, root)
    return {
        "path": relative_path,
        "kind": "dir",
        "file_type": None,
        "size_bytes": None,
        "hash": None,
        "last_modified": stats.st_mtime,
    }

def create_file_info(entry: os.DirEntry, root: str) -> dict:
    stats = entry.stat(follow_symlinks=False)
    file_name, ext = os.path.splitext(entry.name)
    if ext == '':
        ext = file_name
    relative_path = os.path.relpath(entry.path, root)
    return {
        "path": relative_path,
        "kind": "file",
        "file_type": file_ext_to_file_type(ext).value,
        "size_bytes": stats.st_size,
        "hash": None,
        "last_modified": stats.st_mtime,
    }

def scan_repo(root, ignore, depth):
    return

def fs_tree(root: str = ".",
            ignore: set[str] | None=None,
            depth: int | None = None):
    if ignore is None:
        ignore = set()

    filesystem = fs_tree_helper(root, root, ignore, depth)
    return filesystem
    

def fs_tree_helper(curr: str,
            root: str,
            ignore: set[str],
            depth: int | None):
    out: dict[str, Any] = {}
    if depth is not None and depth <= 0:
        return out
    try:
        with os.scandir(curr) as it:
            for entry in it:
                name = entry.name
                if name in ignore:
                    continue
                if entry.is_dir(follow_symlinks=False):
                    out[name] = create_dir_info(entry, root)
                    next_depth = None if depth is None else depth - 1
                    out[name]["children"] = fs_tree_helper(entry.path, root, ignore, next_depth)
                elif entry.is_file(follow_symlinks=False):
                    out[name] = create_file_info(entry, root)
    except OSError as e:
        out["__error__"] = f"{type(e).__name__}: {e}"
    return out