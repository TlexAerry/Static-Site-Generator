import unittest
from htmlnode import LeafNode,ParentNode

class TestHTMLParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("span", "hi")
        child_node2 = LeafNode(None, "ew, no tag?")
        child_node3 = LeafNode("pppp","this is a super ppppp")
        parent_node = ParentNode("div", [child_node1,child_node2,child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>hi</span>ew, no tag?<pppp>this is a super ppppp</pppp></div>"
        )

    def test_to_html_multiple_children2(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_for_tree(self):
        top_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("p2", 
                           [
                               LeafNode("1","we're so tiny"),
                               LeafNode(None, "holding"),
                               LeafNode("2", "yeah it's really small now")

                            ]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(top_node.to_html(),"<p><b>Bold text</b><p2><1>we're so tiny</1>holding<2>yeah it's really small now</2></p2><i>italic text</i>Normal text</p>")

    def test_repr(self):
        node = ParentNode("tag",[LeafNode("inner_tag","value")])
        self.assertEqual(node.__repr__(),"ParentNode(tag, [LeafNode(inner_tag, value, None)], None)" )        

    def test_parent_to_html_with_props(self):
        node = ParentNode("a",[LeafNode("p2","texttext")],{"href": "https://www.website.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.website.com\"><p2>texttext</p2></a>")

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()