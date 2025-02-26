import aiohttp
import asyncio
import json
import requests
from sotopia.messages import Message
from sotopia.api.websocket_utils import WSMessageType
from rocketchat_agent import RocketChatAgent

FAST_API_SERVER = "http://localhost:8000"

async def run_server(
    model_dict: dict[str, str],
	model_name: str,
    agents_roles: dict[str, str],
    tag: str | None = None,
    push_to_db: bool = False,
    using_async: bool = True,
    agent_name: str = "",
) -> list[list[tuple[str, str, Message]]]:
	agents_model_dict = {
        "agent1": model_dict["agent1"],
        "agent2": model_dict["agent2"],
    }
	env_id = f"tmppk_env_id_{agent_name}"
	start_msg = {
            "type": "START_SIM",
            "data": {
                "env_id": env_id,
                "agent_ids": agents_model_dict.values(),
                "agent_models": [model_name, model_name],
                "evaluator_model": model_dict['env'],
                "evaluation_dimension_list_name": "# TODO",
                "mode": "turn"
            },
        }
	current_agent_list = requests.get(f"{FAST_API_SERVER}/agents/").json()
	agent_profile = None
	for agent in current_agent_list:
		if agent.first_name == "theagentcompany":
			agent_profile = agent
			break
	assert agent_profile is not None, "theagentcompany agent is not present in Sotopia database"
	rocket_chat_agent = RocketChatAgent(credential_name=agent_name, agent_profile=agent_profile)
	async with aiohttp.ClientSession() as session:
		async with session.ws_connect(f'ws://{FAST_API_SERVER}/ws/simulation?token={env_id}') as ws:
			await ws.send_json(start_msg)
			while True:
				msg = await ws.receive_json()
				msg_type = msg.get('type')
				if msg.type == WSMessageType.FINISH_SIM.value:
					break
				elif msg.type == WSMessageType.TURN_REQUEST.value:
					pass
					# TODO: modify RocketChatAgent to interface with these messages?
					# Or, directly use the RocketChatBot
					rocket_chat_agent.send_message(msg)
				else:
					pass
	return


