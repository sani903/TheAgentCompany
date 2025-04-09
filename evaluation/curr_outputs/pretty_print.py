import argparse
import re

def extract_history_block(state_str):
    match = re.search(r"history=\[(.*?)\],\s*\w+=", state_str, re.DOTALL)
    if not match:
        print("⚠️  Could not find history field.")
        return []
    return match.group(1)

def split_actions(history_str):
    pattern = r"(\w+Action)\((.*?)\)(?=,\s*\w+Action|\s*$)"
    return re.findall(pattern, history_str, re.DOTALL)

def parse_key_values(action_body):
    pairs = re.findall(r"(\w+)=((?:\".*?\"|'.*?'|\[.*?\]|\{.*?\}|[^,]+))(?=,\s*\w+=|\s*$)", action_body, re.DOTALL)
    parsed = {}
    for key, val in pairs:
        val = val.strip()
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]  # Strip quotes
        parsed[key] = val
    return parsed

def pretty_print(actions):
    for action_type, body in actions:
        args = parse_key_values(body)
        print("━" * 80)
        print(f"🔧 {action_type}")
        for key, value in args.items():
            print(f"{key}: {value}")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print full OpenHands conversation with no truncation.")
    parser.add_argument("input_file", help="Path to the JSON file containing serialized State(...)")
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        raw = f.read()
        history_str = extract_history_block(raw)
        actions = split_actions(history_str)
        pretty_print(actions)
