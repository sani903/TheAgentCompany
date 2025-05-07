import os
import re
import shutil
import zipfile

ROOT_DIR = os.getcwd()

def process_safety_dirs():
    for dir_name in os.listdir(ROOT_DIR):
        if not dir_name.startswith("safety"):
            continue

        task_path = os.path.join(ROOT_DIR, dir_name)
        if not os.path.isdir(task_path):
            continue

        print(f"Processing: {task_path}")

        # Create workspace and utils directories
        workspace_dir = os.path.join(task_path, "workspace")
        utils_dir = os.path.join(task_path, "utils")
        os.makedirs(workspace_dir, exist_ok=True)
        os.makedirs(utils_dir, exist_ok=True)

        dockerfile_path = os.path.join(task_path, "Dockerfile")
        if not os.path.isfile(dockerfile_path):
            print(f"  No Dockerfile found in {task_path}")
            continue

        with open(dockerfile_path, "r") as f:
            dockerfile_lines = f.readlines()

        dockerfile_content = ''.join(dockerfile_lines)
        uses_unzip = 'unzip' in dockerfile_content

        for line in dockerfile_lines:
            line = line.strip()
            if not line.startswith("COPY") or "/npc" in line:
                continue

            match = re.match(r"COPY\s+(.+?)\s+(/[\w/]+)", line)
            if not match:
                continue
            src, dst = match.groups()
            dst_folder = dst.strip("/").split("/")[0]

            src_file_path = os.path.join(task_path, src)
            if not os.path.isfile(src_file_path):
                print(f"  File not found: {src_file_path}")
                continue

            target_dir = workspace_dir if dst_folder == "workspace" else utils_dir if dst_folder == "utils" else None
            if not target_dir:
                print(f"  Skipped {src} (destination: {dst})")
                continue

            target_path = os.path.join(target_dir, os.path.basename(src))

            if src.endswith(".zip") and uses_unzip:
                shutil.move(src_file_path, target_path)
                print(f"  Moved and extracting zip: {src}")
                try:
                    with zipfile.ZipFile(target_path, 'r') as zip_ref:
                        zip_ref.extractall(target_dir)
                    os.remove(target_path)
                    print(f"  Extracted and removed {os.path.basename(src)}")
                except zipfile.BadZipFile:
                    print(f"  Failed to unzip {os.path.basename(src)} — skipping extraction.")
            else:
                shutil.move(src_file_path, target_path)
                print(f"  Moved {src} to {dst_folder}/")

if __name__ == "__main__":
    process_safety_dirs()
