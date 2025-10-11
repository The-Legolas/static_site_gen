import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue

        node_parts = node.text.split(delimiter)
        if len(node_parts) % 2 == 0:
            raise Exception(f"Unmatched delimiter {delimiter!r} in: {node.text!r}")
        
        for idx, part in enumerate(node_parts):
            if part == "":
                continue
            if idx % 2 == 0:
                final_nodes.append(TextNode(part, TextType.TEXT))
            else:
                final_nodes.append(TextNode(part, text_type))

    return final_nodes


def split_nodes_image(old_nodes):
    final_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue
        remaining = node.text
        for alt, link in extract_markdown_images(remaining):
            left, right = remaining.split(f"![{alt}]({link})", 1)
            if left:
                final_nodes.append(TextNode(left, TextType.TEXT))
            final_nodes.append(TextNode(alt, TextType.IMAGE, link))
            remaining = right
            
        if remaining:
            final_nodes.append(TextNode(remaining, TextType.TEXT))
    return final_nodes

def split_nodes_link(old_nodes):
    final_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue
        remaining = node.text
        for alt, link in extract_markdown_links(remaining):
            left, right = remaining.split(f"[{alt}]({link})", 1)
            if left:
                final_nodes.append(TextNode(left, TextType.TEXT))
            final_nodes.append(TextNode(alt, TextType.LINK , link))
            remaining = right
            
        if remaining:
            final_nodes.append(TextNode(remaining, TextType.TEXT))
    return final_nodes




def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)