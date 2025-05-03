import unittest
from block_processing import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_case1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
    )

    def test_case2(self):
        md = ""
        blocks = []
        self.assertEqual(blocks, markdown_to_blocks(md))

    def test_case3(self):
        md = "\n\n"
        blocks = []
        self.assertEqual(blocks, markdown_to_blocks(md))
    
    def test_case4(self):
        md = """
This is **bolded** paragraph






- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
                [
                    "This is **bolded** paragraph",
                    "- This is a list\n- with items",
                ],
    )

if __name__ == "__main__":
    unittest.main()