from enum import Enum

class FileType(Enum):
    Python = "python"
    Rust = "rust"
    Javascript = "js"
    C = "C"
    Cpp = "C++"
    Unknown = ""

def file_ending_to_file_type(file_ending):
    match file_ending:
        case "py":
            return FileType.Python
        case "js":
            return FileType.Javascript
        case "c" | "h":
            return FileType.C
        case "cc" | "cpp" | "cxx" | ".C" | "hh" | "hpp" | "hxx" | "H": 
            return FileType.Cpp
        case "rs":
            return FileType.Rust
        case _:
            return FileType.Unknown

    