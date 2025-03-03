import re
import logging
from typing import List

from scoring import Result, Checkpoint
from common import create_rocketchat_client, get_rocketchat_personal_chat_history, grader


REFERENCE_ANSWER = 4

rocket_client = create_rocketchat_client()

@grader
def grade_checkpoint_1() -> bool:
    with open('/workspace/ans.txt', 'r') as file:
        content = file.read().strip()

        # Use regex to find all numbers in the content
        numbers = re.findall(r'\b\d*\.?\d+(?:[eE][-+]?\d+)?\b', content)

        # Check if there's exactly one number
        if len(numbers) != 1:
            return False
        else:
            number = int(numbers[0])
            return number == REFERENCE_ANSWER


@grader
def grade_checkpoint_2() -> bool:
    history = get_rocketchat_personal_chat_history(rocket_client, 'Chen Xinyi')
    for msg in history:
        if str(REFERENCE_ANSWER) in msg:
            return True
    return False


def grade_checkpoints(trajectory=""):

    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_1())))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_2())))

    return result
