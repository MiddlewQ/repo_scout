import os
from typing import Any

from .tool_response import response_error, response_ok
from .file_type import file_ext_to_file_type

def create_file_info(entry: os.DirEntry, root: str) -> dict:
    stats = entry.stat(follow_symlinks=False)
    _, ext = os.path.splitext(entry.name)
    relative_path = os.path.relpath(entry.path, root)
    return {
        "path": relative_path,
        "size": stats.st_size,
        "last_modfied": stats.st_mtime,
        "hash": None,
        "type": file_ext_to_file_type(ext)
    }


def scan_repo(filepath: str, max_chars = 2000) -> dict[str, Any]:
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            content = f.read(max_chars)
            truncated = f.read(1) != ""
            meta = {
                "truncated": truncated,
                "max_chars": max_chars
            }
    except OSError as e:
        return response_error(error_type=f'{e}')

    return response_ok({"content": content}, meta=meta)


def scan_repo_h(filepath: str, max_chars = 2000):
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            content = f.read(max_chars)
            truncated = f.read(1) != ""
            meta = {
                "truncated": truncated,
                "max_chars": max_chars
            }
            return {"content": content}
    except OSError as e:
        pass

    pass