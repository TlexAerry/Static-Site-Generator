def extract_header(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[0:2] == "# ":
            return line[2:].strip()
        else:
            raise Exception("Markdown contains no header")