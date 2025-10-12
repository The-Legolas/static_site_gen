import re
from enum import Enum

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
