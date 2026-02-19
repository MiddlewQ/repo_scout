# This file contains functions that hash file content, depending on the operating system. 
import os, hashlib

from .file_type import file_ext_to_file_type

def hash_file_content(filepath, chunk_size = 10000):
    h = hashlib.sha256()
    try:
        with open(filepath, mode="rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError as e:
        
        return None
    

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
        "hash": hash_file_content(relative_path),
        "last_modified": stats.st_mtime,
    }