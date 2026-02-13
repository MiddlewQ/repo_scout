import os
from typing import Any
from .utils import file_ending_to_file_type

def create_file_info(entry: os.DirEntry):
    stats = entry.stat(follow_symlinks=False)
    _, ext = os.path.splitext(entry.name)

    return {
        "path": entry.path,
        "size": stats.st_size,
        "last_modfied": stats.st_mtime,
        "hash": None,
        "type": file_ending_to_file_type(ext)
    }

def fs_tree(curr_filepath: str,
            ignore: set[str],
            depth: int = 2):
    out: dict[str, Any] = {}
    if depth <= 0:
        return out
    try:
        with os.scandir(curr_filepath) as it:
            for entry in it:
                name = entry.name
                if entry.is_dir(follow_symlinks=False):
                    if name in ignore:
                        continue
                    out[name] = fs_tree(entry.path, ignore, depth - 1)
                elif entry.is_file(follow_symlinks=False):

                    out[name] = {"size": entry.stat(follow_symlinks=False).st_size}
    except OSError as e:
        out["__error__"] = f"{type(e).__name__}: {e}"
    return out