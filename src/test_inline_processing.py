import unittest
from inline_processing import *
from textnode import TextType

class TestHTMLNode(unittest.TestCase):
    def testcase1(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.NormalText)
        expected_output = [
            TextNode("This is text with a ", TextType.NormalText),
            TextNode("bolded phrase", TextType.BoldText),
            TextNode(" in the middle", TextType.NormalText)
            ]  
        self.assertEqual(expected_output, split_nodes_delimeter([node], "**", TextType.BoldText))

    def testcase2(self):
        node = TextNode("This is text with a `code block` word", TextType.NormalText)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CodeText)
        expected_output = [
            TextNode("This is text with a ", TextType.NormalText),
            TextNode("code block", TextType.CodeText),
            TextNode(" word", TextType.NormalText)
                ]
        self.assertEqual(expected_output, new_nodes)

    def test_delim_bold(self):
            node = TextNode("This is text with a **bolded** word", TextType.NormalText)
            new_nodes = split_nodes_delimeter([node], "**", TextType.BoldText)
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.NormalText),
                    TextNode("bolded", TextType.BoldText),
                    TextNode(" word", TextType.NormalText)
                ],
                new_nodes,
            )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.NormalText
        )
        new_nodes = split_nodes_delimeter([node], "**", TextType.BoldText)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NormalText),
                TextNode("bolded", TextType.BoldText),
                TextNode(" word and ", TextType.NormalText),
                TextNode("another", TextType.BoldText)
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NormalText
        )
        new_nodes = split_nodes_delimeter([node], "**", TextType.BoldText)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NormalText),
                TextNode("bolded word", TextType.BoldText),
                TextNode(" and ", TextType.NormalText),
                TextNode("another", TextType.BoldText)
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.NormalText)
        new_nodes = split_nodes_delimeter([node], "_", TextType.ItalicText)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NormalText),
                TextNode("italic", TextType.ItalicText),
                TextNode(" word", TextType.NormalText)
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.NormalText)
        new_nodes = split_nodes_delimeter([node], "**", TextType.BoldText)
        new_nodes = split_nodes_delimeter(new_nodes, "_", TextType.ItalicText)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BoldText),
                TextNode(" and ", TextType.NormalText),
                TextNode("italic", TextType.ItalicText)
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NormalText)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CodeText)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NormalText),
                TextNode("code block", TextType.CodeText),
                TextNode(" word", TextType.NormalText)
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()


