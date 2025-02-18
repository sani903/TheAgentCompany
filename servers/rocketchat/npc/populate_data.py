import json
import requests

def populate_data():
    with open('npc_definition.json', 'r') as file:
        agent_definitions = json.load(file)

    for definition in agent_definitions:
        response = requests.post("http://localhost:8000/npcs/", json=definition)
        if response.status_code == 200:
            print(f'Inserted {definition["first_name"]} {definition["last_name"]} successfully')
        else:
            print(f'Failed to insert {definition["first_name"]} {definition["last_name"]}')

if __name__ == "__main__":
    populate_data()
