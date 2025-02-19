from fastapi import FastAPI, HTTPException
from sotopia.database.persistent_profile import AgentProfile
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

# Define the NPC model to validate incoming data
class NPC(BaseModel):
    first_name: str
    last_name: str
    age: int
    occupation: str
    profile_picture: str
    gender: str
    gender_pronoun: str
    public_info: str
    big_five: str
    moral_values: List[str]
    schwartz_personal_values: List[str]
    personality_and_values: str
    decision_making_style: str
    secret: str
    model_id: str
    mbti: str

# Helper function to check if an NPC already exists using a composite key
def npc_exists(first_name: str, last_name: str) -> bool:
    existing = AgentProfile.find(
        (AgentProfile.first_name == first_name) &
        (AgentProfile.last_name == last_name)
    ).all()
    return bool(existing)

# Startup event to load NPC definitions from npc_definition.json,
# performing deduplication to avoid duplicate entries on restart.
@app.on_event("startup")
async def populate_initial_npcs():
    file_path = "npc_definition.json"
    if not os.path.exists(file_path):
        print(f"{file_path} not found. Skipping initial NPC population.")
        return

    try:
        with open(file_path, "r") as file:
            agent_definitions = json.load(file)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    inserted = 0
    skipped = 0

    for definition in agent_definitions:
        first_name = definition.get("first_name")
        last_name = definition.get("last_name")

        if npc_exists(first_name, last_name):
            print(f"NPC '{first_name} {last_name}' already exists; skipping.")
            skipped += 1
            continue

        try:
            agent_profile = AgentProfile.parse_obj(definition)
            agent_profile.save()
            print(f"Inserted NPC '{first_name} {last_name}' successfully.")
            inserted += 1
        except Exception as e:
            print(f"Failed to insert NPC '{first_name} {last_name}': {e}")

    print(f"Initial NPC population complete: {inserted} inserted, {skipped} skipped.")


@app.get("/npcs/")
async def get_npcs():
    npcs = AgentProfile.find().all()
    return {"npcs": [npc.dict() for npc in npcs]}

@app.post("/npcs/")
async def create_npc(npc: NPC):
    if npc_exists(npc.first_name, npc.last_name):
        raise HTTPException(status_code=400, detail="NPC already exists")
    agent_profile = AgentProfile.parse_obj(npc.dict())
    agent_profile.save()
    return {"message": "NPC created successfully", "npc": npc.dict()}

@app.get("/npcs/{first_name}/{last_name}")
async def get_npc(first_name: str, last_name: str):
    npcs = AgentProfile.find(
        (AgentProfile.first_name == first_name) &
        (AgentProfile.last_name == last_name)
    ).all()
    if not npcs:
        raise HTTPException(status_code=404, detail="NPC not found")
    return {"npc": npcs[0].dict()}

@app.delete("/npcs/{first_name}/{last_name}")
async def delete_npc(first_name: str, last_name: str):
    npcs = AgentProfile.find(
        (AgentProfile.first_name == first_name) &
        (AgentProfile.last_name == last_name)
    ).all()
    if not npcs:
        raise HTTPException(status_code=404, detail="NPC not found")
    npcs[0].delete()
    return {"message": "NPC deleted successfully"}
