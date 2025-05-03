import unittest
from inline_processing import *
from textnode import TextType

class TestHTMLNode(unittest.TestCase):
#~~~~~~~~~Initial Testing: 8 Test Cases
    def test_case1(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT)
            ]  
        self.assertEqual(expected_output, split_nodes_delimeter([node], "**", TextType.BOLD))

    def test_case2(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
        expected_output = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
                ]
        self.assertEqual(expected_output, new_nodes)

    def test_delim_bold(self):
            node = TextNode("This is text with a **bolded** word", TextType.TEXT)
            new_nodes = split_nodes_delimeter([node], "**", TextType.BOLD)
            self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded", TextType.BOLD),
                    TextNode(" word", TextType.TEXT)
                ],
                new_nodes,
            )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimeter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimeter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimeter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC)
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimeter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes,
        )

class TestExtractImagesandLinks(unittest.TestCase):
#~~~~~~~~~Testing extracting links and images: 8 Test Cases
    def test_extract_image1(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_image2(self):
        matches = extract_markdown_images(
            "This is text with no image)"
            )
        self.assertListEqual([], matches)
        
    def test_extract_image3(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
            )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_image4(self):
        matches = extract_markdown_images(
            "This is text with an ![text]()"
            )
        self.assertListEqual([("text", "")], matches)

    def test_extract_links1(self):
        matches = extract_markdown_links(
            "This is text with an image ![url](websiteisdmji)"
            )
        self.assertListEqual([], matches)

    def test_extract_links2(self):
        matches = extract_markdown_links(
            "This is text with an image [alt text1](websiteisdmji url)"
            )
        self.assertListEqual([("alt text1","websiteisdmji url")], matches)

    def test_extract_links3(self):
        matches = extract_markdown_links(
            "This is text with an image [](websiteisdmji)"
            )
        self.assertListEqual([("","websiteisdmji")], matches)

    def test_extract_links4(self):
        matches = extract_markdown_links(
            "This is text with an image [asdasd]()"
            )
        self.assertListEqual([("asdasd","")], matches)

class TestSplittingImagesandLinks(unittest.TestCase):
#~~~~~~~~~Testing for splitting images and links: 9 Test Cases 
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )        

    def test_split_no_images(self):
        node = TextNode(
            "This is text with no images and with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images and with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )        

    def test_split_no_links(self):
        node = TextNode(
            "This is text with no links and with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links and with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )        

    def test_mix_image_and_link(self):
        node = TextNode(
            "This is text with an image ![image](url) and a link [link](url) and with text that follows",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" and a link [link](url) and with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )  

    def test_mix_link_and_image(self):
        node = TextNode(
            "This is text with an image ![image](url) and a link [link](url) and with text that follows",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ![image](url) and a link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" and with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )  

class TestTextToTextNodes(unittest.TestCase):
#~~~~~~~~~Testing for text to text nodes: 3 Test Cases
    def test_text_to_text_node1(self):
        expected_list = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual_list = text_to_text_nodes(input)
        self.assertListEqual(expected_list, actual_list)

    def test_text_to_text_node2(self):
        expected_list = []
        input = ""
        actual_list = text_to_text_nodes(input)
        self.assertListEqual(expected_list, actual_list)

    def test_text_to_text_node3(self):
        expected_list = [
            TextNode("This is no bold text with no italic text and no code block", TextType.TEXT)
            ]
        input = "This is no bold text with no italic text and no code block"
        actual_list = text_to_text_nodes(input)
        self.assertListEqual(expected_list, actual_list)


if __name__ == "__main__":
    unittest.main()