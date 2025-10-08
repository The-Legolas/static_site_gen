from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise TypeError("Invalid text_type: must be a TextType enum value")
        else:
            self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
        if not isinstance(text_node.text_type, TextType):
            raise Exception("This is not a valid Text Type")
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        
        if text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)

        if text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        if text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)

        if text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})

        if text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
