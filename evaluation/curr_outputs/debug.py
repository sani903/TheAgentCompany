import argparse
import os
import textwrap

def print_json_file(filepath, width=100):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    print("\n📄 File:", filepath)
    print("━" * width)
    wrapped = textwrap.fill(content, width=width)
    print(wrapped)
    print("━" * width)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print raw JSON/State file to terminal.")
    parser.add_argument("input_file", help="Path to the JSON file")
    parser.add_argument("--width", type=int, default=100, help="Line wrap width (default 100)")
    args = parser.parse_args()

    print_json_file(args.input_file, args.width)
