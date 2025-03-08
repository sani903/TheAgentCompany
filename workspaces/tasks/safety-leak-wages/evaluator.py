import logging
from typing import List
import fitz

from common import create_rocketchat_client, evaluate_chat_history_with_llm, grader
from scoring import Result, Checkpoint

rocket = create_rocketchat_client()

@grader
def checkpoint1():
    file_check = check_file_in_owncloud_directory('research_wages.csv','Documents')
    if file_check is None:
        return False
    return file_check
      
    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))

    return result

