expect: 1 | <header row, separator, quoting, encoding, line endings>
expect: 1 | <section name>
Expected: NOT READY. Template placeholders that start with an HTML tag word, <header row, separator, quoting, encoding, line endings> and <section name>, are still placeholders; the real tags beside them, <label> and <input type="text" required>, are not. Run: python3 skill/scripts/check_kit.py evals/fixtures/check-placeholder-like-tag
