from datetime import datetime
from celery import shared_task
from redis import Redis

r = Redis(host="localhost", port=6379, db=0, decode_responses=True)


@shared_task
def process_data(data: dict) -> dict:
    if data:
        r.incr("page_view_count")
        id = r.get("page_view_count")
        language: str = data["navigator"]["language"]
        user_agent: str = data["navigator"]["userAgent"]
        now = datetime.now()
        r.hset("user:%s" % id, "id", str(id))
        r.hset("user:%s" % id, "language", language)
        r.hset("user:%s" % id, "user_agent", user_agent)
        r.hset("user:%s" % id, "time", str(now))
    return data
