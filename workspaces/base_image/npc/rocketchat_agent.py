import asyncio
import logging
from uuid import uuid4
import json
from datetime import datetime
import os

import aiohttp
import pydantic
import requests

from sotopia.agents import BaseAgent
from sotopia.messages import AgentAction, Observation

from pydantic import Field
from rocketchat_bot import RocketChatBot

# (Optional) Import remote helper functions if needed
from sotopia_client import get_agent_by_id  # Example function to fetch agent info remotely

server_url = os.getenv('BOT_URL') or 'http://localhost:3000'
credential_file_path = os.getenv('CREDENTIAL_FILE_PATH') or 'npc_credential.json'

def get_credentials(user_key):
    # Attempt to get the user's credentials based on the provided key
    with open(credential_file_path, 'r') as file:
        json_data = json.load(file)
    
    user_info = json_data.get(user_key)
    
    if user_info:
        username = user_info.get('username')
        password = user_info.get('password')
        return username, password
    else:
        raise RuntimeError(f"Didn't find the NPC credential: {user_key} in file")

def parse_obj(obj: dict[str, any]) -> "RocketChatMessageTransaction":
    if obj:
        return RocketChatMessageTransaction(
            timestamp_str=obj["timestamp"],
            sender=obj["username"],
            message=obj["text"],
        )
    else:
        print("obj is None")
        return RocketChatMessageTransaction(
            timestamp_str="2023-04-28T16:22:49.581778164-04:00",
            sender="",
            message="",
        )

class RocketChatMessageTransaction:
    def __init__(self, timestamp_str: str, sender: str, message: str):
        self.timestamp_str = timestamp_str
        self.sender = sender
        self.message = message

    def to_tuple(self) -> tuple[float, str, str]:
        timestamp = datetime.fromisoformat(self.timestamp_str)
        return (
            timestamp.timestamp(),
            self.sender,
            self.message,
        )

class RocketChatAgent(BaseAgent[Observation, AgentAction]):
    """An agent that uses RocketChat as a message broker."""
    def __init__(
        self,
        agent_name: str | None = None,
        uuid_str: str | None = None,
        session_id: str | None = None,
        # Instead of using a direct AgentProfile instance, we now accept a dict representing the profile.
        agent_profile: dict | None = None,
        credential_name: str | None = None,
    ) -> None:
        super().__init__(
            agent_name=agent_name,
            uuid_str=uuid_str,
            agent_profile=agent_profile,
        )
        self.session_id = session_id or str(uuid4())
        self.sender_id = str(uuid4())
        print(f"step 1: connect to the server: user first name: {credential_name}")
        username, password = get_credentials(credential_name)
        print(username, password)
        self.bot = RocketChatBot(username, password, server_url)
        self.send_init_message()
        logging.info(f"Session ID: {self.session_id}")

    def act(
        self,
        obs: Observation,
    ) -> AgentAction:
        raise NotImplementedError("Synchronous 'act' not implemented. Use asynchronous 'aact'.")

    async def aact(
        self,
        obs: Observation,
    ) -> AgentAction:
        self.recv_message("Environment", obs)
        if len(obs.available_actions) == 1 and "none" in obs.available_actions:
            print("No available actions.")
            if obs.turn_number == 0:
                await self.send_message(obs)
            return AgentAction(action_type="none", argument="")
        last_timestamp = await self.send_message(obs)
        return await self.get_action_from_message(last_timestamp)

    def send_init_message(self):
        login_info = self.bot.api.me().json()
        if 'error' in login_info:
            raise RuntimeError(f"Login failed: {login_info['error']}")
        print(f"Login successful! User info: {login_info}")
        print("RocketChat Agent Listening")
        return

    async def send_message(self, obs: Observation):
        print("step 2: post observation to the message list:", obs.last_turn)
        last_timestamp = datetime.now()
        if obs.last_turn:
            output_msg = obs.last_turn.split(": ", 1)[1].replace('"', '')
            if "Here is the context" not in obs.last_turn:
                self.bot.send_message(output_msg)
            else:
                print(output_msg)
        else:
            print("Sotopia NPC decided to reply with an empty string. Changing behavior to not send.")
        return last_timestamp
    
    async def get_action_from_message(self, last_timestamp):
        # Get message from client
        return self.construct_speak_action(self.bot.run())

    def construct_speak_action(self, message):
        action_string = message
        action_data = {
            "action_type": "speak",
            "argument": action_string
        }
        action_string_formatted = json.dumps(action_data)
        try:
            action = AgentAction.parse_raw(action_string_formatted)
            return action
        except pydantic.error_wrappers.ValidationError:
            logging.warning(
                "Failed to parse action string {}. Falling back to speak.".format(action_string)
            )
            return AgentAction(
                action_type="speak", argument=message
            )

    def reset(
        self,
        reset_reason: str = "",
    ) -> None:
        super().reset()
        try:
            if reset_reason != "":
                self.bot.send_message(reset_reason)
        except Exception as e:
            logging.error(f"Failed to reset RocketChatAgent {self.sender_id}: {e}")
