import httpx
from typing import Any, Dict, List

# The base URL for the Sotopia FastAPI service
SOTOPIA_BASE_URL = "http://sotopia-server:8800"

# ---------------------
# Scenario Endpoints
# ---------------------
async def get_scenarios_all() -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/scenarios")
        response.raise_for_status()
        return response.json()

async def get_scenarios(get_by: str, value: str) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/scenarios/{get_by}/{value}")
        response.raise_for_status()
        return response.json()

async def create_scenario(scenario_data: Dict[str, Any]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SOTOPIA_BASE_URL}/scenarios", json=scenario_data)
        response.raise_for_status()
        return response.json()  # Expected to return the new scenario's pk

async def delete_scenario(scenario_id: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SOTOPIA_BASE_URL}/scenarios/{scenario_id}")
        response.raise_for_status()
        return response.json()

# ---------------------
# Agent Endpoints
# ---------------------
async def get_agents_all() -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/agents")
        response.raise_for_status()
        return response.json()

async def get_agents(get_by: str, value: str) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/agents/{get_by}/{value}")
        response.raise_for_status()
        return response.json()

async def create_agent(agent_data: Dict[str, Any]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SOTOPIA_BASE_URL}/agents", json=agent_data)
        response.raise_for_status()
        return response.json()  # Expected to return the new agent's pk

async def delete_agent(agent_id: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SOTOPIA_BASE_URL}/agents/{agent_id}")
        response.raise_for_status()
        return response.json()

# ---------------------
# Relationship Endpoints
# ---------------------
async def get_relationship(agent_1_id: str, agent_2_id: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/relationship/{agent_1_id}/{agent_2_id}")
        response.raise_for_status()
        return response.json()

async def create_relationship(relationship_data: Dict[str, Any]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SOTOPIA_BASE_URL}/relationship", json=relationship_data)
        response.raise_for_status()
        return response.json()

async def delete_relationship(relationship_id: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SOTOPIA_BASE_URL}/relationship/{relationship_id}")
        response.raise_for_status()
        return response.json()

# ---------------------
# Episode Endpoints
# ---------------------
async def get_episodes_all() -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/episodes")
        response.raise_for_status()
        return response.json()

async def get_episodes(get_by: str, value: str) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/episodes/{get_by}/{value}")
        response.raise_for_status()
        return response.json()

async def delete_episode(episode_id: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SOTOPIA_BASE_URL}/episodes/{episode_id}")
        response.raise_for_status()
        return response.json()

# ---------------------
# Models
# ---------------------
async def get_models() -> List[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/models")
        response.raise_for_status()
        return response.json()

# ---------------------
# Evaluation Dimensions Endpoints
# ---------------------
async def get_evaluation_dimensions() -> Dict[str, List[Any]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SOTOPIA_BASE_URL}/evaluation_dimensions")
        response.raise_for_status()
        return response.json()

async def create_evaluation_dimensions(evaluation_data: Dict[str, Any]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SOTOPIA_BASE_URL}/evaluation_dimensions", json=evaluation_data)
        response.raise_for_status()
        return response.json()

async def delete_evaluation_dimension_list(list_name: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SOTOPIA_BASE_URL}/evaluation_dimensions/{list_name}")
        response.raise_for_status()
        return response.json()

# ---------------------
# Simulation Endpoint
# ---------------------
async def simulate(simulation_data: Dict[str, Any]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SOTOPIA_BASE_URL}/simulate", json=simulation_data)
        response.raise_for_status()
        # Assuming the simulation endpoint returns a simulation episode ID or OK message.
        return response.text

