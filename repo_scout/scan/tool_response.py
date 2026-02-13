from typing import Any


def response_ok(message: dict[str, Any], **meta):
    result = {
        "ok": True,
        "message": message
    }
    if meta:
        result["meta"] = meta
    return result

def response_error(error_type: str, result = None, **meta):
    return {
        "ok": False,
        "error_type": error_type,
    }
    