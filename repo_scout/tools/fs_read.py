import os
from typing import Any

from .tool_response import response_error, response_ok

def fs_read(filepath: str, max_chars = 2000) -> dict[str, Any]:
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

def fs_read_help(filepath: str, max_chars = 2000):
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