import os
import tempfile
import unittest

from tasklist import store


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "items.json")

    def tearDown(self):
        self.dir.cleanup()

    def test_add_and_save(self):
        items = store.add([], "Buy stamps")
        store.save(items, self.path)
        self.assertEqual(store.load(self.path)[0]["title"], "Buy stamps")

    def test_missing_file_is_empty_list(self):
        self.assertEqual(store.load(self.path), [])


if __name__ == "__main__":
    unittest.main()
