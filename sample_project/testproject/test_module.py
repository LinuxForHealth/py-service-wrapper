from typing import Dict
from pydantic import BaseModel
from typing import Union


def hello_name(name):
    return {'Hello': f'{name}!'}


def hello_name_and_age(name, age: int):
    return f'Hello, {name}! You are {age} years old'


def hello_world():
    return f'Hello, World!'


def hello_post(data: Dict):
    return f'hello {data}'


class TestModel(BaseModel):
    name: str
    age: int


def hello_pydantic(data: TestModel):
    return f'hello {data.name}! You are {data.age} years old'


def hello_dynamic(name: str, age: Union[int, float]):
    return f'Hello, {name}! You are {age} years old'
