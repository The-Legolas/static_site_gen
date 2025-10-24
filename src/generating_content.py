from block_markdown import markdown_to_html_node, markdown_to_blocks
import os

def generate_page(from_path, template_path, dest_path):
    # Getting the needed data
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        from_path_md_data = f.read()
    with open(template_path) as f:
        template_path_data = f.read()
    from_path_to_html = markdown_to_html_node(from_path_md_data).to_html()
    from_path_title = extract_title(from_path_md_data)
    
    # Replacing the title and content of the template file with the actual file content
    updated_template  = template_path_data.replace("{{ Title }}", from_path_title)
    updated_template  = updated_template.replace("{{ Content }}", from_path_to_html)
    
    # checking to see if the path exits and if not creeates it
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    # writes to the targetes file it correct file contents
    with open(dest_path, "w") as f:
        f.write(updated_template)

def extract_title(markdown):
    md_str = markdown_to_blocks(markdown)
    first_md_line = md_str[0]
    if not first_md_line.startswith("# "):
        raise Exception(f"This is incorrect formating. {first_md_line} should start with a single '#' and a leading space")
    stripped_md_str = first_md_line.strip("# ")
    return stripped_md_str