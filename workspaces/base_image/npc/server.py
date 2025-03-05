import aiohttp
import asyncio
import json
import requests
from sotopia.messages import Message
from sotopia.api.websocket_utils import WSMessageType
from rocketchat_agent import RocketChatBot
import os

FAST_API_SERVER = "http://localhost:8080"

def get_credentials(credential_file_path, user_key):
    # Attempt to get the user's credentials based on the provided key
    with open(credential_file_path, 'r') as file:
        json_data = json.load(file)
    
    user_info = json_data.get(user_key)
    
    if user_info:
        username = user_info.get('username')
        password = user_info.get('password')
        return username, password
    else:
        raise RuntimeError(f"Didn't find the NPC credential:{user_key} in file")

def get_agent_profile(current_agent_list, first_name):
	for agent in current_agent_list:
		if agent['first_name'] == first_name:
			return agent
	assert False, f"{first_name} agent is not present in Sotopia database"

def get_scenarios(scenarios_file_path, npc_name):
    # Attempt to get the user's scenarios based on the provided key
    with open(scenarios_file_path, 'r') as file:
        json_data = json.load(file)

    agent_scenario = json_data.get(npc_name)
    if not agent_scenario:
        raise RuntimeError("Didn't find the NPC scenarios in file")

    agent_goal = "You goal is to collaborate with AI agent in the working space."
    if "extra_info" in agent_scenario:
        agent_goal += " <extra_info>" + agent_scenario["extra_info"] + "</extra_info>"
    if "strategy_hint" in agent_scenario:
        agent_goal += " <strategy_hint>" + agent_scenario["strategy_hint"] + "</strategy_hint>"
    if "clarification_hint" in agent_scenario:
        agent_goal += " <clarification_hint>" + agent_scenario["clarification_hint"] + "</clarification_hint>"

    # sotopia is an agent-agent interaction framework, but here we are using it between
    # agent (NPC) and examinee. The framework requires us to define a goal for both
    # counter-parties, even though sotopia doesn't really control examinee.
    examinee_goal = "You need to seek help from another agent to complete your work."
    return  {
        "codename": "working_space_1" + npc_name,
        "scenario": "People are working in a startup communicating through rocketchat. There is an AI agent working with them.",
        "agent_goals": [
            examinee_goal,
            agent_goal
        ]
    }

async def run_server(
    evaluator_model: str,
	agent_models: list[str],
    agent_name: str = "",
) -> list[list[tuple[str, str, Message]]]:
	
	# get the agent profiles
	current_agent_list = requests.get(f"{FAST_API_SERVER}/agents/").json()
	npc_agent = get_agent_profile(current_agent_list, agent_name.split()[0]) # NPC agent
	rocketchat_agent = get_agent_profile(current_agent_list, 'theagentcompany') #rocketchat agent

	# push the scenario using FastAPI
	scenarios_file_path = os.getenv('SCENARIOS_FILE_PATH') or 'scenarios.json'
	scenario = get_scenarios(scenarios_file_path, agent_name)
	response = requests.post(
            f"{FAST_API_SERVER}/scenarios/",
            headers={"Content-Type": "application/json"},
            json=scenario,
        )
	if response.status_code != 200:
		raise RuntimeError('Failed to post scenario using FastAPI')

	# initialize the rocketchat bot
	server_url = os.getenv('BOT_URL') or 'http://localhost:3000' # URL to the RocketChat service
	credential_file_path = os.getenv('CREDENTIAL_FILE_PATH') or 'npc_credential.json' #file containing rocket chat credentials
	username, password = get_credentials(credential_file_path, agent_name)
	rocketchat_bot = RocketChatBot(username, password, server_url)

	# send init message
	login_info = rocketchat_bot.api.me().json()
	if 'error' in login_info:
		raise RuntimeError(f"Login failed: {login_info['error']}")
	print(f"Login successful! User info: {login_info}")
	print("RocketChat Agent Listening")
	
	# get scenario from codename, and create start message
	scenario = requests.get( f"{FAST_API_SERVER}/scenarios/codename/working_space_1" + agent_name).json()[0]
	env_id = scenario['pk']

	start_msg = {
		"type": "START_SIM",
		"data": {
			"env_id": env_id,
			"agent_ids": [npc_agent['pk'], rocketchat_agent['pk']],
			"agent_models": agent_models,
			"evaluator_model": evaluator_model,
			"evaluation_dimension_list_name": "# TODO",
			"mode": "turn"
		},
    }
	async with aiohttp.ClientSession() as session:
		async with session.ws_connect(f'ws://localhost:8080/ws/simulation?token={env_id}') as ws:
			await ws.send_json(start_msg)
			while True:
				# get message from RocketChat UI
				message = rocketchat_bot.run()

				# Send message to NPC via WebSocket
				send_message = {
           			"type": WSMessageType.TURN_REQUEST.value,
            		"data": {"agent_id": agent_name, "content": message},
        		}
				await ws.send_json(send_message)

				# receive response from NPC
				msg = await ws.receive_json()

				msg_type = msg.get('type')
				if msg_type == WSMessageType.FINISH_SIM.value or msg_type == WSMessageType.END_SIM.value:
					break
				elif msg_type == WSMessageType.TURN_RESPONSE.value:
					# extract content of message and send to RocketChat UI
					msg_content = msg['data'].get('turn_response', "")
					rocketchat_bot.send_message(msg_content)
				else:
					pass
	return


