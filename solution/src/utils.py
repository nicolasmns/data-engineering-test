import os

BASE_PATH = "resources"

def getFilepath(filename:str)->str:

    return os.path.join(os.path.dirname(__file__), f"{BASE_PATH}/{filename}")
