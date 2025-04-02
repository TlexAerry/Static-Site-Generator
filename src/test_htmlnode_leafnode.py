import unittest
from htmlnode import LeafNode

class TestHTMLLeafNode(unittest.TestCase):
    def test_values(self):
        # when accessing the values of a instance, do they match?
        node = LeafNode(
            "p", 
            "Hi, this is a paragraph etc....", 
            {
                "href": "https://www.google.com",
                "target": "_blank",
            })
        self.assertEqual(node.tag,"p")
        self.assertEqual(node.value,"Hi, this is a paragraph etc....")
        self.assertEqual(node.props,{'href': 'https://www.google.com', 'target': '_blank'})
    
    def test_default_values(self):
        #does the default behaviour work?
        node =LeafNode("hold","hold")
        self.assertEqual(node.props,None)

    def test_methods(self):
        #do the methods behave as expecetd?
        #__repr__
        repr_node = LeafNode("a",None, {"key":"value"})
        self.assertEqual(repr_node.__repr__(),"LeafNode(a, None, {'key': 'value'})")

        #to_html
        to_html_node1 = LeafNode(None,"content")
        self.assertEqual(to_html_node1.to_html(),"content")

        to_html_node2 = LeafNode("p","content")
        self.assertEqual(to_html_node2.to_html(),f"<p>content</p>")

if __name__ == "__main__":
    unittest.main()
