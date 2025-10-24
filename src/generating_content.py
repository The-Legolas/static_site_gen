from block_markdown import markdown_to_html_node, markdown_to_blocks
import os

def generate_page(from_path, template_path, dest_path, basepath, base_dir=None):
    # Getting the needed data
    # If base_dir is provided, show relative paths; otherwise, use basenames
    if base_dir:
        from_rel = os.path.relpath(from_path, base_dir)
        dest_rel = os.path.relpath(dest_path, base_dir)
        template_rel = os.path.relpath(template_path, base_dir)
        print(f"Generating page from {from_rel} to {dest_rel} using {template_rel}")
    else:
        print(f"Generating page from {os.path.basename(from_path)} to {os.path.basename(dest_path)} using {os.path.basename(template_path)}")
    
    #print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #print(f"Generating page from {os.path.basename(from_path)} to {os.path.basename(dest_path)} using {os.path.basename(template_path)}")
    with open(from_path) as f:
        from_path_md_data = f.read()
    with open(template_path) as f:
        template_path_data = f.read()
    from_path_to_html = markdown_to_html_node(from_path_md_data).to_html()
    from_path_title = extract_title(from_path_md_data)
    
    # Replacing the title and content of the template file with the actual file content
    updated_template  = template_path_data.replace("{{ Title }}", from_path_title)
    updated_template  = updated_template.replace("{{ Content }}", from_path_to_html)
    updated_template  = updated_template.replace('href="/', f'href="{basepath}')
    updated_template  = updated_template.replace('src="/', f'src="{basepath}')
    
    # checking to see if the path exits and if not creeates it
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    # writes to the targeted file's contents
    with open(dest_path, "w") as f:
        f.write(updated_template)

def extract_title(markdown):
    md_str = markdown_to_blocks(markdown)
    first_md_line = md_str[0]
    if not first_md_line.startswith("# "):
        raise Exception(f"This is incorrect formating. {first_md_line} should start with a single '#' and a leading space")
    stripped_md_str = first_md_line.strip("# ")
    return stripped_md_str


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath, max_depth=20, depth=0, visited=None):
    if visited is None:
        visited = set()
    if depth > max_depth:
        print(f"Max depth of {max_depth} reached at {os.path.basename(dir_path_content)}")
        return
    abs_path = os.path.abspath(dir_path_content)
    if abs_path in visited:
        print(f"Cycle detected at {os.path.basename(dir_path_content)}")
        return
    visited.add(abs_path)

    try:
        for entry in os.listdir(dir_path_content):
            dir_full_path = os.path.join(dir_path_content, entry) 
            dest_full_path = os.path.join(dest_dir_path, entry)
            try:
                if os.path.isfile(dir_full_path) and dir_full_path.endswith(".md"):
                    if entry == "index.md":
                        print(f" * Found markdown file: {entry} -> converting to html")
                        dest_html_path = os.path.join(dest_dir_path, "index.html")
                    else:
                        name = os.path.splitext(entry)[0]
                        print(f" * Found markdown file: {entry} -> converting to html")
                        dest_html_path = os.path.join(dest_dir_path, name + ".html")
                    generate_page(dir_full_path, template_path, dest_html_path, basepath, base_dir=dir_path_content)
                if os.path.isdir(dir_full_path):
                    os.makedirs(dest_full_path, exist_ok=True)
                    generate_pages_recursive(dir_full_path, template_path, dest_full_path, basepath, max_depth, depth + 1, visited)
            except Exception as e:
                print(f"Error processing {entry}: {e}")
                continue
    except Exception as e: 
        print(f"Error: {e}")
