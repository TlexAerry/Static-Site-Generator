import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BoldText)
        node2 = TextNode("This is a text node", TextType.BoldText)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BoldText)
        node2 = TextNode("This is a text node", TextType.NormalText)
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = TextNode("This is a text node", TextType.BoldText)
        node2 = TextNode("This is a text node", TextType.BoldText, "a.b@c.d")
        self.assertNotEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BoldText,None)
        node2 = TextNode("This is a text node", TextType.BoldText)
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.NormalText)
        node2 = TextNode("This is a text node", TextType.CodeText)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
