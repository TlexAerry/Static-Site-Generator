import unittest
from markdown_extraction import *


class TestHeaderExtraction(unittest.TestCase):
    def test_case1(self):
        a = "# Hello"
        self.assertEqual("Hello", extract_header(a))

    def test_case2(self):
        a = "## Hello"
        with self.assertRaises(Exception):
             extract_header(a)

    def test_case3(self):
        a = " # Hello"
        with self.assertRaises(Exception):
             extract_header(a)

    def test_case4(self):
        a = ""
        with self.assertRaises(Exception):
            extract_header(a)


if __name__ == "__main__":
    unittest.main()