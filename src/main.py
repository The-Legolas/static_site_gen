import sys
import os
from copy_files_recursively import copy_files_recursive
from generating_content import generate_pages_recursive


# Get the directory of this script (root/src)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to root
root_dir = os.path.dirname(script_dir)

dir_path_static = os.path.join(root_dir, "static")
dir_path_public = os.path.join(root_dir, "docs")
dir_path_content = os.path.join(root_dir, "content")
template_path = os.path.join(root_dir, "template.html")
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"


def main():
    print(f"Copying {dir_path_static} files to {dir_path_public} directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    
    print("Generating page...")
    generate_pages_recursive(dir_path_content,
        template_path,
        dir_path_public,
        basepath)
  
if __name__ == "__main__":
    main()
