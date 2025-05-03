from enum import Enum
from htmlnode import LeafNode
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text,type, url = None):
        self.text = text
        self.type = TextType(type)
        self.url = url

    def __eq__(self, TextNode):
        text_same = self.text == TextNode.text
        type_same = self.type == TextNode.type
        url_same = self.url == TextNode.url
        return text_same and type_same and url_same 

    def __repr__(self):
        return f"TextNode({repr(self.text)}, {self.type}, {repr(self.url)})"

def text_node_to_html_node(text_node):
    match text_node.type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img","", {"src":f"{text_node.url}","alt":f"{text_node.text}"})
        case _:
            raise ValueError(f"{text_node.type} text type is incorrect, please use one of the pre-defined values")