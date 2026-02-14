import os
from typing import Any

from .file_type import file_ext_to_file_type
from .tool_response import response_ok, response_error

def create_dir_info(entry: os.DirEntry, root: str) -> dict:
    relative_path = os.path.relpath(entry.path, root)
    return {
        "path": relative_path,
        "kind": "dir",
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
        "size": stats.st_size,
        "last_modified": stats.st_mtime,
        "hash": None,
        "file_type": file_ext_to_file_type(ext).value
    }

def fs_tree(root: str = ".",
            ignore: set[str] | None=None,
            depth: int = 2):
    if ignore is None:
        ignore = set()
    
    filesystem = fs_tree_helper(root, root, ignore, depth)
    meta = {
        "depth": depth,
        "ignore_list": ignore
    }
    return response_ok(filesystem)
    

def fs_tree_helper(curr: str,
            root: str,
            ignore: set[str],
            depth: int):
    out: dict[str, Any] = {}
    if depth <= 0:
        return out
    try:
        with os.scandir(curr) as it:
            for entry in it:
                name = entry.name
                if name in ignore:
                    continue
                if entry.is_dir(follow_symlinks=False):
                    out[name] = create_dir_info(entry, root)
                    out[name]["children"] = fs_tree_helper(entry.path, root, ignore, depth - 1)
                elif entry.is_file(follow_symlinks=False):
                    out[name] = create_file_info(entry, root)
    except OSError as e:
        out["__error__"] = f"{type(e).__name__}: {e}"
    return out