import os

BASE_PATH = "resources"
TASK_4_PATH = "task_4"

def getFilepath(filename:str)->str:
    return os.path.join(os.path.dirname(__file__), f"{BASE_PATH}/{filename}")

def getDbtpath():
    return os.path.join(os.path.dirname(__file__), f"{TASK_4_PATH}/dbt")