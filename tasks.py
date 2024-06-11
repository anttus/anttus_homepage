import os
from datetime import datetime
from celery import shared_task
from redis import Redis
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST: str = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT: int = 6379

r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
r.ping()


@shared_task
def process_data(data: dict) -> dict:
    if data:
        r.incr("page_view_count")
        id = r.get("page_view_count")
        language: str = data["navigator"]["language"]
        user_agent: str = data["navigator"]["userAgent"]
        now = datetime.now()
        epoch = datetime.now().timestamp()
        r.hset("user:%s" % id, "id", str(id))
        r.hset("user:%s" % id, "language", language)
        r.hset("user:%s" % id, "user_agent", user_agent)
        r.hset("user:%s" % id, "time", str(now))
        r.hset("user:%s" % id, "epoch", str(epoch))
    return data
