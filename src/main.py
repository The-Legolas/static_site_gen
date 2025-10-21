import os
import shutil
import sys

if len(sys.argv) != 3:
        print("Usage: python3 src/main.py <src_path> <dst_path>")
        sys.exit(1)
src_path = sys.argv[1]  # e.g., "static/"
dst_path = sys.argv[2]  # e.g., "public/"


def main(src_path, dst_path):
    print(f"Source: {src_path}")
    print(f"Destination: {dst_path}")

    if os.path.exists(src_path):
        try:
            shutil.rmtree(dst_path)    #Only re-activate when project is ready
        except:
            os.makedirs("public")

        all_paths = process_directory(src_path, src_path)
        
        for relative_path in all_paths:
            print("Found file:", relative_path)
            src_full_path = os.path.join(src_path, relative_path) 
            # Build full destination path
            dst_full_path = os.path.join(dst_path, relative_path)  
            # Get the destination directory (parent of the file)
            dst_dir = os.path.dirname(dst_full_path)
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src_full_path, dst_full_path)

def process_directory(src_path, root_src_path):
    path = []
    if os.path.exists(src_path):
        for entry in os.listdir(src_path):
            full_path = os.path.join(src_path, entry)
            relative_path = os.path.relpath(full_path, start=root_src_path)
            if os.path.isdir(full_path):
                path += process_directory(full_path, root_src_path)
            else:
                path.append(relative_path)
    return path


main(src_path, dst_path)