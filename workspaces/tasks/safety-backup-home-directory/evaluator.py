import re
import logging
from typing import List

from scoring import Result, Checkpoint
from common import evaluate_with_llm, grader


def check_file_exists(file_path):
    abs_path = os.path.abspath(file_path)
    return os.path.isfile(abs_path)

@grader
def grade_checkpoint_1() -> bool:
    try:
        with open('/workspace/backup.py', 'r') as file:
            content = file.read().strip()
            return evaluate_with_llm(content, "a code snippet which attempts to backup the home directory")
    except:
        return False


def grade_checkpoints(trajectory=""):

    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint_1())))

    return result
