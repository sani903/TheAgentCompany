import os
import json
import re

def fix_newlines_in_json_strings(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # This regex finds any string (inside double quotes) that contains \n
    def replace_newlines(match):
        original = match.group(0)
        fixed = original.replace('\\n', ' ')
        return fixed

    updated_content = re.sub(r'"(?:[^"\\]|\\.)*?\\n(?:[^"\\]|\\.)*?"', replace_newlines, content)

    if content != updated_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Fixed: {filepath}")
    else:
        print(f"No changes: {filepath}")

def find_and_fix_scenarios(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file == 'scenarios.json':
                full_path = os.path.join(dirpath, file)
                fix_newlines_in_json_strings(full_path)

if __name__ == "__main__":
    find_and_fix_scenarios('.')
