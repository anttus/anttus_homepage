import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST: str = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT: int = 6379
REDIS_HOST_STR = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
RESULT_EXPIRES = 3600

app = Celery("tasks", broker=REDIS_HOST_STR, backend=REDIS_HOST_STR)

app.conf.update(
    result_expires=RESULT_EXPIRES,
)
