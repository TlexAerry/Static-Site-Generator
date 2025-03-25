import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_neq(self):
        HTMLnode = HTMLNode(tag="<a>",props="hi")
        HTMLnode2 = HTMLNode(value="<a>",props="hi")
        self.assertNotEqual(HTMLnode, HTMLnode2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# none neq none?
# need to figure this out
    def test_neq_nulls(self):
        HTMLnode = HTMLNode()
        HTMLnode2 = HTMLNode()
        self.assertNotEqual(HTMLnode, HTMLnode2)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_propsToHTML(self):
        test_dict = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                    }
        input = HTMLNode(props=test_dict)
        actual = input.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(actual, expected)


    
if __name__ == "__main__":
    unittest.main()
