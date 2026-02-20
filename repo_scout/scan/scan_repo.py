import os
from typing import Any

from .scan_node import create_dir_info, create_file_info
from .config import *

def fs_tree(root: str = ".",
            ignore: set[str] | None=None,
            depth: int | None = None):
    if ignore is None:
        ignore = set(DEFAULT_IGNORE_NAMES)
    else:
        ignore |= DEFAULT_IGNORE_NAMES
    
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

# def fs_read(filepath: str, max_chars = 2000) -> dict[str, Any]:
#     try:
#         with open(filepath, mode="r", encoding="utf-8") as f:
#             content = f.read(max_chars)
#             truncated = f.read(1) != ""
#             meta = {
#                 "truncated": truncated,
#                 "max_chars": max_chars
#             }
#     except OSError as e:
#         return response_error(error_type=f'{e}')

#     return c

# def fs_read_help(filepath: str, max_chars = 2000):
#     try:
#         with open(filepath, mode="r", encoding="utf-8") as f:
#             content = f.read(max_chars)
#             truncated = f.read(1) != ""
#             meta = {
#                 "truncated": truncated,
#                 "max_chars": max_chars
#             }
#             return {"content": content}
#     except OSError as e:
#         pass

#     pass