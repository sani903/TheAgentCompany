import os

EXCLUDE_FILES = {"task.md", "checkpoints.md", "scenarios.json"}

def print_tree(root, prefix=""):
    entries = sorted(os.listdir(root))
    for i, entry in enumerate(entries):
        path = os.path.join(root, entry)
        connector = "└── " if i == len(entries) - 1 else "├── "
        print(f"{prefix}{connector}{entry}")
        if os.path.isdir(path):
            extension = "    " if i == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension)

def main():
    cwd = os.getcwd()
    for folder in sorted(os.listdir(cwd)):
        if not folder.startswith("safety"):
            continue

        folder_path = os.path.join(cwd, folder)
        if not os.path.isdir(folder_path):
            continue

        # Check for non-excluded files in top-level of folder
        top_files = [f for f in os.listdir(folder_path)
                     if os.path.isfile(os.path.join(folder_path, f))
                     and f not in EXCLUDE_FILES]

        if not top_files:
            continue  # Skip folders with only the excluded files

        print(f"\n📁 {folder}/")
        print_tree(folder_path)

if __name__ == "__main__":
    main()
