import redis
import os
from dotenv import load_dotenv
import logging
import json
import tomllib

logging.basicConfig(level=logging.INFO)

load_dotenv()
def load_or_create_json_loader(file_path,encode):
    if os.path.exists(file_path):
        with open(file_path, 'r',encoding=encode) as f:
            return json.load(f)
    else:
        with open(file_path, 'w') as f:
            json.dump({}, f)
        return {}
try:
    with open('task.toml', 'rb') as f:
        pyproject = tomllib.load(f)
        logging_config = pyproject.get('tool', {}).get('logging', {})
        logging.basicConfig(**logging_config)
        task_target = pyproject.get('path')+pyproject.get('target')
        json_loader = load_or_create_json_loader(task_target,pyproject.get('encode','utf-8'))
except FileNotFoundError:
    logging.basicConfig(level=logging.INFO)
input=''
class ModelRepository:
    def __init__(self):
        pool = redis.ConnectionPool(
            host=os.getenv('HOST', 'localhost'),
            port=int(os.getenv('PORT', 6379)),
            db=int(os.getenv('DB', 0)),
            decode_responses=os.getenv('D_R', 'True') == 'True'
        )
        self._client = redis.Redis(connection_pool=pool)
        logging.info("Connected to Redis")
class ModelService:
    def __init__(self, repository: ModelRepository):
        self.repo = repository
