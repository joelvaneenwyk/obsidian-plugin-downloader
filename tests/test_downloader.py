# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from obsidian.utils.json import PLUGINS_JSON_FILE


class TestJsonUtilities(unittest.TestCase):

    def test_plugin_file(self):
        self.assertNotEqual(PLUGINS_JSON_FILE, '')


if __name__ == '__main__':
    unittest.main()
