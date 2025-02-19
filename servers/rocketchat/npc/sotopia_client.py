import httpx
from typing import List, Dict

SOTOPIA_BASE_URL = "http://sotopia-server:8800"  # update if necessary

async def create_agent(npc_data: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SOTOPIA_BASE_URL}/agents", json=npc_data)
        response.raise_for_status()
        return response.json()

async def get_agents() -> List[Dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/agents")
        response.raise_for_status()
        return response.json()

async def delete_agent(agent_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SOTOPIA_BASE_URL}/agents/{agent_id}")
        response.raise_for_status()
        return response.json()
