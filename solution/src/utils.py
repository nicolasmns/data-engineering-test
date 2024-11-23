import os

_BASE_PATH = "resources"
_TASK_4_PATH = "task_4"

HOST = "localhost"


def getFilepath(filename:str)->str:
    return os.path.join(os.path.dirname(__file__), f"{_BASE_PATH}/{filename}")

def getDbtpath():
    return os.path.join(os.path.dirname(__file__), f"{_TASK_4_PATH}/dbt")