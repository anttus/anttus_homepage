import requests, json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn.workers import UvicornWorker
from redis import Redis
from tasks import process_data

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

REDIS_HOST = "localhost"
REDIS_PORT = 6379
redis_client: Redis = Redis(
    host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, db=0
)

cv_url = (
    "https://gist.githubusercontent.com/anttus/d1285d208ef1cb4d54e27561251e38cd/raw/"
)


@app.get("/")
async def root(request: Request):
    page_view_count = redis_client.get("page_view_count") or 0
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"data": load_data(), "page_view_count": page_view_count},
    )


def load_data():
    try:
        r = requests.get(cv_url)
        return json.loads(r.content)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


@app.post("/collect-data")
async def collect_data(request: Request):
    data = await request.json()
    process_data(data)
    return {"message": "Data received"}


class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": "logging.yaml",
    }
