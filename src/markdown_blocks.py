from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "ulist"
    OLIST = "olist"
    
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks
    
def block_to_block_type(block):
    if block.startswith(
        (
            "# ",
            "## ",
            "### ",
            "#### ",
            "##### ",
            "###### ",
            )):
        return BlockType.HEADING
    if block.startswith(("```\n")) and block.endswith(("```")):
        return BlockType.CODE

    lines = block.split("\n")
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


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    result = []
    for block in markdown_blocks:
        result.append(block_to_html_node(block))
    return ParentNode("div", result, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    raise ValueError("invalid block type")
    

def text_to_children(text):
    nodes = text_to_textnodes(text)
    result = []
    for node in nodes:
        result.append(text_node_to_html_node(node))
    return result

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    nested_parent = ParentNode("code", [child])
    return ParentNode("pre", [nested_parent])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    children = text_to_children(" ".join(new_lines))
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)

def olist_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line.split(". ", 1)[1]
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)