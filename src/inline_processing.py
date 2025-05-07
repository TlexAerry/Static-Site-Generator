from textnode import TextNode, TextType
import re

#   This function will split a node or a series of nodes into a
#   new list of nodes and each of those nodes dependent on what
#   delimeter and is detected which determines what the text is 
#   i.e. if ** is detected then it will create a text node for 
#   some bold text and then two nodes, one for before the bold 
#   text and one for after the bold text.
def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.type != TextType.TEXT:
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
                new_nodes.append(TextNode(substrings[i],TextType.TEXT))
            else:
                new_nodes.append(TextNode(substrings[i],text_type))
    return new_nodes

#   Helper function to identify markdown images within text
def extract_markdown_images(text):
    matches = re.findall("!\\[(.*?)\\]\\((.*?)\\)", text)
    return matches 

#   Helper function to identify markdown links within text
def extract_markdown_links(text):
    matches = re.findall("(?<!\\!)\\[(.*?)\\]\\((.*?)\\)", text)
    return matches

#   This will take a list of nodes, and split them based on
#   identified images using above defined helper functions.
#   Then will return a list of TextNodes for the text before
#   the image, the image, and the text after the image.  
def split_nodes_image(old_nodes):
    return_list =[]
    for old_node in old_nodes:
        # may need to whack in a test to check if the node is normal
        # slash what nodes should this act on? 
        # I think if the node is not a normal text the we just add it to the new nodes
        extracted_text = old_node.text
        matches = extract_markdown_images(extracted_text)
        if len(matches) == 0:
            return_list.append(old_node)
            continue

        for text, url in matches:
            split_text = f"![{text}]({url})"
            extracted_text = extracted_text.split(f"{split_text}",1) #should always be a list of length 2
            if extracted_text[0] is not None and extracted_text[0] != "":
                return_list.append(TextNode(f"{extracted_text[0]}",TextType.TEXT))
            return_list.append(TextNode(f"{text}",TextType.IMAGE, f"{url}"))

            extracted_text = extracted_text[1]
            if extracted_text == "":
                break
            
        if extracted_text !="":
           return_list.append(TextNode(f"{extracted_text}", TextType.TEXT))   
        
    return return_list    


#   See split_nodes_image function for this function, they 
#   are equivalent but just use different helper functions. 
def split_nodes_link(old_nodes):
    return_list =[]
    for old_node in old_nodes:
        # may need to whack in a test to check if the node is normal
        # slash what nodes should this act on? 
        # I think if the node is not a normal text the we just add it to the new nodes
        extracted_text = old_node.text
        matches = extract_markdown_links(extracted_text)
        if len(matches) == 0:
            return_list.append(old_node)
            continue

        for text, url in matches:
            split_text = f"[{text}]({url})"
            extracted_text = extracted_text.split(f"{split_text}",1) #should always be a list of length 2
            if extracted_text[0] is not None and extracted_text[0] != "":
                return_list.append(TextNode(f"{extracted_text[0]}",TextType.TEXT))
            return_list.append(TextNode(f"{text}",TextType.LINK, f"{url}"))

            extracted_text = extracted_text[1]
            if extracted_text == "":
                break
            
        if extracted_text !="":
           return_list.append(TextNode(f"{extracted_text}", TextType.TEXT))   
        
    return return_list    

#   The jewel in the crown of this file. This takes a string, 
#   turns it into a text node, then splits it based on any 
#   images in that text, does the same for links. And then iterates
#   through potential delimeters for other text types, and builds
#   text nodes for that text. Will return a list of text nodes. 
def text_to_text_nodes(text):
    text_node = TextNode(text, TextType.TEXT)
    image_nodes = split_nodes_image([text_node])
    link_nodes = split_nodes_link(image_nodes)
    final_nodes = link_nodes
    delimeters_and_types = [
        ("**",TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    ]
    for delimeter, type in delimeters_and_types:
        final_nodes = split_nodes_delimeter(final_nodes, delimeter, type)    

    
    return final_nodes