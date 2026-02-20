import os
from enum import Enum

class FileType(Enum):
    PYTHON = "python"
    JAVASCRIPT = "js"
    C = "c"
    CPP = "cpp"
    SQLITE = "sql"
    RUST = "rust"
    TOML = "toml"
    JSON = "json"
    MAKEFILE = "makefile"
    MARKDOWN = "markdown"
    TEXT = "text"
    UNKNOWN = "other"

def detect_file_type(filename: str) -> str:
    lower = filename.lower()

    if lower == "makefile":
        return "makefile"
    if lower == "dockerfiler":
        return "dockerfile"

    _, ext = os.path.splitext(lower)
    return file_ext_to_file_type(ext).value

def file_ext_to_file_type(ext):
    ext = ext.lstrip(".").lower()
    match ext:
        case "py":
            return FileType.PYTHON
        case "js":
            return FileType.JAVASCRIPT
        case "c" | "h":
            return FileType.C
        case "cc" | "cpp" | "cxx" | "C" | "hh" | "hpp" | "hxx" | "H": 
            return FileType.CPP
        case "sql":
            return FileType.SQLITE
        case "rs":
            return FileType.RUST
        case "toml":
            return FileType.TOML
        case "json":
            return FileType.JSON
        case "md":
            return FileType.MARKDOWN
        case "txt":
            return FileType.TEXT
        case _:
            return FileType.UNKNOWN

    