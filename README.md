# Repo Scout

Repo scout is a small CLI tool that scans a repository, builds a local SQLite index, and lets you run quick analysis commands like "largest files" and "duplicates files by hash content"

## Features

- `scan`: indexes files in a repo into a local SQLite database 
- `largest`: lists the largest files
- `dupes`: finds duplicates files by content hash 
- `clear`: empties current index database

## How it works


Repo Scout finds the repository root by searching upward for a marker (for example .git/).

It stores an index database at .repo_scout/index.sqlite inside the repo.

File duplicates are detected using a full content hash (SHA-256).

## Roadmap

1. Easier to run to from anywhere
2. More commands 
3. More output formats