from typing import Dict


def hello_name(name):
    return f"Hello, {name}!"


def hello_name_and_age(name, age: int):
    return f"Hello, {name}! You are {age} years old"


def hello_world():
    return f"Hello, World!"


def hello_post(data: Dict):
    return f"hello {data}"