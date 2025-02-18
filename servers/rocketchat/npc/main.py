from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sotopia.database import AgentProfile
import json

app = FastAPI()

# Define Pydantic model for NPC data
class NPC(BaseModel):
    first_name: str
    last_name: str
    age: int
    description: str

# Load NPC definitions from JSON (optional for initialization)
@app.on_event("startup")
async def load_initial_data():
    try:
        with open('npc_definition.json', 'r') as file:
            agent_definitions = json.load(file)
        for definition in agent_definitions:
            if not AgentProfile.find(
                (AgentProfile.first_name == definition["first_name"]) &
                (AgentProfile.last_name == definition["last_name"])
            ).all():
                agent_profile = AgentProfile.parse_obj(definition)
                agent_profile.save()
    except Exception as e:
        print(f"Error loading initial data: {e}")

# Endpoint to get all NPCs
@app.get("/npcs/")
async def get_npcs():
    npcs = AgentProfile.find().all()
    return {"npcs": [npc.dict() for npc in npcs]}

# Endpoint to get an NPC by name
@app.get("/npcs/{first_name}/{last_name}")
async def get_npc(first_name: str, last_name: str):
    npc = AgentProfile.find(
        (AgentProfile.first_name == first_name) &
        (AgentProfile.last_name == last_name)
    ).all()
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    return {"npc": npc[0].dict()}

# Endpoint to create a new NPC
@app.post("/npcs/")
async def create_npc(npc: NPC):
    existing_npc = AgentProfile.find(
        (AgentProfile.first_name == npc.first_name) &
        (AgentProfile.last_name == npc.last_name)
    ).all()
    if existing_npc:
        raise HTTPException(status_code=400, detail="NPC already exists")
    
    agent_profile = AgentProfile.parse_obj(npc.dict())
    agent_profile.save()
    return {"message": "NPC created successfully", "npc": npc.dict()}

# Endpoint to delete an NPC by name
@app.delete("/npcs/{first_name}/{last_name}")
async def delete_npc(first_name: str, last_name: str):
    npc = AgentProfile.find(
        (AgentProfile.first_name == first_name) &
        (AgentProfile.last_name == last_name)
    ).all()
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    
    npc[0].delete()
    return {"message": "NPC deleted successfully"}
