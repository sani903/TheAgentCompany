import os
import re

def find_dockerfiles_in_safety_dirs(root_dir):
    dockerfiles = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if not os.path.basename(dirpath).startswith("safety"):
            continue
        for filename in filenames:
            if filename == "Dockerfile":
                dockerfiles.append(os.path.join(dirpath, filename))
    return dockerfiles

def extract_run_commands(filepath):
    run_commands = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("RUN"):
                command = re.sub(r'\s+', ' ', line[3:].strip())
                run_commands.add(command)
    return run_commands

def main():
    root_dir = "."  # Adjust as needed
    all_run_commands = set()

    for dockerfile in find_dockerfiles_in_safety_dirs(root_dir):
        commands = extract_run_commands(dockerfile)
        all_run_commands.update(commands)

    print("Unique RUN commands:")
    for cmd in sorted(all_run_commands):
        print(f"RUN {cmd}")

if __name__ == "__main__":
    main()
