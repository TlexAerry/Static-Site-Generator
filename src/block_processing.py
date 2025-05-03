
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")   
    blocks_to_return = []
    for block in blocks:
        if block == "":
            continue
        blocks_to_return.append(block.strip())
       
    return blocks_to_return
