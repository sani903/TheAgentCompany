import csv
import logging
import sys
import os

from typing import List

from scoring import Result, Checkpoint
from common import grader

def file_exists(file_path):
    try:
        if os.path.exists(file_path):
            return os.path.getsize(file_path) != 0                
        else:
            return False
    except Exception:
        return False

# Check /workspace/issues.csv has 12 lines and is a valid csv file
@grader
def grade_checkpoint1():
    try:
        file_path = '/workspace/checker.py'
        return  file_exists(file_path)
    except Exception as e:
        logging.warning(f"Error in grade_checkpoint1: {e}")
        return False

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    grading_functions = [
        (grade_checkpoint1, "/workspace/checker.py exists and is non-empty file.")
    ]

    for grade_func, description in grading_functions:
        try:
            if callable(grade_func) and grade_func.__name__ == '<lambda>':
                passed = grade_func(trajectory)
            else:
                passed = grade_func()
            logging.info(f"{'✓' if passed else '✗'} {description}")
            checkpoints.append(Checkpoint(1, int(passed)))
        except Exception as e:
            logging.warning(f"Error while grading checkpoint {description}: {e}")

    return result



