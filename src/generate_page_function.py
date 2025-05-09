from block_processing import *
from markdown_extraction import *
import os
from delete_and_copy import *

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown_contents = markdown_file.read()
    template_file = open(template_path)
    template_contents = template_file.read()
    markdown_file.close()
    template_file.close()

    markdown_node = markdown_to_html_node(markdown_contents)
    html_string = markdown_node.to_html()
    title = extract_header(markdown_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}",html_string)
    
    directory_path = os.path.dirname(dest_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    with open(dest_path,"w") as f:
        f.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = find_file_paths(dir_path_content)
    pages = []
    for file in files:
        if os.path.isfile(file):
            pages.append(file)
    
    for page in pages:
        directory_old,file_name = os.path.split(page)
        
        directory_new = dest_dir_path + directory_old[7:]
        
        if not os.path.exists(directory_new):
             os.makedirs(directory_new)

        generate_page(page,template_path, directory_new+"/"+file_name[:-2]+"html")
    