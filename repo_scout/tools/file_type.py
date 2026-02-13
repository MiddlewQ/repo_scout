from enum import Enum

class FileType(Enum):
    Python = "python"
    Javascript = "js"
    C = "C"
    Cpp = "C++"
    SQLite = "sql"
    Rust = "rust"
    Toml = "toml"
    Json = "json"
    Makefile = "makefile"
    Unknown = ""

def file_ext_to_file_type(file_ending):
    match file_ending:
        case "py":
            return FileType.Python
        case "js":
            return FileType.Javascript
        case "c" | "h":
            return FileType.C
        case "cc" | "cpp" | "cxx" | ".C" | "hh" | "hpp" | "hxx" | "H": 
            return FileType.Cpp
        case "sql":
            return FileType.SQLite
        case "rs":
            return FileType.Rust
        case "toml":
            return FileType.Toml
        case "json":
            return FileType.Json
        case _:
            return FileType.Unknown

    