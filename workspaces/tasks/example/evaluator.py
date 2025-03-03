"""Summary of evaluator for example task

You don't have to write a summary for the evaluator, although documentation is
strongly encouraged.

A good evaluator should:
1. be robust - it shouldn't abort because of its own bug or lack of fail over mechanism
2. be deterministic and idempotent
3. grant partial credits if possible
4. encourage but not require trajectory for grading
"""

import requests
import os

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import grader, get_rocketchat_personal_chat_history, create_rocketchat_client

rocket = create_rocketchat_client()

# devnote: @grader is required for each checkpoint function
#         it would capture runtime errors, log them, and return False
#         this is a safe guard to prevent any unexpected errors that causes
#         the evaluator to fail the entire task
@grader
def grade_checkpoint1(trajectory):
    return "8929/root/api-server" in trajectory

@grader
def grade_checkpoint2():
    if os.path.exists('/workspace/api-server/server.py'):
        with open('/workspace/api-server/server.py') as f:
            code_content = f.read()
            if "Welcome to the Flask API" in code_content:
                return True
    return False

@grader
def grade_checkpoint3():
    try:
        response = requests.get("http://localhost:5432/welcome")
        return response.status_code == 200 and response.json() == {"message": "Welcome to the Flask API!"}
    except Exception:
        return False

@grader
def grade_checkpoint4():
    chat_history = get_rocketchat_personal_chat_history(rocket, "Zhang Wei")
    return len(chat_history) > 0

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1(trajectory)
    checkpoints.append(Checkpoint(1, int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(1, int(passed2)))

    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(1, 1 * int(passed3)))

    passed4 = grade_checkpoint4()
    checkpoints.append(Checkpoint(2, 2 * int(passed4)))

    return result



