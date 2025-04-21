from textnode import TextNode, TextType
import re


def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.type != TextType.NormalText:
            new_nodes.append(old_node)
            continue
        extracted_text = old_node.text
        substrings = extracted_text.split(delimeter)
        if len(substrings) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(0,len(substrings)):
            if substrings[i] == "":
                continue
            if i%2 == 0:
                new_nodes.append(TextNode(substrings[i],TextType.NormalText))
            else:
                new_nodes.append(TextNode(substrings[i],text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall("!\\[(.*?)\\]\\((.*?)\\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall("(?<!\\!)\\[(.*?)\\]\\((.*?)\\)", text)
    return matches