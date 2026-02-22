from typing import Any


def format_largest(files: list):
    rank_width = 4
    size_width = 8
    path_width = 40
    line_width = rank_width + 1 + size_width + path_width

    print("=" * line_width)
    print(f"{'Rank':>{rank_width}} {'Size':>{size_width}}   Path")
    print("=" * line_width)

    for i, file in enumerate(files):
        kb = int(file[5]) / 1000
        path = file[0]
        size_str = f"{kb:.2f} KB"

        print(f"{i+1:>{rank_width}} {size_str:>{size_width}}   {path}")

def format_dupes(duplicate_hashes: list):
    if not duplicate_hashes:
        print("No duplicate files found.")
        return

    count_width = 5
    hash_width = 64
    line_width = count_width + 1 + hash_width

    print(f"{'Count':>{count_width}} {'Hash':<{hash_width}}")
    print("=" * line_width)

    for file_hash, count in duplicate_hashes:
        print(f"{count:>{count_width}} {file_hash:<{hash_width}}")