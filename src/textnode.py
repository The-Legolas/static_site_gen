from enum import Enum

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
        if self.url is not None:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return f"TextNode({self.text}, {self.text_type.value})"