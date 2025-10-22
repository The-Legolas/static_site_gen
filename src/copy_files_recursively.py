import os
import shutil

def copy_files_recursive(src_path, dst_path):
    if not os.path.exists(src_path):
        raise ValueError(f"The {src_path} does not exist")
    if os.path.exists(dst_path):
        print(f"Deleting {dst_path} directory...")
        shutil.rmtree(dst_path)
    os.makedirs(dst_path, exist_ok=True)

    for entry in os.listdir(src_path):
        src_full_path = os.path.join(src_path, entry) 
        dst_full_path = os.path.join(dst_path, entry) 
        if os.path.isfile(src_full_path):
            print(f" * Found file: {entry} -> copying to {dst_full_path}")
            shutil.copy(src_full_path, dst_full_path)
        if os.path.isdir(src_full_path):
            os.makedirs(dst_full_path, exist_ok=True)
            copy_files_recursive(src_full_path, dst_full_path)