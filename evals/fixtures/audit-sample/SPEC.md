# tasklist specification

Version 1.0 · 2026-09-01

## Requirements

- **R1. Add.** `add TITLE` stores a new open item. The title is trimmed; an empty title or one longer than 200 characters is refused with a message and nothing is stored.
- **R2. List.** `list` prints open items in the order they were added, numbered from 1.
- **R3. Done.** `done N` marks the item shown as number N by `list` as done. A number that isn't on the list is refused with a message.
- **R4. Export.** `export FILE` writes every item, open and done, to a UTF-8 CSV file with the header `title,done,created`.
- **R5. Storage.** Items live in `~/.tasklist.json`. If the file doesn't exist yet, the list is empty. Every save replaces the file in one step, so a crash never leaves half a file.

## Data format

```json
{"items": [{"title": "Buy stamps", "done": false, "created": "2026-09-01"}]}
```
