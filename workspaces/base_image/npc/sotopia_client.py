import httpx
from typing import Any, Dict

SOTOPIA_BASE_URL = "http://sotopia-server:8800"

async def get_agent_by_id(agent_id: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/agents/id/{agent_id}")
        response.raise_for_status()
        return response.json()

async def get_agent_by_name(first_name: str, last_name: str) -> Dict[str, Any]:
    params = {"first_name": first_name, "last_name": last_name}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/agents", params=params)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data[0]
        raise Exception("Agent not found")

async def get_scenario_by_id(scenario_id: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/scenarios/id/{scenario_id}")
        response.raise_for_status()
        return response.json()

