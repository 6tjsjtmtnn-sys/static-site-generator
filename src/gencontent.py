import os
from markdown_blocks import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    markdown_file = open(from_path, "r")
    markdown_content = markdown_file.read()
    markdown_file.close()
    
    template_file = open(template_path, "r")
    template_content = template_file.read()
    template_file.close()
    
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    
    html_title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", html_title)
    template_content = template_content.replace("{{ Content }}", html_string)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    dest_file = open(dest_path, "w")
    dest_file.write(template_content)
    dest_file.close()
    
    
def extract_title(md: str) -> str:
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")