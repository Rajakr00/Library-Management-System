import redis
from flask_caching import Cache

redis_client = redis.Redis(host='localhost',port=6379,db=0)

cache = Cache(config={'CACHE_TYPE': 'redis','CACHE_REDIS':redis_client})