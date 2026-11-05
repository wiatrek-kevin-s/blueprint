"""Command-line interface."""
import sys

from tasklist import store


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage: tasklist add TITLE | list | done N")
        return 2
    command, rest = argv[0], argv[1:]
    items = store.load()
    if command == "add":
        store.add(items, " ".join(rest).strip())
        store.save(items)
        return 0
    if command == "list":
        for n, item in enumerate(store.open_items(items), 1):
            print(f"{n}. {item['title']}")
        return 0
    if command == "done":
        try:
            store.mark_done(items, int(rest[0]))
        except (IndexError, ValueError) as e:
            print(f"error: {e}")
            return 1
        store.save(items)
        return 0
    print(f"unknown command: {command}")
    return 2
