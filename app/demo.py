from typing import Union
from fastapi import FastAPI
import redis


app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    redis_client.set(item_id, q)
    return {"item_id": item_id, "q": q}
