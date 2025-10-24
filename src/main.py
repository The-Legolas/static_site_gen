import sys
from copy_files_recursively import copy_files_recursive # comment this out if run as a script
#from .copy_files_recursively import copy_files_recursive # Un-comment this out if ran as a script using the main.sh file
from generating_content import generate_page

if len(sys.argv) != 6:
        print("Usage: python3 src/main.py <src_path> <dst_path> <from_path> <template_path> <dest_path>")
        sys.exit(1)
src_path = sys.argv[1]  # e.g., "static/"
dst_path = sys.argv[2]  # e.g., "public/"
from_path = sys.argv[3]  # e.g., "content/index.md" 
template_path = sys.argv[4]  # e.g., "template.html" 
dest_path = sys.argv[5]  # e.g., "public/index.html" 


def main(src_path, dst_path, from_path, template_path, dest_path):

    print(f"Copying {src_path} files to {dst_path} directory...")
    copy_files_recursive(src_path, dst_path)
    
    print("Generating page...")
    generate_page(from_path, template_path, dest_path)
   

if __name__ == "__main__":
    # default to static -> public if not provided
    src = sys.argv[1] if len(sys.argv) > 1 else "static"
    dst = sys.argv[2] if len(sys.argv) > 2 else "public"
    fro_path = sys.argv[3] if len(sys.argv) > 3 else "content/index.md"
    temp = sys.argv[4] if len(sys.argv) > 4 else "template.html"
    ds_path = sys.argv[5] if len(sys.argv) > 5 else "public/index.html"
    main(src, dst, fro_path, temp, ds_path)

