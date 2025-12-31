import redis
import os
from dotenv import load_dotenv
import logging
import tomllib

logging.basicConfig(level=logging.INFO)

load_dotenv()


try:
    with open('task.toml', 'rb') as f:
        pyproject = tomllib.load(f)
        logging_config = pyproject.get('tool', {}).get('logging', {})
        logging.basicConfig(**logging_config)
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
    def set_data(self, key, mapping):
        self._client.hset(key, mapping=mapping)
    def delete_data(self, key):
        self._client.delete(key)
    def delete_entire_set(self,key):
        members = self._client.smembers(key)
        pipe = self._client.pipeline()
        for member in members:
            pipe.delete(member)
        pipe.delete(key)
        pipe.execute()
    def get_data(self, key):
        return self._client.hgetall(key)
    def key_exists(self, key):
        return self._client.exists(key)
    def add_to_set(self,  *values):
        self._client.sadd(self.set_name, *values)
    def remove_from_set(self, *values):
        self._client.srem(self.set_name, *values)
    
    

class ModelService:
    def __init__(self, repository: ModelRepository):
        self.repo = repository
