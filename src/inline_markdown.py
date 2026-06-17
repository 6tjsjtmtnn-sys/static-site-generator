from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    nodes_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            nodes_list.append(old_node)
        else:
            split_text = old_node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("invalid Markdown syntax")
            new_nodes = []
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i % 2 == 0:
                    new_node = TextNode(split_text[i], TextType.TEXT)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(split_text[i], text_type)
                    new_nodes.append(new_node)
            nodes_list.extend(new_nodes)
    return nodes_list

# Regex

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)