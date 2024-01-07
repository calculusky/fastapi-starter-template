from typing import TypeVar
import random

TData = TypeVar("TData", dict | list[dict], None)

def buildResponse(message: str, data: TData = None):
    return {
        "message": message,
        "data": data
    }

def generateRandomNum(length: int | None = None):
    string = ""
    len = length or 5
    for i in range(1, len + 1):
        num = random.randint(0, 9)
        string += str(num)
    return string
    
    