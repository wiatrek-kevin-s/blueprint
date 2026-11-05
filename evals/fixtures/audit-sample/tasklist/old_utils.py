"""Helpers from the first version."""


def format_line(item):
    mark = "x" if item.get("done") else " "
    return f"[{mark}] {item['title']}"


def count_open(items):
    return sum(1 for item in items if not item.get("done"))
