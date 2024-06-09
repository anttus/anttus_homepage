from celery import Celery

REDIS_HOST = "redis://redis-service:6379/0"

app = Celery("tasks", broker=REDIS_HOST, backend=REDIS_HOST)

app.conf.update(
    result_expires=3600,
)
