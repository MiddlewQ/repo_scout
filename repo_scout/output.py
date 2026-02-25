from typing import Any

def format_largest(files: list) -> None:
    # files: [(path, size_bytes), ...] sorted desc
    if not files:
        print("No files found.")
        return

    for i, file in enumerate(files, start=1):
        path = file[0]
        size_bytes = file[5]
        kib = size_bytes / 1024
        mib = kib / 1024
        if mib >= 1:
            size_str = f"{mib:.2f} MiB"
        elif kib >= 1:
            size_str = f"{kib:.1f} KiB"
        else:
            size_str = f"{size_bytes} B"

        print(f"[{i}] {size_str}  {path}")

def format_dupes(duplicate_files_by_hash):
    if not duplicate_files_by_hash:
        print("No duplicate files found.")
        return

    items = sorted(
        duplicate_files_by_hash.items(),
        key=lambda kv: (-len(kv[1]), kv[0]),
    )

    for i, (file_hash, paths) in enumerate(items, start=1):
        count = len(paths)
        print(f"[{i}] {count} files share hash {file_hash}")
        for path in paths:
            print(f"  - {path}")
        if i != len(items):
            print()  # blank line between groups
