from delete_and_copy import *
from markdown_extraction import *
from generate_page_function import generate_page
def main():
    copy_to_dest("static","public")
    generate_page("content/index.md","template.html","public/index.html")


if __name__ == "__main__":
    main()