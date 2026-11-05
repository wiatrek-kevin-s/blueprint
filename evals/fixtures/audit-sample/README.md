# tasklist

A tiny command-line to-do list. Items are kept in a JSON file in your home folder.

## Use

```bash
python3 -m tasklist add "Buy stamps"
python3 -m tasklist list
python3 -m tasklist done 1
python3 -m tasklist export tasks.csv
```

- `add` adds an item.
- `list` shows open items, numbered from 1.
- `done N` marks item N from the list as done.
- `export FILE` writes all items to a CSV file.

## Requirements

Python 3.9 or later. No other dependencies.

## Tests

```bash
python3 -m unittest discover -s tests
```

## Specification

See [SPEC.md](SPEC.md).

## Licence

MIT.
