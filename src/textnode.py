from enum import Enum

class TextType(Enum):
    NormalText = "normal"
    BoldText = "bold"
    ItalicText = "italic"
    CodeText = "code"

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
        return f"TextNode({self.text}, {self.type.value}, {self.url})"

        