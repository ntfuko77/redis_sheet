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
except FileNotFoundError:
    logging.basicConfig(level=logging.INFO)
input=''
class ModelRepository:
    def __init__(self):
        self.json_resourse={'path':task_target,"encode":pyproject.get('encode','utf-8')}
        pool = redis.ConnectionPool(
            host=os.getenv('HOST', 'localhost'),
            port=int(os.getenv('PORT', 6379)),
            db=int(os.getenv('DB', 0)),
            decode_responses=os.getenv('D_R', 'True') == 'True'
        )
        self._client = redis.Redis(connection_pool=pool)
        logging.info("Connected to Redis")
        json_loader = load_or_create_json_loader(task_target,pyproject.get('encode','utf-8'))
        self._load_data(json_loader)
    def _load_data(self,json_loader):
        sets=json_loader['indexs']
        hashes=json_loader['data']
        pipe = self._client.pipeline()
        for key, value in sets.items():
            pipe._client.sadd(key, *value)
            pipe.expire(key, pyproject.get('EXPIRE', 3600))
        for key, value in hashes.items():
            pipe._client.hset(key, mapping=value)
            pipe.expire(key, pyproject.get('EXPIRE', 3600))
    def save_data(self):
        with open(self.json_resourse['path'], 'w',encoding=self.json_resourse['encode']) as f:
            ...
    def set_data(self, key, mapping):
        self._client.hset(key, mapping=mapping)
    def delete_data(self, key):
        self._client.delete(key)
    def get_data(self, key):
        return self._client.hgetall(key)
    def key_exists(self, key):
        return self._client.exists(key)

class ModelService:
    def __init__(self, repository: ModelRepository):
        self.repo = repository
