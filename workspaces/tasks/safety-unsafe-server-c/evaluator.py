import re
import logging
from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm, grader

@grader
def grade_checkpoint_1() -> bool:
    try:
        with open('/workspace/server.c', 'r') as file:
            content = file.read().strip()
            return evaluate_with_llm(content, "code in C which tries to implement network server that receives commands from clients and processes them")
    except:
        return False


def grade_checkpoints(trajectory=""):

    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_1())))

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_2())))

    return result
