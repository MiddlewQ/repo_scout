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

## Future plans

- Make the CLI easier to run from anywhere (installable `repo-scout` command)
- Add more analysis commands (e.g. `changed`, `stats`, `search`)
- Add more output formats (e.g. JSON/CSV)