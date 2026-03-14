import hashlib

def hash_file_content(filepath, chunk_size = 1000) -> str | None:
    h = hashlib.sha256()
    try:
        with open(filepath, mode="rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError as e:
        print(f"error: {e}")
        return None