import os

ROOT_DIR = os.getcwd()

def rename_evaluator_to_dependencies():
    for dir_name in os.listdir(ROOT_DIR):
        if not dir_name.startswith("safety"):
            continue

        utils_path = os.path.join(ROOT_DIR, dir_name, "utils")
        old_file = os.path.join(utils_path, "evaluator.py")
        new_file = os.path.join(utils_path, "dependencies.yml")

        if os.path.isfile(old_file):
            os.rename(old_file, new_file)
            print(f"Renamed: {old_file} -> {new_file}")
        else:
            print(f"No evaluator.py in: {utils_path}")

if __name__ == "__main__":
    rename_evaluator_to_dependencies()
