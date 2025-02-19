import json
import logging

import requests
import time
import redis

"""
Reference: https://github.com/sotopia-lab/sotopia/blob/main/examples/fast_api_example.py
https://github.com/sotopia-lab/sotopia/blob/main/sotopia/api/fastapi_server.py
"""


BASE_URL = "http://localhost:8080"

with open('npc_definition.json', 'r') as file:
    agent_definitions = json.load(file)
    print(f"NPC definitions loaded, number of NPCs = {len(agent_definitions)}")

current_agent_list = requests.get(f"{BASE_URL}/agents/").json()
for definition in agent_definitions:
    is_present = False
    # the script must be idempotent
    for agent in current_agent_list:
        if agent['first_name'] == definition['first_name'] and agent['last_name'] == definition['last_name']:
            is_present=True
            break
    if is_present:
        continue
    attempts = 0
    while attempts < 5:
        response = requests.post(
            f"{BASE_URL}/agents/",
            headers={"Content-Type": "application/json"},
            json=definition,
        )
        if response.status_code == 200:
            break
        else:
            attempts += 1
    
