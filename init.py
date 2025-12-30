import os
from dotenv import load_dotenv
import tomllib
from pydantic import BaseModel

class Config(BaseModel):
    path: str
    target: str
    encode: str
    EXPIRE:int
task_key=['path','target','encode','EXPIRE']
poll_config_key=['HOST','PORT','DB','D_R']

load_dotenv()
def env_variable_integrity():
    for key in poll_config_key:
        if os.getenv(key) is None:
            return False
    return True
def create_env_file(values:dict):
    with open('.env', 'w') as f:
        f.write("#REDIS CONFIG\n")
        for key, value in values.items():
            f.write(f"{key}={value}\n")
def input_env_variables():
    values = {}
    for key in poll_config_key:
        user_input = input(f"Please enter value for {key}: ")
        values[key] = user_input
    create_env_file(values)

def task_config_integrity():
    try:
        with open('task.toml', 'rb') as f:
            pyproject = tomllib.load(f)
            Config(**{key: pyproject.get(key) for key in task_key})
            return True
    except FileNotFoundError:
        return False

def create_task_file(values:dict):
    ...
def input_task_config():
    ...


def main():
    if not env_variable_integrity():
        input_env_variables()
    if not task_config_integrity():
        input_task_config()

main()
    

        