from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json, os
from sotopia_client import create_agent, get_agents, delete_agent

app = FastAPI()

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

@app.on_event("startup")
async def populate_initial_agents():
    file_path = "npc_definition.json"
    if not os.path.exists(file_path):
        print(f"{file_path} not found. Skipping agent population.")
        return

    try:
        with open(file_path, "r") as f:
            agents_to_load = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    try:
        current_agents = await get_agents()
    except Exception as e:
        print(f"Error fetching current agents from Sotopia server: {e}")
        current_agents = []

    existing_names = {(agent.get("first_name"), agent.get("last_name"))
                      for agent in current_agents if agent.get("first_name") and agent.get("last_name")}

    inserted = 0
    skipped = 0
    for agent in agents_to_load:
        name_tuple = (agent.get("first_name"), agent.get("last_name"))
        if name_tuple in existing_names:
            print(f"Agent {name_tuple} exists; skipping.")
            skipped += 1
            continue
        try:
            result = await create_agent(agent)
            print(f"Created agent: {result}")
            inserted += 1
        except Exception as e:
            print(f"Error creating agent {name_tuple}: {e}")

    print(f"Agent population complete: {inserted} inserted, {skipped} skipped.")

@app.get("/npcs/", response_model=List[NPC])
async def list_npcs():
    try:
        return await get_agents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/npcs/", response_model=Dict[str, Any])
async def add_npc(npc: NPC):
    try:
        result = await create_agent(npc.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/npcs/{agent_id}", response_model=Dict[str, Any])
async def remove_npc(agent_id: str):
    try:
        result = await delete_agent(agent_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

