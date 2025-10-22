import sys
from copy_files_recursively import copy_files_recursive

if len(sys.argv) != 3:
        print("Usage: python3 src/main.py <src_path> <dst_path>")
        sys.exit(1)
src_path = sys.argv[1]  # e.g., "static/"
dst_path = sys.argv[2]  # e.g., "public/"


def main(src_path, dst_path):

    print(f"Copying {src_path} files to {dst_path} directory...")
    copy_files_recursive(src_path, dst_path)
    
        


main(src_path, dst_path)