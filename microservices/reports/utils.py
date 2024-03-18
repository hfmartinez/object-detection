import redis
from microservices.reports.config import global_config
from fastapi.encoders import jsonable_encoder
import json

redis_config = global_config.get_redis_config()


def redis_manager(data_store=None, key: str = "", operation: str = "read"):
    rd = redis.Redis(
        host=redis_config["REDIS_HOSTNAME"], port=redis_config["REDIS_PORT"], db=0
    )
    return_data = {}
    if operation == "read":
        data = rd.get(key)
        if data:
            return_data = json.loads(data)
    elif operation == "save":
        rd.set(key, json.dumps(jsonable_encoder(data_store)))
        return_data = data_store
    elif operation == "clear":
        rd.flushdb()
    return return_data
