import re
from textnode import TextNode, TextType

def text_to_Text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


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


def _split_nodes_by_pattern(old_nodes, extractor, make_pattern, make_node):
    final_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_nodes.append(node)
            continue

        remaining = node.text
        for alt, url in extractor(remaining):
            parts = remaining.split(make_pattern(alt, url), 1)
            if len(parts) != 2:
                raise ValueError("invalid markdown, section not closed")
            left, right = parts
            if left:
                final_nodes.append(TextNode(left, TextType.TEXT))
            final_nodes.append(make_node(alt, url))
            remaining = right

        if remaining:
            final_nodes.append(TextNode(remaining, TextType.TEXT))
    return final_nodes


def split_nodes_image(old_nodes):
    return _split_nodes_by_pattern(
        old_nodes,
        extractor=extract_markdown_images,
        make_pattern=lambda alt, url: f"![{alt}]({url})",
        make_node=lambda alt, url: TextNode(alt, TextType.IMAGE, url),
    )


def split_nodes_link(old_nodes):
    return _split_nodes_by_pattern(
        old_nodes,
        extractor=extract_markdown_links,
        make_pattern=lambda alt, url: f"[{alt}]({url})",
        make_node=lambda alt, url: TextNode(alt, TextType.LINK, url),
    )




def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
