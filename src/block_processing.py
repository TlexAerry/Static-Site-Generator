from enum import Enum 
import re 
from htmlnode import *
from textnode import *
from inline_processing import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

#   Takes a block_type and return the html tag for that 
#   block type. The block is passed in only for headers 
#   to identify how many # are involved/
def block_type_to_tag(block_type, block = None):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            num = block[0:6].count("#") 
            return f"h{num}" 
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.ULIST:
            return "ul"
        case BlockType.OLIST:
            return "ol"
        case _:
            raise ValueError("Incorrect BlockType specified")

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")   
    blocks_to_return = []
    for block in blocks:
        if block == "":
            continue
        blocks_to_return.append(block.strip())
       
    return blocks_to_return

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH

def text_to_children(text):
    # takes a string and parses it into a 
    # list of text nodes, effectively handling 
    # inline markdown
    text_nodes = text_to_text_nodes(text)
    html_nodes = []

    #then we take each of those text nodes
    # and make them html nodes
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    #then we return a list of the child nodes
    #Which will sit within parent nodes
    return html_nodes

def get_code_content(text):
    #split text by \n
    lines = text.split("\n")
    #remove first line with ```
    lines = lines[1:] 
    #if lines not empty and if the final line is just the backticks sans whitespacee then    
    if lines and lines[-1].strip() == "```":
        #remove last line
        lines = lines[:-1]
    #join all the code lines now and return it
    content =  "\n".join(lines)
    return content+"\n"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    global_parent = ParentNode("div", [])
    for block in blocks:
        html_node = block_to_html_node(block)
        global_parent.children.append(html_node)
    return global_parent

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    raise ValueError("Wrong block type :( ")


#~~~~~~~~~~~~~~~~ Helper Functions for block_to_html_node(block) function
def paragraph_to_html_node(block):
    text = block
    lines = text.split("\n")
    new_text = " ".join(lines)
    #processes the  inline markdown
    children = text_to_children(new_text) 
    parent = ParentNode("p",children)
    return parent
    
def heading_to_html_node(block):
    number_of_hts = 0
    testing_text = block
    while number_of_hts < 6:
        if testing_text[0] == "#":
            number_of_hts += 1
            testing_text = testing_text[1:]
        else: #it's hit a space or text
            break

    tag = f"h{number_of_hts}"
    text = block.lstrip("#")
    text = text.lstrip()
    children = text_to_children(text)
    return ParentNode(tag, children)
 
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    #code_text = get_code_content(block)
    code_text = block[4:-3]
    raw_text_node = TextNode(code_text, TextType.TEXT)
    child_node = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [child_node])
    return ParentNode("pre", [code_node])

def olist_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for i in range(0,len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            raise ValueError("Your ordered list is wrong")
        stripped_line = lines[i].lstrip(f"{i+1}. ")
        children = text_to_children(stripped_line)
        li_nodes.append(ParentNode("li",children))
    return ParentNode("ol",li_nodes)

def ulist_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        if line[0:2] != "- ":
            raise ValueError("Your unordered list is wrong")
        li_inline_nodes = text_to_children(line[2:])
        li_nodes.append(ParentNode("li",li_inline_nodes))
    return ParentNode("ul",li_nodes)

def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        if line[0] != ">":
            raise ValueError("Youre quote block is wrong")
        stripped_lines.append(line[2:])

    full_quote = " ".join(stripped_lines)
    children = text_to_children(full_quote)
    return ParentNode("blockquote", children)