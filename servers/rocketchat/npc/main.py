from fastapi import FastAPI
from sotopia.database.persistent_profile import AgentProfile
from pydantic import BaseModel
from typing import List

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

@app.get("/npcs/")
async def get_npcs():
    npcs = AgentProfile.find().all()
    return {"npcs": [npc.dict() for npc in npcs]}

@app.post("/npcs/")
async def create_npc(npc: NPC):
    agent_profile = AgentProfile.parse_obj(npc.dict())
    agent_profile.save()
    return {"message": "NPC created successfully", "npc": npc.dict()}

@app.get("/npcs/{first_name}/{last_name}")
async def get_npc(first_name: str, last_name: str):
    npc = AgentProfile.find(
        (AgentProfile.first_name == first_name) &
        (AgentProfile.last_name == last_name)
    ).all()
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    return {"npc": npc[0].dict()}

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
