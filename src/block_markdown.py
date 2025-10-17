import re
from enum import Enum
from inline_markdown import text_to_Text_nodes, split_nodes_image, split_nodes_link
from textnode import text_node_to_html_node, TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    parts = re.split(r"\n{2,}", markdown.strip())
    clean = [p.strip() for p in parts if p.strip()]
    return clean

def block_to_block_type(single_markdown_block: str) -> BlockType:
    if re.match(r"^#{1,6}\s", single_markdown_block):
        return BlockType.HEADING
    if single_markdown_block.startswith("```") and single_markdown_block.endswith("```"):
        return BlockType.CODE
    
    lines = single_markdown_block.splitlines()

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    parent = ParentNode(tag="div", children=[])
 
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            child = ParentNode("p", text_to_children(block.strip()))
        elif block_type == BlockType.HEADING:
            child = make_heading(block)
        elif block_type == BlockType.CODE:
            child = ParentNode("pre", make_code(block))
        elif block_type == BlockType.QUOTE:
            child = ParentNode("blockquote", text_to_children(block))
        elif block_type == BlockType.UNORDERED_LIST:
            child = LeafNode("ul", block)
        elif block_type == BlockType.ORDERED_LIST:
            child = LeafNode("ol", block)
        else:
            print("Unknown block type:", block_type)
            continue
        parent.children.append(child)
    return parent
    
def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_Text_nodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def make_heading(text: str) -> HTMLNode:
    m = re.match(r'^(\#+\s{1})(.*)', text)
    level = len(m.group(1).strip())
    if level > 6:
        raise ValueError("Too many leading '#' (max 6)")
    node = text_to_children(m.group(2).strip())
    return ParentNode(f"h{level}", node)

def make_code(text: str) -> HTMLNode:
    lines = text.splitlines(keepends=True)
    if len(lines) < 2:
        raise ValueError("not a fenced block")
    if not lines[0].startswith("```"):
        raise ValueError("missing opening fence")
    if not lines[-1].startswith("```"):
        raise ValueError("missing closing fence")
    first = lines[0]
    if first.strip() == "```":
        inner = lines[1:-1]
        node = "".join(inner)
    else:
        
        inline = first[first.find("```")+3:]
        node = "".join([inline] + lines[1:-1])
    code_child = LeafNode("code", node)
    return ParentNode("pre", [code_child])


def make_qoute(text):
    ...
    

def make_blockqoute(text):
    ...

def make_unordered_list(text):
    ...

def make_ordered_list(text):
    ...

print(make_qoute("```this is code,\n but\nthis is also code\n```"))
#print(make_qoute("```this is code, butthis is also code\n```"))