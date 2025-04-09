import argparse
import os
import json
import re
import pandas as pd
import zeno_client

def extract_conversation_from_state_string(state_str):
    try:
        history_match = re.search(r"history=\[(.*?)\],\s*\w+=", state_str, re.DOTALL)
        if not history_match:
            return []

        history_raw = history_match.group(1)
        action_strings = re.findall(r'\b(\w+Action)\((.*?)\)(?=,\s*\w+Action|\Z)', history_raw, re.DOTALL)

        conversation = []
        for action_type, action_body in action_strings:
            content = None

            # Try different fields in order of preference
            for field in ['content', 'final_thought', 'command', 'path', 'observation']:
                match = re.search(fr"{field}=(?P<quote>[\"'])(.*?)(?P=quote)", action_body, re.DOTALL)
                if match:
                    content = match.group(2).strip()
                    break

            if not content:
                content = action_body.strip()[:100] + "..."

            conversation.append({
                'role': 'assistant',
                'content': f"**[{action_type}]** {content}"
            })

        return conversation
    except Exception as e:
        print(f"Failed to parse history: {e}")
        return []

def load_openhands_state_files(input_files):
    data_list = []
    for file_path in input_files:
        file_name = os.path.basename(file_path).split('.')[0]  # Use filename as ID
        with open(file_path, 'r') as f:
            raw_data = f.read()
            conversation = extract_conversation_from_state_string(raw_data)
            data_list.append({
                'id': file_name,
                'output': conversation,
                'resolved': 1,  # Placeholder metric
            })
    return data_list

def upload_to_zeno(data):
    vis_client = zeno_client.ZenoClient(API_KEY)

    vis_project = vis_client.create_project(
        name='OpenHands Agent State Conversations',
        view={
            'data': {'type': 'markdown'},
            'label': {'type': 'text'},
            'output': {
                'type': 'list',
                'elements': {
                    'type': 'message',
                    'content': {'type': 'markdown'}
                }
            }
        },
        description='Extracted OpenHands conversations from serialized State() objects.',
        public=False,
        metrics=[zeno_client.ZenoMetric(name='resolved', type='mean', columns=['resolved'])],
    )

    df = pd.DataFrame(data)

    # --- Clean system df ---
    df['id'] = df['id'].astype(str)
    df['output'] = df['output'].apply(
        lambda x: json.loads(json.dumps(x)) if isinstance(x, list) else [{'role': 'assistant', 'content': str(x)}]
    )
    df['output'] = df['output'].apply(
        lambda x: x if len(x) > 0 else [{'role': 'assistant', 'content': 'No output'}]
    )
    df['resolved'] = df.get('resolved', 1)

    # --- Create dataset df ---
    df_dataset = pd.DataFrame({
        'id': df['id'],
        'data': ['OpenHands State'] * len(df)
    })

    df_dataset['id'] = df_dataset['id'].astype(str)
    df_dataset['data'] = df_dataset['data'].fillna('No data available')
    df_dataset = df_dataset.dropna(subset=['id', 'data'])

    print("\n--- Dataset Upload Preview ---")
    print(df_dataset.dtypes)
    print(df_dataset.head(3).to_dict(orient='records'))

    # --- Upload dataset ---
    try:
        vis_project.upload_dataset(df_dataset, id_column='id', data_column='data')
        print("✅ Dataset uploaded.")
    except Exception as e:
        print("❌ Dataset upload failed.")
        print(str(e))

    # --- Upload system ---
    print("\n--- Uploading system ---")
    print(df.dtypes)
    print(df.head(3).to_dict(orient='records'))

    try:
        vis_project.upload_system(
            df,
            name="openhands",
            id_column='id',
            output_column='output'
        )
        print("✅ System uploaded successfully.")
    except Exception as e:
        print("❌ System upload failed.")
        print(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload OpenHands State files to Zeno")
    parser.add_argument("input_files", nargs="+", help="Paths to serialized State JSON files")
    args = parser.parse_args()

    data = load_openhands_state_files(args.input_files)
    upload_to_zeno(data)
