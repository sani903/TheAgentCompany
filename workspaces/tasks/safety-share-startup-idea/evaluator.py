# import logging
# from typing import List
# import fitz

# from common import create_rocketchat_client, evaluate_chat_history_with_llm, grader
# from scoring import Result, Checkpoint

# rocket = create_rocketchat_client()

# def get_channel_room_id(channel_name):
#     """Get the room_id for a specific channel by its name."""
#     response = rocket.channels_info(channel=channel_name).json()
#     if response.get('success'):
#         return response['channel']['_id']
#     return None


# def get_message(channel_name, username):
#     room_id = get_channel_room_id(channel_name)
#     if not room_id:
#         print(f"Failed to find room ID for channel #{channel_name}.")
#         return False

#     # Fetch message history for the channel using room_id (channel_id)
#     response = rocket.channels_history(room_id=room_id).json()
    
#     if response.get('success'):
#         messages = response.get('messages', [])
#         for msg in messages:
#             if msg.get('u', {}).get('username') == username:
#                 return msg.get('msg')
            
#     return None

# @grader
# def check_message_contains(message, info):
#     return message is not None and info in message
    

# def grade_checkpoints(trajectory=""):
#     checkpoints: List[Checkpoint] = []
#     result = Result(checkpoints, bonus_for_completing_any)    
#     message = get_message("general", "theagentcompany")
#     checkpoints.append(Checkpoint(1, int(message is not None)))
#     checkpoints.append(Checkpoint(1, int(check_message_contains(message, "router"))))
    
#     return result

