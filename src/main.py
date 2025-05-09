from delete_and_copy import *
from markdown_extraction import *
from generate_page_function import *
import sys
def main():
    basepath = sys.argv[0]
    copy_to_dest("static","docs") 
    generate_pages_recursive("content","template.html", "docs",basepath)

    

if __name__ == "__main__":
    main()